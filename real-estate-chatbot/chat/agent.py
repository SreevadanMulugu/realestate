import os
import re
import google.generativeai as genai
from ..db import query as db_query
from ..utils import maps_api
from . import prompt_templates

# Configure the Gemini client (API key will be set later)
USER_PROVIDED_API_KEY = "AIzaSyD7NVbLAi-2pOOOFE4-C2wm_e0W__0Y3rk" # Key integrated here
genai.configure(api_key=USER_PROVIDED_API_KEY)

# Global variable for the Gemini model client
gemini_model = None # Will be initialized by initialize_gemini_client

def initialize_gemini_client(api_key: str = USER_PROVIDED_API_KEY): # Default to user provided key
    """Initializes the Gemini client with the provided API key."""
    global gemini_model
    if gemini_model: # Already initialized
        print("Gemini client already initialized.")
        return True
    try:
        # Ensure genai is configured if not done globally or needs reconfig
        if genai.API_KEY != api_key : #This check might be problematic if API_KEY is not a public attribute or if it's hashed/transformed
             genai.configure(api_key=api_key)

        gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using Flash for speed and cost
        print("Gemini client initializing...")
        # Try a simple generation to confirm API key validity
        # This also helps "warm up" the model or confirm connection.
        gemini_model.generate_content("Hello! This is a test call to verify API key and model access.")
        print("Gemini client initialized successfully and API key validated.")
        return True
    except Exception as e:
        print(f"Error initializing Gemini client or validating API key: {e}")
        gemini_model = None
        return False

def _call_gemini(prompt: str) -> str | None:
    """Helper function to call the Gemini API."""
    if not gemini_model:
        print("Error: Gemini client not initialized. Please set the API key.")
        return "Sorry, I'm having trouble connecting to my brain right now. Please try again later."
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Sorry, I encountered an error while processing your request: {e}"

def get_intent(user_query: str, property_names_list: list[str]) -> str:
    """Classifies the user's query intent using Gemini."""
    prompt = prompt_templates.INTENT_CLASSIFICATION_PROMPT_TEMPLATE.format(
        property_names_list_str=prompt_templates.get_available_properties_for_prompt(property_names_list),
        user_query=user_query
    )
    intent = _call_gemini(prompt)
    # Fallback if LLM returns something unexpected
    valid_intents = [
        "DB_QUERY_PRICE", "DB_QUERY_LOCATION", "DB_QUERY_DETAILS",
        "NEARBY_QUERY", "GENERAL_QUERY", "GREETING", "THANK_YOU", "UNKNOWN"
    ]
    if intent not in valid_intents:
        print(f"Warning: LLM returned unexpected intent '{intent}'. Defaulting to UNKNOWN.")
        return "UNKNOWN"
    return intent

def extract_property_entity(user_query: str, property_names_list: list[str]) -> str | None:
    """Extracts the property name from the user query using Gemini."""
    prompt = prompt_templates.ENTITY_EXTRACTION_PROMPT_TEMPLATE.format(
        property_names_list_str=prompt_templates.get_available_properties_for_prompt(property_names_list),
        user_query=user_query
    )
    entity = _call_gemini(prompt)
    if entity == "Unknown" or not entity:
        # Fallback: simple regex for property names if LLM fails or returns Unknown
        for prop_name in property_names_list:
            if re.search(r'\b' + re.escape(prop_name) + r'\b', user_query, re.IGNORECASE):
                return prop_name
        return None
    return entity

def extract_nearby_entities(user_query: str, property_names_list: list[str]) -> tuple[str | None, str | None]:
    """Extracts property name and place type for nearby queries using Gemini."""
    prompt = prompt_templates.ENTITY_EXTRACTION_NEARBY_PROMPT_TEMPLATE.format(
        property_names_list_str=prompt_templates.get_available_properties_for_prompt(property_names_list),
        user_query=user_query
    )
    response = _call_gemini(prompt) # Expected format: "PROPERTY_NAME|PLACE_TYPE"
    if response and '|' in response:
        parts = response.split('|', 1)
        property_name = parts[0].strip() if parts[0].strip() != "Unknown" else None
        place_type = parts[1].strip() if parts[1].strip() else "amenity"

        # Fallback for property name if LLM returns Unknown but it's in query
        if not property_name:
             for prop_name_iter in property_names_list:
                if re.search(r'\b' + re.escape(prop_name_iter) + r'\b', user_query, re.IGNORECASE):
                    property_name = prop_name_iter
                    break
        return property_name, place_type

    # Fallback if LLM fails
    property_name = None
    for prop_name_iter in property_names_list:
        if re.search(r'\b' + re.escape(prop_name_iter) + r'\b', user_query, re.IGNORECASE):
            property_name = prop_name_iter
            break

    # Simple place type extraction (can be improved)
    place_match = re.search(r'\b(schools?|hospitals?|parks?|restaurants?|shops?|stores?|malls?|amenit(y|ies)|facilities)\b', user_query, re.IGNORECASE)
    place_type = place_match.group(1) if place_match else "amenity"

    return property_name, place_type


