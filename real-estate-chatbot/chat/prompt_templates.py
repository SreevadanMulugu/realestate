# Prompt templates to guide the LLM

# Helper function to list available properties for prompts
def get_available_properties_for_prompt(property_list):
    if not property_list:
        return "No properties available."
    return ", ".join([f'"{name}"' for name in property_list])

INTENT_CLASSIFICATION_PROMPT_TEMPLATE = """
You are a real estate chatbot assistant. Your task is to classify the user's query into one of the following categories:
1.  **DB_QUERY_PRICE**: User is asking for the price of a specific property.
2.  **DB_QUERY_LOCATION**: User is asking for the location of a specific property.
3.  **DB_QUERY_DETAILS**: User is asking for general details, description, or type of a specific property.
4.  **NEARBY_QUERY**: User is asking about nearby places (schools, hospitals, parks, etc.) for a specific property.
5.  **GENERAL_QUERY**: User is asking a general real estate related question, an opinion, or something not covered by the above.
6.  **GREETING**: User is greeting the chatbot.
7.  **THANK_YOU**: User is thanking the chatbot.
8.  **UNKNOWN**: User query is unclear or not related to real estate.

Available properties: {property_names_list_str}

Analyze the user's query: "{user_query}"

Respond with only the category name (e.g., DB_QUERY_PRICE, NEARBY_QUERY, GENERAL_QUERY).
If the query mentions a property not in the list, try to classify the intent generally (e.g. if they ask for price of "Xyz property" and it's not in the list, classify as DB_QUERY_PRICE).
If the query is about a property in the list but the specific information type (price, location, details) is unclear, prefer DB_QUERY_DETAILS.
"""

ENTITY_EXTRACTION_PROMPT_TEMPLATE = """
You are a helpful assistant. Extract the primary real estate property name mentioned in the user's query.
Available properties: {property_names_list_str}
User query: "{user_query}"

If a property from the list is mentioned, respond with only the property name as listed (e.g., "Lotus Villa").
If multiple properties from the list are mentioned, respond with the first one.
If no specific property from the list is mentioned, or if the mentioned property is not in the list, respond with "Unknown".
"""

ENTITY_EXTRACTION_NEARBY_PROMPT_TEMPLATE = """
You are a helpful assistant. From the user's query, extract:
1. The primary real estate property name mentioned.
2. The type of place the user is asking about (e.g., school, hospital, park, restaurant, shop, mall, temple, church, mosque, etc.).

Available properties: {property_names_list_str}
User query: "{user_query}"

Respond in the format: "PROPERTY_NAME|PLACE_TYPE"
Example: "Pearl Heights|school"

If a property from the list is mentioned, use its exact name. If multiple properties are mentioned, use the first one.
If no specific property from the list is mentioned, or if the mentioned property is not in the list, use "Unknown" for PROPERTY_NAME.
If the type of place is not clear, use "place" as the PLACE_TYPE. If no specific place type is mentioned, use "amenity".
"""


FORMAT_DB_RESPONSE_PROMPT_TEMPLATE = """
You are a helpful real estate assistant.
The user asked: "{user_query}"
The database returned the following information for "{property_name}": {db_data}

Rephrase this information into a friendly and natural conversational response.
If the data contains price, ensure it's mentioned.
If the data contains location, ensure it's mentioned.
If the data contains a description, try to include it or a summary.
If specific information like only price was asked, focus on that.
If the database returned no information (None or empty), inform the user politely that the property details were not found or the specific detail is unavailable.
"""

FORMAT_NEARBY_RESPONSE_PROMPT_TEMPLATE = """
You are a helpful real estate assistant.
The user asked: "{user_query}"
Regarding the property "{property_name}", we found the following nearby {place_type}(s): {nearby_places_list}

Present this information in a friendly and natural conversational response.
If no places were found (list is empty or contains a 'no mock data' type message), inform the user politely that no such places were found nearby or information is unavailable.
List a few examples if many are available.
"""

GENERAL_KNOWLEDGE_PROMPT_TEMPLATE = """
You are a helpful and knowledgeable real estate assistant.
The user asked: "{user_query}"
Please provide a concise, informative, and neutral response to this general real estate question.
If the question is an opinion (e.g., "Is this a good area?"), provide a balanced view considering common factors for such an assessment (e.g., development, connectivity, amenities for area assessment).
If the question is too broad or subjective, you can state that.
Keep the response focused on real estate.
"""

GREETING_RESPONSE_TEMPLATE = "Hello! I'm your real estate assistant. How can I help you find information about our properties today?"
THANK_YOU_RESPONSE_TEMPLATE = "You're welcome! Let me know if there's anything else I can help you with."
UNKNOWN_QUERY_RESPONSE_TEMPLATE = "I'm sorry, I didn't quite understand that. Could you please rephrase your question? I can help with property prices, locations, details, and nearby amenities."

# Example of how to use with property list:
if __name__ == '__main__':
    sample_properties = ["Lotus Villa", "Green Valley Apartments", "Pearl Heights"]
    sample_query_price = "What's the price of Lotus Villa?"
    sample_query_nearby = "What schools are near Pearl Heights?"

    print("--- INTENT CLASSIFICATION ---")
    prompt_intent = INTENT_CLASSIFICATION_PROMPT_TEMPLATE.format(
        property_names_list_str=get_available_properties_for_prompt(sample_properties),
        user_query=sample_query_price
    )
    print(prompt_intent)

    print("\n--- ENTITY EXTRACTION (Property) ---")
    prompt_entity = ENTITY_EXTRACTION_PROMPT_TEMPLATE.format(
        property_names_list_str=get_available_properties_for_prompt(sample_properties),
        user_query=sample_query_price
    )
    print(prompt_entity)

    print("\n--- ENTITY EXTRACTION (Nearby) ---")
    prompt_entity_nearby = ENTITY_EXTRACTION_NEARBY_PROMPT_TEMPLATE.format(
        property_names_list_str=get_available_properties_for_prompt(sample_properties),
        user_query=sample_query_nearby
    )
    print(prompt_entity_nearby)


    print("\n--- FORMAT DB RESPONSE ---")
    sample_db_data = {'price': '₹75 Lakhs', 'location': 'Kondapur, Hyderabad', 'description': 'A beautiful villa.'}
    prompt_format_db = FORMAT_DB_RESPONSE_PROMPT_TEMPLATE.format(
        user_query=sample_query_price,
        property_name="Lotus Villa",
        db_data=str(sample_db_data)
    )
    print(prompt_format_db)

    print("\n--- FORMAT NEARBY RESPONSE ---")
    sample_nearby_places = ["Oakridge International School", "Chirec International School"]
    prompt_format_nearby = FORMAT_NEARBY_RESPONSE_PROMPT_TEMPLATE.format(
        user_query=sample_query_nearby,
        property_name="Pearl Heights",
        place_type="schools",
        nearby_places_list=str(sample_nearby_places)
    )
    print(prompt_format_nearby)

    print("\n--- GENERAL KNOWLEDGE ---")
    sample_general_query = "Is Gachibowli a good area for investment?"
    prompt_general = GENERAL_KNOWLEDGE_PROMPT_TEMPLATE.format(user_query=sample_general_query)
    print(prompt_general)
