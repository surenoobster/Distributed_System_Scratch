# node.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
data_store = {}

# List of other nodes in the cluster
peers = ["http://localhost:5001", "http://localhost:5002"]

@app.route('/put', methods=['POST'])
def put():
    key = request.json['key']
    value = request.json['value']
    data_store[key] = value

    # Replicate to peers
    for peer in peers:
        if peer != request.host_url.strip('/'):
            try:
                requests.post(f"{peer}/replicate", json={"key": key, "value": value})
            except:
                pass  # Handle peer failure

    return jsonify({"status": "ok"}), 200

@app.route('/replicate', methods=['POST'])
def replicate():
    key = request.json['key']
    value = request.json['value']
    data_store[key] = value
    return jsonify({"status": "replicated"}), 200

@app.route('/get/<key>', methods=['GET'])
def get(key):
    value = data_store.get(key)
    return jsonify({"value": value}), 200

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1])
    app.run(port=port)
