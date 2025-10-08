# Real Estate Chatbot PoC

A smart AI-powered chatbot for real estate queries, integrating Gemini LLM and simulated property/landmark data.

## Features
- Natural language Q&A about properties (price, location)
- Fetches nearby landmarks (schools, hospitals)
- LLM-powered conversational answers
- Simple web chat UI

## Tech Stack
- FastAPI (Python backend)
- Google Gemini LLM (via google-generativeai)
- Simulated DB and Google Places API
- HTML/JS frontend

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   cd real-estate-chatbot && python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
3. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Example Prompts
- What's the price of Lotus Villa?
- What schools are nearby Pearl Heights?
- Is this a good area for investment? 