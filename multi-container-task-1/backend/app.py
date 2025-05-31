from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/write')
def write_message():
    with open('/data/message.json', 'w') as f:
        json.dump({'message': 'Hello from Flask!'}, f)
    return jsonify({'status': 'written'})
