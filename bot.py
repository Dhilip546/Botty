import json
from transformers import pipeline

# Load the chatbot model
bot = pipeline("conversational")

def load_qa_pairs(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return {}

def get_response(user_input, qa_pairs):
    user_input = user_input.lower()
    for section, pairs in qa_pairs.items():
        for pair in pairs:
            if user_input in pair["question"].lower():
                return pair["answer"]
    return "I'm sorry, I don't have the answer to that question."

def main():
    qa_filename = "qa_pairs.json" 
    qa_pairs = load_qa_pairs(qa_filename)

    print("Chatbot: Hello! How can I assist you today? (Type 'exit' to end the conversation)")

    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'stop']:
            print("Chatbot: Goodbye!")
            break
        
        response = get_response(user_input, qa_pairs)
        if response:
            print("Chatbot:", response)
        else:
            response = bot(user_input)
            print("Chatbot:", response[0]['message']['content'])

if __name__ == "__main__":
    main()
