from flask import Flask, render_template, flash, request, session, send_file, jsonify
from flask import render_template, redirect, url_for, request
import os
import mysql.connector

import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
import datetime
import time

lemmatizer = WordNetLemmatizer()

# chat initialization
model = load_model("chatbot_model.h5")
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/NewMentor")
def NewMentor():
    return render_template('NewMentor.html')


@app.route('/MentorLogin')
def MentorLogin():
    return render_template('MentorLogin.html')


@app.route("/NewStudent")
def NewStudent():
    return render_template('NewStudent.html')


@app.route("/StudentLogin")
def StudentLogin():
    return render_template('StudentLogin.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['Password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM mentortb")
            data = cur.fetchall()

            return render_template('AdminHome.html', data=data)
        else:
            flash("UserName or Password Incorrect!")

            return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM mentortb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)


@app.route("/AStudentInfo")
def AStudentInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()

    return render_template('AStudentInfo.html', data=data)


@app.route("/newmentor", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        Subject = request.form['Subject']
        username = request.form['username']
        Password = request.form['Password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from mentortb where username='" + username + "' ")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into mentortb values('','" + name + "','" + age + "','" + mobile + "','" + email + "','" + address + "','" + Subject + "','" +
                username + "','" + Password + "')")
            conn.commit()
            conn.close()
            return render_template('MentorLogin.html')



        else:
            flash('Already Register Username')
            return render_template('NewMentor.html')


@app.route("/mentorlogin", methods=['GET', 'POST'])
def mentorlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['Password']
        session['mname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from mentortb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('MentorLogin.html')

        else:
            session['subject'] = data[6]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM mentortb where UserName='" + session['mname'] + "' ")
            data = cur.fetchall()

            return render_template('MentorHome.html', data=data)


@app.route("/MentorHome")
def MentorHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM mentortb where UserName='" + session['mname'] + "' ")
    data = cur.fetchall()

    return render_template('MentorHome.html', data=data)


@app.route('/ShareNotes')
def ShareNotes():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sharetb where MName='" + session['mname'] + "' ")
    data = cur.fetchall()

    return render_template('ShareNotes.html', data=data, subject=session['subject'])


@app.route("/newsharenote", methods=['GET', 'POST'])
def newsharenote():
    if request.method == 'POST':
        name = request.form['name']
        Info = request.form['Info']
        Batch = request.form['Batch']

        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + file.filename
        file.save("static/upload/" + savename)

        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where Batch='" + Batch + "' ")
        data = cursor.fetchone()
        if data:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into sharetb values('','" + session[
                    'mname'] + "','" + name + "','" + savename + "','" + Info + "','" + Batch + "','" + date + "')")
            conn.commit()
            conn.close()
            flash('Record Saved..!')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sharetb where MName='" + session['mname'] + "' ")
            data = cur.fetchall()

            return render_template('ShareNotes.html', data=data, subject=session['subject'])

        else:
            flash('Student Not Found This Year')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sharetb where MName='" + session['mname'] + "' ")
            data = cur.fetchall()
            return render_template('ShareNotes.html', data=data, subject=session['subject'])


@app.route("/MRemove")
def MRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cursor = conn.cursor()
    cursor.execute("delete from  sharetb  where id='" + id + "' ")
    conn.commit()
    conn.close()
    flash('Notes Removed..!')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sharetb where MName='" + session['mname'] + "' ")
    data = cur.fetchall()
    return render_template('ShareNotes.html', data=data, subject=session['subject'])


@app.route("/MQueryInfo")
def MQueryInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where Answer='waiting' and Mname='" + session['mname'] + "'  ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where Answer!='waiting' and Mname='" + session['mname'] + "'  ")
    data1 = cur.fetchall()
    return render_template('MQueryInfo.html', data=data, data1=data1)


@app.route("/Forward")
def Forward():
    id = request.args.get('id')
    session['qid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM mentortb   ")
    data = cur.fetchall()

    return render_template('Forward.html', data=data)


@app.route("/Answer")
def Answer():
    id = request.args.get('id')
    session['qid'] = id
    return render_template('Answer.html')


@app.route("/answer", methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        Answer = request.form['Answer']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute(
            "update   Querytb set Answer='" + Answer + "'  where id='" + session['qid'] + "' ")
        conn.commit()
        conn.close()
        flash("Record Saved!")

        return MQueryInfo()


@app.route("/forwardq", methods=['GET', 'POST'])
def forwardq():
    if request.method == 'POST':
        ment = request.form['Batch']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute(
            "update   Querytb set Mname='" + ment + "'  where id='" + session['qid'] + "' ")
        conn.commit()
        conn.close()
        flash("Forward to Mentor Saved!")
        return MQueryInfo()


@app.route("/newstudent", methods=['GET', 'POST'])
def newstudent():
    if request.method == 'POST':
        name = request.form['name']
        regno = request.form['regno']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        Subject = request.form['Batch']
        username = request.form['username']
        Password = request.form['Password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' ")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into regtb values('','" + name + "','" + regno + "','" + mobile + "','" + email + "','" + address + "','" + Subject + "','" +
                username + "','" + Password + "')")
            conn.commit()
            conn.close()
            return render_template('StudentLogin.html')

        else:
            flash('Already Register Username')
            return render_template('NewStudent.html')


@app.route("/studentlogin", methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['Password']
        session['sname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('StudentLogin.html')

        else:
            session['regno'] = data[2]
            session['batch'] = data[6]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where UserName='" + session['sname'] + "' ")
            data = cur.fetchall()

            return render_template('StudentHome.html', data=data)


@app.route("/StudentHome")
def StudentHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where UserName='" + session['sname'] + "' ")
    data = cur.fetchall()
    return render_template('StudentHome.html', data=data)


@app.route("/SNotes")
def SNotes():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sharetb where Batch='" + session['batch'] + "' ")
    data = cur.fetchall()
    return render_template('SNotes.html', data=data)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':

        Subject = request.form['Subject']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from sharetb where Subject='" + Subject + "' and Batch='" + session['batch'] + "'")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sharetb where Batch='" + session['batch'] + "' ")
            data = cur.fetchall()
            flash('Record Not Found..!')
            return render_template('SNotes.html', data=data)

        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * from sharetb where Subject='" + Subject + "' and Batch='" + session['batch'] + "'")
            data = cur.fetchall()
            return render_template('SNotes.html', data=data)


@app.route("/Download")
def Download():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from sharetb where id ='" + str(id) + "'   ")
    data = cursor.fetchone()
    if data is None:
        return 'material Not Upload'
    else:
        filename = "static/upload/" + data[3]
        return send_file(filename, as_attachment=True)


@app.route("/NewQuery")
def NewQuery():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Mentortb  ")
    data = cur.fetchall()
    return render_template('NewQuery.html', data=data)


@app.route("/msearch", methods=['GET', 'POST'])
def msearch():
    if request.method == 'POST':

        Subject = request.form['Subject']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from Mentortb where Subject='" + Subject + "' ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Mentortb  ")
            data = cur.fetchall()
            flash('Record Not Found..!')
            return render_template('NewQuery.html', data=data)

        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * from Mentortb where Subject='" + Subject + "' ")
            data = cur.fetchall()
            return render_template('NewQuery.html', data=data)


@app.route("/newq")
def newq():
    sub = request.args.get('sub')
    mname = request.args.get('mname')
    return render_template('NewQuerys.html', sub=sub, mname=mname)


@app.route("/newquery", methods=['GET', 'POST'])
def newquery():
    if request.method == 'POST':
        mname = request.form['mname']
        sub = request.form['sub']
        Query = request.form['Query']

        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into Querytb values('','" + mname + "','" + sub + "','" + Query + "','waiting','" + date + "','" +
            session['sname'] + "')")
        conn.commit()
        conn.close()
        flash('Record Saved..!')
        return NewQuery()


@app.route("/SAnswer")
def SAnswer():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where Sname='" + session['sname'] + "'  ")
    data = cur.fetchall()
    return render_template('SAnswer.html', data=data)


@app.route("/Qsearch", methods=['GET', 'POST'])
def Qsearch():
    if request.method == 'POST':

        Subject = request.form['Subject']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from Querytb where Subject='" + Subject + "' ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Querytb where Sname='" + session['sname'] + "'  ")
            data = cur.fetchall()
            flash('Record Not Found..!')
            return render_template('SAnswer.html', data=data)

        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Querytb where Sname='" + session['sname'] + "'  ")
            data = cur.fetchall()
            return render_template('SAnswer.html', data=data)


@app.route('/Chat')
def Chat():
    return render_template('Chat.html')


@app.route("/ask", methods=['GET', 'POST'])
def ask():
    message = str(request.form['messageText'])

    # msg = request.form["msg"]
    msg = message
    print(msg)
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
    elif msg == "Mentor" or msg == "mentor" or msg == "MENTOR":

        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        # search Result
        cur1 = conn1.cursor()
        cur1.execute(
            "SELECT *  from mentortb  ")
        data1 = cur1.fetchall()

        for item1 in data1:

            ss1 = '<a href="http://127.0.0.1:5000/newq?id='
            ss11 = item1[0] + "&sub" + item1[6] + "&mname" + item1[7] + '">NewQuery</a> <br>'

            price1 = '<p class="price">SubjectName ' + item1[6] + '</p> <br>'

            bot_response1 = ss1 + ss11 + price1

            if (bott1 == ""):
                bott1 = bot_response1
            else:
                bott1 = bott1 + bot_response1

            print(bott1)
        res = bott1
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    # return res
    return jsonify({'status': 'OK', 'answer': res})


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    bott1 = ''
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
    elif msg == "Mentor" or msg == "mentor" or msg == "MENTOR":

        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1collegementordb')
        # search Result
        cur1 = conn1.cursor()
        cur1.execute(
            "SELECT *  from mentortb  ")
        data1 = cur1.fetchall()

        for item1 in data1:

            ss1 = '<a href="http://127.0.0.1:5000/newq?id='
            ss11 = str(item1[0]) + "&sub=" + item1[6] + "&mname=" + item1[7] + '">NewQuery</a> <br>'

            price2 = '<p class="price">MentorName ' + item1[7] + '</p> <br>'

            price1 = '<p class="price">SubjectName ' + item1[6] + '</p> <br>'

            bot_response1 = price2 + price1 +ss1 + ss11

            if (bott1 == ""):
                bott1 = bot_response1
            else:
                bott1 = bott1 + bot_response1

            print(bott1)
        res = bott1
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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
