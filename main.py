import json
from difflib import get_close_matches

def load_knowledge_base(file_path):
    """Loads the knowledge base from a given file path."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path, data):
    """Saves the given data to the knowledge base at the specified file path."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question, questions):
    """Finds the best match for a user's question from a list of questions."""
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question, knowledge_base):
    """Retrieves an answer for a given question from the knowledge base, if available."""
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None  # Explicitly return None if no match is found

def chat_bot():
    """Runs the chat bot, loading and updating the knowledge base as necessary."""
    knowledge_base = load_knowledge_base('knowledge_base.json')

    while True:
        user_input = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer, Can you teach me?')
            new_answer = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':  # Correct use of lower() method
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})  # Correct key for "answer"
                save_knowledge_base('knowledge_base.json', knowledge_base)  # Ensure the correct file name is used
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
