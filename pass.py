from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS 
import pandas as pd
import numpy as np
import random
import math
from urllib.request import urlopen


app = Flask(__name__)
app.static_folder = 'static'

#password checker backend

def check_length(password):
  if len(password) >= 12:
    return True
  return False

def check_symbol(password):
  symbols = "!\@#$%^&*()-+?_=,<>/'.:;[]`{}|~\" "
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
  symbols = "!\@#$%^&*()-+?_=,<>/'.:;[]`{}|~\" "
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

def cleanPass(password):
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

#password generator backend

def create_dict():
  words_dict = {}
  file = urlopen("https://www.eff.org/files/2016/09/08/eff_short_wordlist_1.txt").read().decode('utf-8')
  arr = file.split()

  for i in range(0, len(arr), 2):
    words_dict[arr[i].strip()] = arr[i+1].strip()
  return words_dict

def diceroll():
  num = ''
  for i in range(4):
    num += str(random.randint(1, 6))
  return num

def generate_password(length):
  password = ''
  if length == 1:
    length = 14
  elif length == 2:
    length = 20
  else:
    length = 27

  words_dict = create_dict()
  symbols = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/', '\'', ' ']
  symbol = random.choice(symbols)
  cap = random.randint(0, 2)
  breakpoint = random.randint(1,4)
  digit = start_digit = random.randint(0,95)
  used_words = []

  while len(password) < length:
    num = diceroll()
    word = words_dict[num]
    #check if the word is already used
    if word in used_words:
      continue
    used_words.append(word)
    word = word[:cap] + word[cap].upper() + word[cap + 1:]
    word = word[:breakpoint] + symbol + word[breakpoint:]
    password += (word + str(digit))
    digit += 1

  return [password, used_words, (cap + 1), (breakpoint + 1), start_digit]


#entropy backend
def calculate_entropy(password):
  length = len(password)
  characterSetSize = 0
  characterSet = []
  if check_digits(password):
    characterSetSize += 10
    characterSet.append("digits")
  if check_lower_alpha(password):
    characterSetSize += 26
    characterSet.append("lowercase letters")
  if check_upper_alpha(password):
    characterSetSize += 26
    characterSet.append("uppercase letters")
  if check_symbol(password):
    characterSetSize += 33
    characterSet.append("symbols and special characters")
  
  calculation = length * math.log2(characterSetSize)
  return [calculation, length, characterSet, characterSetSize]



#app routing

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
        password = cleanPass(password)
        output=check_password(password)
      
    return render_template('strengthCheckerPage.html', output=output)

@app.route('/pass_generator', methods=('GET', 'POST'))
def gotToPassGeneratorPage():
  passGen=[]
  output1=[]
  output2=[]
  output3=[]
  output4=[]
  if request.method == 'POST':
    charLen = int(request.form.get("length"))
    passGen=generate_password(charLen)

    output1.append(passGen[0])
    output2 = passGen[1]
    output3.append(passGen[2])
    output4.append(passGen[3])


  return render_template('passGeneratorPage.html',
   output1=output1, output2=output2, output3=output3, output4=output4)


@app.route('/entropy',  methods=('GET', 'POST'))
def goToEntropyPage():
  out1=[]
  out2=[]
  out3=[]
  out4=[]
  if request.method == 'POST':
    entropyPass = request.form.get("entropyPass")
    out1.append(calculate_entropy(entropyPass)[0])
    out2.append(calculate_entropy(entropyPass)[1])
    out3 = calculate_entropy(entropyPass)[2]
    out4.append(calculate_entropy(entropyPass)[3])

  return render_template('entropy.html', out1=out1, out2=out2, out3=out3, out4=out4)