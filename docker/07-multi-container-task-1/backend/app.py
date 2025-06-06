from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/write')
def write_message():
    with open('/data/message.json', 'w') as f:
        json.dump({'message': 'Hello from Flask!'}, f)
    return jsonify({'status': 'written'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
