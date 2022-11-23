from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS 
import pandas as pd
import numpy as np
import random


app = Flask(__name__)
app.static_folder = 'static'
# CORS(app)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)

def check_length(password):
  if len(password) >= 12:
    return True
  return False

def check_symbol(password):
  symbols = "!@#$%^&*()-+?_=,<>/"
  if any(ch in symbols for ch in password):
    return True
  else:
    return False

def check_upper_alpha(password):
  if any(ch.isupper() for ch in password):
    return True
  return False

def check_lower_alpha(password):
  if any(ch.islower() for ch in password):
    return True
  return False

def check_digits(password):
  if any(ch.isdigit() for ch in password):
    return True
  return False  

def check_unique_chars(password):
  s = set(password)
  if len(s) >= len(password)//2:
    return True
  return False

def checkIfInList(word):
  csv = pd.read_csv("https://raw.githubusercontent.com/pkLazer/password_rank/master/4000-most-common-english-words-csv.csv")
  csv.columns = ['Word']

  words = np.array(csv.values.tolist())
  common_words = words.ravel().tolist()

  if (word.lower() in common_words):
    return True
  return False

def cleanStr(word):
  symbols = "!@#$%^&*()-+?_=,<>/"
  list1 =[]
  val = ""
  for i in word:
    if ((not i.isdigit()) and (i not in symbols)):
      val = val + i
    else:
      val+="1" #delimiting character to seperate words 
  list1 = val.split("1")
  list2 = [i for i in list1 if i != ""]
  return list2

def checkAll(word):
  if checkIfInList(word):
    return True
  else:
    val = cleanStr(word)
    for i in val:
      if checkIfInList(i):
        return True
  return False

def reverseVal(word):
  val = word[::-1]
  if checkAll(val):
    return True
  return False

def cleanStr(password):
  pass1 = password
  if("'" in password):
    pass1 = pass1.replace("'", "")
  elif('"' in password):
    pass1 = pass1.replace('"', "")

  return pass1


def check_password(password):
  arr = []
  if not check_length(password):
    arr.append("Password does not meet the minimum recommended length of 12")
  if not check_symbol(password):
    arr.append("Password does not contain any symbols")
  if not check_upper_alpha(password):
    arr.append("Password does not contain any upper case letters")
  if not check_lower_alpha(password):
    arr.append("Password does not contain any lower case letters")
  if not check_digits(password):
    arr.append("Password does not contain any digits")
  if not check_unique_chars(password):
    arr.append("Password does not meet the minimum number of unique characters")
  if checkAll(password):
    arr.append("**Warning** Password contains a common word. Check password randomness and access 'About' tab to learn more.")
  if reverseVal(password):
    arr.append("**Warning** Password contains a reversed common word. Check password randomness and access 'About' tab to learn more.")
  if(len(arr)==0):
    arr.append("Password has no vulnerabilities!")
  return arr

@app.route('/')
def goToMainPage():
     return render_template('mainPage.html')
    

@app.route('/learn')
def goToLearnPage():
    return render_template('learnPage.html')

@app.route('/strength_checker', methods=('GET', 'POST'))
def gotToStrengthCheckerPage():
    output=[]
    if request.method == 'POST':
        password = request.form.get("password")
        password = cleanStr(password)
        output=check_password(password)
      
    return render_template('strengthCheckerPage.html', output=output)

@app.route('/pass_generator', methods=('GET', 'POST'))
def gotToPassGeneratorPage():
  output1=[]
  if request.method == 'POST':
    charLen = request.form.get("length")
    output1.append(charLen)

    #temp output for now  
  return render_template('passGeneratorPage.html', output1=output1)

@app.route('/entropy',  methods=('GET', 'POST'))
def goToEntropyPage():
  output2=[]
  if request.method == 'POST':
    entropyPass = request.form.get("entropyPass")
    output2.append(entropyPass)

  return render_template('entropy.html', output2 = output2)