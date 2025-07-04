# Real Estate Chatbot PoC (LLM Integrated)

This project is a Proof of Concept for an AI-powered real estate chatbot using a Large Language Model (LLM) integration, specifically Google's Gemini. The chatbot can answer questions about property prices, locations, details, and nearby amenities based on a mock internal database and simulated external API calls.

## Features

*   **Natural Language Q&A**: Users can ask questions in free-form.
*   **Intent Recognition**: Uses an LLM to determine the user's intent (e.g., asking for price, location, nearby places).
*   **Entity Extraction**: Uses an LLM to identify key information from queries (e.g., property name, type of amenity).
*   **Database Integration (Mock)**: Retrieves property data from an internal mock database.
*   **External API Simulation (Mock)**: Simulates fetching contextual data (e.g., nearby landmarks) from external APIs like Google Maps.
*   **LLM for Response Generation**: Uses an LLM to format answers naturally and handle general real estate questions.
*   **Simple Web UI**: Basic HTML and JavaScript interface for interacting with the chatbot.

## Tech Stack

*   **Backend**: Python, Flask
*   **LLM Integration**: Google Gemini API (`google-generativeai` SDK)
*   **Data Source (Mock)**: Python dictionaries in `db/query.py`
*   **External API (Mock)**: Python functions in `utils/maps_api.py`
*   **Frontend**: Basic HTML, CSS, JavaScript

## Project Structure

```
real-estate-chatbot/
├── app.py                  # Main Flask application
├── chat/
│   ├── __init__.py
│   ├── agent.py            # Core chatbot logic (intent, entity, routing, LLM calls)
│   └── prompt_templates.py # Prompts for guiding the LLM
├── db/
│   ├── __init__.py
│   └── query.py            # Mock database functions
├── utils/
│   ├── __init__.py
│   └── maps_api.py         # Mock external API functions (e.g., for nearby places)
├── web/
│   └── chatbot.html        # HTML, CSS, JS for the chat UI
├── requirements.txt        # Python package dependencies
└── README.md               # This file
```

## Setup and Running the Project

### Prerequisites

*   Python 3.8+
*   Access to Google Gemini API and an API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Steps

1.  **Clone the repository (if applicable) or create the files as per the structure.**

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set the Gemini API Key:**
    You **MUST** set your Gemini API key as an environment variable.
    ```bash
    export GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
    ```
    On Windows (Command Prompt):
    ```bash
    set GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
    ```
    Or Windows (PowerShell):
    ```bash
    $env:GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
    ```
    The application will attempt to read this key when it starts.

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will start, typically on `http://127.0.0.1:5000/`.

6.  **Access the chatbot:**
    Open your web browser and go to `http://127.0.0.1:5000/`.

## How it Works

1.  The user types a query into the web UI.
2.  The JavaScript frontend sends the query to the `/chat` endpoint of the Flask backend.
3.  `app.py` receives the query and passes it to `chat.agent.handle_query()`.
4.  The `agent.py` module:
    a.  Initializes the Gemini client (if not already done, using the API key).
    b.  Uses an LLM call with `INTENT_CLASSIFICATION_PROMPT_TEMPLATE` to determine the user's intent.
    c.  If necessary (for DB or nearby queries), uses another LLM call with entity extraction prompts to identify property names or amenity types.
    d.  **DB Queries**: Fetches data from `db/query.py`.
    e.  **Nearby Queries**: Fetches data from `utils/maps_api.py` (after getting coordinates from `db/query.py`).
    f.  Uses the LLM again with formatting prompts (`FORMAT_DB_RESPONSE_PROMPT_TEMPLATE`, `FORMAT_NEARBY_RESPONSE_PROMPT_TEMPLATE`) to generate a natural language response.
    g.  **General Queries**: Directly uses the LLM with `GENERAL_KNOWLEDGE_PROMPT_TEMPLATE`.
5.  The response is sent back to the frontend and displayed to the user.

## Colab Notebook

For easy execution, a Google Colab notebook version will be provided that bundles all the code and handles dependencies within the Colab environment. You will still need to provide your Gemini API Key in the Colab notebook.

## Future Improvements (Optional for PoC)

*   **Real Database Integration**: Connect to MongoDB, PostgreSQL, etc.
*   **Real Google Maps/Places API**: Use actual API calls for live data.
*   **LangChain/LlamaIndex**: Implement more sophisticated agent routing and RAG patterns.
*   **Memory**: Add conversation history for context awareness.
*   **Error Handling**: More robust error handling and logging.
*   **Security**: Input sanitization, API key management best practices for production.
*   **Streaming Responses**: For a more interactive feel.
*   **Frontend Enhancements**: A more polished UI using a framework like React or Vue.
```
