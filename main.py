from flask import Flask
from flask import render_template
from flask import request, session, flash

import database_manager as dbHandler
import secrets

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex()
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 86400

@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index(check=None, credentials=None):
    posts = dbHandler.get_forums()
    return render_template('/index.html', posts=posts, nomatch=check, cred=credentials)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        email = request.form['eml']
        password = request.form['pswrd']
        response = dbHandler.retrieve_details(email, password)
        if response == True:
            session['status'] = response
            session['mail'] = email
            session['key'] = app.config["SECRET_KEY"]
            session['logs'] = False
            dbHandler.update_session(email, session['key'])
            return index(credentials=True)
        else: 
            return render_template('/login.html')
    else:
        return render_template('/login.html')
    
    
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['usrnm']
        email = request.form['eml']
        password = request.form['pswrd']
        confirm_password = request.form['pswrdCK']
        if password != confirm_password:
            flash('Passwords do not match')
            return index(check=True)
        else:
            status = dbHandler.insert_details(username, email, password)
            if status == True:
                return index()
            else:
                print(status)
    else:
        return render_template('/signup.html')
    
@app.route('/profile.html', methods=['POST', 'GET'])
def profile():
    if request.method == 'GET':
        if session['key'] == dbHandler.check_session(session['mail']):
            return render_template('/profile.html', cred=True)

@app.route('/sign_out')
def sign_out():
    dbHandler.reset_session(session['mail'])
    session.clear()
    return render_template('index.html')

@app.route('/graph.html', methods=['GET'])
def graph():
    return render_template('CrinGraph/graph.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)