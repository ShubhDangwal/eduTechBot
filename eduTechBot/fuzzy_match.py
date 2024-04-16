import json
import pickle
import random
from fuzzywuzzy import fuzz
import Levenshtein

def load_intents(file_path):
    with open(file_path, 'r') as file:
        intents = json.load(file)
    return intents['faq']

def preprocess_patterns(intents):
    patterns_dict = {}
    for intent in intents:
        for pattern in intent['patterns']:
            patterns_dict[pattern.lower()] = intent['responses']
    return patterns_dict

def fuzzy_match_response(input_text, patterns_dict):
    max_probability = 0
    best_response = None
    for pattern, responses in patterns_dict.items():
        levenshtein_distance = Levenshtein.distance(input_text, pattern)
        probability = 1 - (levenshtein_distance / max(len(input_text), len(pattern)))
        if probability > max_probability:
            max_probability = probability
            best_response = random.choice(responses)  # Randomly choose a response from the list
    return  max_probability, best_response

# Load intents from JSON file
intents = load_intents('intents.json')

# Preprocess patterns and responses
patterns_dict = preprocess_patterns(intents)

# Save patterns_dict to a file using pickle
with open('patterns_dict.pkl', 'wb') as f:
    pickle.dump(patterns_dict, f)