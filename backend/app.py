from flask import Flask, request, jsonify
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os 
import openai
# Initialize Flask application
app = Flask(_name_)

# Connect to Milvus server
connections.connect("default", host="localhost", port="19530")

# Load SentenceTransformer model
sentence_transformer_ef = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Specify collection name
collection_name = "conversational_chatbot_ai"

genai.configure(api_key="AIzaSyCb9T6i-893AQOtF9KXgyXNSIp6OB_YFrY")
model = genai.GenerativeModel("gemini-1.5-flash")



def generate_response(relevant_doc, query):
    prompt = f"The user asked: {query}. Based on the following context: {relevant_doc}, please generate a helpful response in around 50 words."
    
    response = model.generate_content(prompt)
    print(response)
    if hasattr(response, 'candidates') and response.candidates:
        # Extract the text from the first candidate
        response_text = response.candidates[0].content.parts[0].text
        # Replace '\n' with actual line breaks and strip excess whitespace
        response_text = response_text.replace('\\n', '\n').strip()
        # Optional: Further formatting for indentation
        response_text = "\n".join(line.strip() for line in response_text.splitlines())
    else:
        response_text = "No response generated."

    return response_text


@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    # Encode query using the model
    embedding = sentence_transformer_ef.encode([query]).tolist()

    # Load the collection
    collection = Collection(collection_name)

    # Search parameters
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 16}
    }

    try:
        # Perform the search
        res = collection.search(
            data=embedding,  # Embedding query to search
            anns_field="embeddings",  # Field containing the vector data
            param=search_params,
            limit=1,  # Number of results to return
            output_fields=["source"]  # Return the 'source' field from the collection
        )

        # Extract relevant data from results
        results = [{"source": hit.entity.get('source')} for hit in res[0]]

        if results:
            response_text = generate_response(results[0]['source'], query)
            return jsonify({"response": response_text})

        # If no results found, generate content using Google AI
        ai_response = model.generate_content(query)
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if _name_ == "_main_":
    app.run(debug=True, port=5011)