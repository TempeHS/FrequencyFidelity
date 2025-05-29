from flask import Flask
from flask import render_template
from flask import request

import database_manager as dbHandler

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    posts = dbHandler.get_forums()
    return render_template('/index.html', posts=posts)

@app.route('/graph.html', methods=['GET'])
def graph():
    return render_template('CrinGraph/graph.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)