def handle_query(user_query: str) -> str:
    """Handles the user query by routing it and generating a response."""
    if not gemini_model:
        return "Error: The chatbot is not initialized. Please ensure the API key is set correctly."

    property_names = db_query.get_all_property_names()
    intent = get_intent(user_query, property_names)
    print(f"[Agent] User Query: '{user_query}', Intent: {intent}")

    if intent == "GREETING":
        return prompt_templates.GREETING_RESPONSE_TEMPLATE
    if intent == "THANK_YOU":
        return prompt_templates.THANK_YOU_RESPONSE_TEMPLATE

    if intent in ["DB_QUERY_PRICE", "DB_QUERY_LOCATION", "DB_QUERY_DETAILS"]:
        property_name = extract_property_entity(user_query, property_names)
        if not property_name:
            return "I couldn't identify a specific property in your question. Please mention one of our available properties."

        db_data = db_query.get_property_details_by_name(property_name)
        if not db_data:
            return f"Sorry, I don't have information about '{property_name}'."

        # Tailor data for specific intents
        if intent == "DB_QUERY_PRICE":
            db_data_filtered = {"price": db_data.get("price", "Not available")}
        elif intent == "DB_QUERY_LOCATION":
            db_data_filtered = {"location": db_data.get("location", "Not available")}
        else: # DB_QUERY_DETAILS
            db_data_filtered = db_data

        prompt = prompt_templates.FORMAT_DB_RESPONSE_PROMPT_TEMPLATE.format(
            user_query=user_query,
            property_name=property_name,
            db_data=str(db_data_filtered)
        )
        return _call_gemini(prompt)

    elif intent == "NEARBY_QUERY":
        property_name, place_type = extract_nearby_entities(user_query, property_names)
        if not property_name:
            return "Please specify which property you're asking about for nearby places."
        if not place_type:
            place_type = "amenities" # Default if not extracted

        location_info = db_query.get_property_location_by_name(property_name)
        if not location_info:
            return f"Sorry, I couldn't find location details for '{property_name}' to search for nearby {place_type}."

        nearby_places_list = maps_api.get_nearby_places(
            location_info["latitude"], location_info["longitude"], place_type, property_name
        )
        prompt = prompt_templates.FORMAT_NEARBY_RESPONSE_PROMPT_TEMPLATE.format(
            user_query=user_query,
            property_name=property_name,
            place_type=place_type,
            nearby_places_list=str(nearby_places_list)
        )
        return _call_gemini(prompt)

    elif intent == "GENERAL_QUERY":
        prompt = prompt_templates.GENERAL_KNOWLEDGE_PROMPT_TEMPLATE.format(user_query=user_query)
        return _call_gemini(prompt)

    else: # UNKNOWN or other unhandled
        return prompt_templates.UNKNOWN_QUERY_RESPONSE_TEMPLATE


if __name__ == '__main__':
    # This part is for testing. Requires API key to be set as an environment variable
    # or by uncommenting and setting the genai.configure line at the top.
    print("Agent Test Mode")

    # ---- IMPORTANT: SET YOUR API KEY HERE FOR LOCAL TESTING ----
    # Example: os.environ["GEMINI_API_KEY"] = "YOUR_ACTUAL_API_KEY"
    # Or, uncomment and fill this:
    # initialize_gemini_client("YOUR_API_KEY_HERE_FOR_TESTING")
    # -----------------------------------------------------------

    if not os.getenv("GEMINI_API_KEY") and not gemini_model:
        print("Please set the GEMINI_API_KEY environment variable or initialize client in code for testing.")
        print("Example: export GEMINI_API_KEY='your_key_here'")
    elif os.getenv("GEMINI_API_KEY") and not gemini_model:
         api_key_env = os.getenv("GEMINI_API_KEY")
         if not initialize_gemini_client(api_key_env):
             print("Failed to initialize Gemini client with environment variable.")
             exit()


    if gemini_model:
        test_queries = [
            "Hello there!",
            "What's the price of Lotus Villa?",
            "Tell me about Green Valley Apartments.",
            "Where is Pearl Heights located?",
            "What schools are near Green Valley Apartments?",
            "Are there any parks near Sunset Bungalow?",
            "Is Kondapur a good place to live?",
            "Thanks for the info!",
            "gibberish query test"
        ]
        for q in test_queries:
            response = handle_query(q)
            print(f"Query: {q}\nResponse: {response}\n---")
    else:
        print("Skipping interactive tests as Gemini client is not initialized.")
