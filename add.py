from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import json
import datetime

app = Flask(__name__)


def load_qa_pairs(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return {}

qa_pairs = load_qa_pairs("qa_pairs.json")


bot = pipeline("conversational")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process_message", methods=["POST"])
def process_message():
    user_message = request.json.get("message", "")
    response = get_response(user_message, qa_pairs)
    if not response:
        response = bot(user_message)[0]['message']['content']
    return jsonify({"message": response})

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    feedback_data = request.json
    sentiment = feedback_data.get("sentiment", "")
    comment = feedback_data.get("comment", "")
    
    if sentiment and comment:
        
        timestamp = datetime.datetime.now().isoformat()
        feedback_entry = {"timestamp": timestamp, "sentiment": sentiment, "comment": comment}
        with open("feedback.json", "a", encoding="utf-8") as feedback_file:
            json.dump(feedback_entry, feedback_file, ensure_ascii=False)
            feedback_file.write("\n")
        
        
        return jsonify({"status": "Feedback received"})

    return jsonify({"error": "Invalid feedback data"}), 400

def get_response(user_input, qa_pairs):
    user_input = user_input.lower()
    for section, pairs in qa_pairs.items():
        for pair in pairs:
            if user_input in pair["question"].lower():
                return pair["answer"]
    return "I'm sorry, I don't have the answer to that question."

if __name__ == "__main__":
    app.run(debug=True)
