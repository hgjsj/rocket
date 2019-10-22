from flask import Flask, url_for


app = Flask(__name__)

@app.route('/hello_world')
def hello():
    return "hello word"

#app.add_url_rule('/', 'hello', hello)
