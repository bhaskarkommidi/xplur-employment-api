from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def helloIndex():
    return 'Hello World from Python Flask!'

app.run(host='127.0.0.1', port=5000)