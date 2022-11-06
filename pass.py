from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS 


app = Flask(__name__)
app.static_folder = 'static'
# CORS(app)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)


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
        output=[password, password]
      
    return render_template('strengthCheckerPage.html', output=output)

@app.route('/pass_generator')
def gotToPassGeneratorPage():
    return render_template('passGeneratorPage.html')