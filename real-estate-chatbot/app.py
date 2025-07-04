import os
from flask import Flask, request, jsonify, render_template
from chat.agent import handle_query, initialize_gemini_client

app = Flask(__name__, template_folder='web', static_folder='web/static')

# Initialize Gemini Client when the app starts
# The API key will be requested from the user if not found as an environment variable
API_KEY_INITIALIZED = False

@app.before_request
def ensure_api_key():
    global API_KEY_INITIALIZED
    if not API_KEY_INITIALIZED:
        # This part is tricky for a non-interactive setup.
        # For now, we'll rely on an environment variable or a placeholder.
        # In a real deployment, this would be handled during setup or configuration.
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            if initialize_gemini_client(api_key):
                API_KEY_INITIALIZED = True
            else:
                print("Failed to initialize Gemini client with API key from environment variable.")
                # App will run but chatbot functionality will be impaired.
                # Error messages will be shown by the agent.
        else:
            print("GEMINI_API_KEY environment variable not found.")
            # Instructions for user will be part of README and Colab.


@app.route('/')
def home():
    # Serve the chatbot HTML page
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    global API_KEY_INITIALIZED
    if not API_KEY_INITIALIZED:
        # Attempt to initialize again if it failed before and key might have been set
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            if initialize_gemini_client(api_key):
                API_KEY_INITIALIZED = True
            else:
                return jsonify({"error": "Failed to initialize AI model. API key might be invalid."}), 500
        else:
            return jsonify({"error": "AI model not initialized. GEMINI_API_KEY is missing."}), 500

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_query = data.get('query')

    if not user_query:
        return jsonify({"error": "Missing 'query' in request data"}), 400

    try:
        response_text = handle_query(user_query)
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error during handle_query: {e}")
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

@app.route('/health')
def health_check():
    return jsonify({"status": "ok", "api_key_initialized": API_KEY_INITIALIZED}), 200


if __name__ == '__main__':
    # Note: For local execution without Docker/Colab, ensure GEMINI_API_KEY is set.
    # e.g., export GEMINI_API_KEY='your_api_key_here'
    print("Flask app starting...")
    print("To use the chatbot, ensure GEMINI_API_KEY environment variable is set.")
    print("Example: export GEMINI_API_KEY='your_actual_gemini_api_key'")
    print("Then run: python app.py")
    print("Access the UI at http://127.0.0.1:5000/")
    print("Send POST requests to http://127.0.0.1:5000/chat with JSON {'query': 'Your question'}")

    # The API key check will happen in before_request
    # If running locally and key is not set, agent will return error messages.
    app.run(debug=True, host='0.0.0.0', port=5000)
