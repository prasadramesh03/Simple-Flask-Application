from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return jsonify({
        "message": "Hello from the DevOps Project!",
        "hostname": hostname
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)