import csv
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Load dataset from CSV
dataset = []
with open('bankingchatbotabc-master/AI-engine/data/Bitext_Sample_Customer_Service_Training_Dataset.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        dataset.append(row)

def get_intent(user_query):
    """
    Get the intent associated with the user query
    """
    for row in dataset:
        if user_query.lower() == row['utterance'].lower():
            return row['intent']
    return None  
def get_random_response(intent):
    """
    Generate a random response for the given intent
    """
    responses = [row['utterance'] for row in dataset if row['intent'] == intent]
    return random.choice(responses)

@app.route('/')
def hello_world():
    """
    Sample hello world
    """
    return render_template('home.html')

@app.route('/chat', methods=["POST"])
def chat():
    """
    Chat endpoint that performs intent recognition and constructs response from the dataset
    """
    try:
        user_query = request.form["text"]
        print("User Query:", user_query)
        intent = get_intent(user_query)
        print("Intent:", intent)
        
        if intent:
            response_text = intent
        else:
            response_text = "Sorry, I couldn't understand your query."
        
        return jsonify({"status": "success", "response": response_text})
    
    except Exception as e:
        print(e)
        return jsonify({"status": "success", "response": "Sorry, I am not trained to do that yet..."})

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8000)