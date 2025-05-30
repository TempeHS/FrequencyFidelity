from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 86400

@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    posts = dbHandler.get_forums()
    return render_template('/index.html', posts=posts)

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
            return index()
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
            return 
        else:
        status = dbHandler.insert_details(username, email, password)
        if status == True:
            return render_template('/login.html')
        else:
            print(status)
    else:
        return render_template('/signup.html')

@app.route('/graph.html', methods=['GET'])
def graph():
    return render_template('CrinGraph/graph.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)