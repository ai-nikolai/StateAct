from flask import Flask
import os

app = Flask(__name__)

@app.route('/abc')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    socket_path = './tmp/flask.sock'
    
    # Remove existing socket file if it exists
    if os.path.exists(socket_path):
        os.remove(socket_path)
    
    app.run(host='unix://' + socket_path)
