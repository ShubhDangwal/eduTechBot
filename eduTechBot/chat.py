import random
import json
import torch
import pickle
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from fuzzy_match import fuzzy_match_response

fallback_answers = [
    "I'm sorry, I didn't understand that. Can you please rephrase your question?",
    "Apologies, I'm not equipped to answer that question at the moment. Is there anything else I can assist you with?",
    "I'm still learning and might not have the answer to that question. Would you like me to try something else?",
    "I'm not programmed to respond to that query, but I'm here to help with a variety of other topics. What else can I do for you?",
    "It seems like I'm not familiar with that topic. Let's talk about something else. What would you like to know?",
    "I'm not sure how to help with that right now. Maybe I can assist you with something else instead?",
    "I'm afraid I can't provide an answer to that question. Is there anything else you'd like to ask?",
    "Hmm, it seems I'm unable to process that request. Let's try discussing a different topic. What else is on your mind?",
    "I'm sorry, I'm not capable of answering that question. Can I help you with something else?",
    "I'm still learning and may not have all the answers yet. Is there another question you'd like to ask?"
]

def load_chatbot_resources():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)

    with open('patterns_dict.pkl', 'rb') as f:
        patterns_dict = pickle.load(f)

    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    return device, patterns_dict, intents, all_words, tags, model

bot_name = "LearnHub Assistant"
print("Let's chat! (type 'quit' to exit)")
def chatbot_response(sentence, bot_name, device, patterns_dict, intents, all_words, tags, model):
    if sentence.lower() == "quit":
        return None
    
    highest_probability, best_response = fuzzy_match_response(sentence, patterns_dict)
    
    if highest_probability > 0.66:
        return f"{bot_name}: {best_response}"
    
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['faq']:
            if tag == intent["tag"]:
                return f"{bot_name}: {random.choice(intent['responses'])}"
    else:
        return f"{bot_name}: I do not understand..."
