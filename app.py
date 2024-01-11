import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.static_folder = 'static'

# Load the trained model
model = load_model('model.h5')

# Load the intents and preprocessed data
intents = json.loads(open('masakan.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Clean up sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Create bag of words array
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

# Predict the intent of the user's message
def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Get all responses based on intent
def get_responses(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    responses = []
    for intent in list_of_intents:
        if intent['tag'] == tag:
            responses.extend(intent['responses'])
    return responses

# Process user's message and generate response
def chatbot_response(msg):
    ints = predict_class(msg, model)
    responses = get_responses(ints, intents)
    return responses

# Define routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    responses = chatbot_response(user_text)
    choices = []
    dataset_responses = []
    if responses and len(responses) > 0:
        choices = [response for response in responses if response != user_text]
        dataset_responses = [response for response in responses if response == user_text]
    return jsonify({"response": user_text, "choices": choices, "dataset_responses": dataset_responses})

if __name__ == "__main__":
    app.run()
