from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS 


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
        output=check_password(password)
      
    return render_template('strengthCheckerPage.html', output=output)

@app.route('/pass_generator', methods=('GET', 'POST'))
def gotToPassGeneratorPage():
  output1=[]
  if request.method == 'POST':
    city = request.form.get("birthcity")
    mon = request.form.get("birthmon")
    hero = request.form.get("hero")
    food = request.form.get("food")
    color = request.form.get("color")

    #temp output for now  
    output1 = [city, mon, hero, food, color]
  return render_template('passGeneratorPage.html', output1=output1)