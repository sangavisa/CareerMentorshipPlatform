import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


# chat initialization
model = load_model("chatbot_model.h5")
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'




@app.route("/")
def hello():
    return render_template('Chat.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/ask",  methods=['GET', 'POST'])
def ask():

    message = str(request.form['messageText'])

    #msg = request.form["msg"]
    msg = message
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}", name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}", name)
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    #return res
    return jsonify({'status':'OK','answer':res})



@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    return res


# chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


'''def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result'''


import random

def getResponse(ints, intents_json):
    # Check if the 'ints' list is empty
    if not ints:
        return "I'm sorry, I didn't understand that."

    # Extract the predicted tag from the first element
    tag = ints[0].get("intent")

    # Extract the list of intents from the JSON data
    list_of_intents = intents_json.get("intents", [])

    # Search for the matching intent and return a random response
    for intent in list_of_intents:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "I'm sorry, I don't have a response for that."

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)