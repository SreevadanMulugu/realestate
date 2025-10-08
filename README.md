
Project Title: Real Estate Chatbot – AI-Powered Property Assistant

Demo 
https://drive.google.com/file/d/11ILlIRzmhg0bOut6UIzUmal23ylSTPhr/view?usp=sharing

Overview:
A smart AI-powered chatbot for real estate queries, integrating Google Gemini LLM, property database, and live web search for amenities and market info. The chatbot provides concise, natural answers to user questions about properties, always synthesizing information using the LLM.
 
Features:
- Natural language Q&A about properties (price, location, features)
- Fetches nearby amenities (schools, hospitals, parks, etc.)
- LLM-powered conversational answers (Gemini, with grounded web search)
- Simple web chat UI
- Admin panel for property management

---

Architecture & Workflow:

Backend:
- Python (FastAPI)
- SQLite property database
- Google Gemini LLM (with grounded search)


Frontend:
- HTML/JS web chat interface

Workflow:
1. User submits a query (e.g., “What schools are near Lotus Villa?”).
2. Backend fetches property info from the database.
3. Backend sends the user query and property info as context to Gemini.
4. Gemini LLM decides whether to use Google Search for additional info.
5. Gemini synthesizes a concise, direct answer (never just links or generic advice).
6. The answer is returned to the user via the chat UI.

 
<img width="3840" height="2061" alt="Untitled diagram _ Mermaid Chart-2025-07-09-065529" src="https://github.com/user-attachments/assets/655b96ab-33a5-4c4a-a4d6-76a36a4e4a31" />


Setup Instructions:
- Install dependencies using pip and the requirements.txt file.
- Run the app with Uvicorn.
- Open the application in your browser at the specified local address.

---

Main Modules:
- app.py: FastAPI app, routes, and endpoints for chat, property info, admin, and amenities.
- chat/agent.py: Handles chatbot logic, always using Gemini LLM with property info and (optionally) web search context.
- db/query.py: Handles all property database operations (CRUD, search, fetch by ID).
- web/maps_api.py: Simulates Google Places API for nearby amenities.
- web/chatbot.html: Frontend chat interface.

---

Example Prompts:
- “What’s the price of Lotus Villa?”
- “What schools are nearby Pearl Heights?”
- “Is this a good area for investment?”
- “Show me hospitals near Green Valley Apartments.”

 
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/cdeeb5f4-c4bd-41ab-8add-12e264e283a1" />


Key Design Principles:
- The LLM always generates the final answer and never just outputs web search results.
- Property info and web search context are always provided to the LLM.
- No filtering or classification is done; all context is sent to Gemini, which decides what to use.
- Answers are concise, relevant, and direct.

---

Extending to Production:
- Add authentication and user management.
- Deploy on scalable cloud infrastructure.
- Add logging, monitoring, and error handling.
- Secure API keys and sensitive data.

  

