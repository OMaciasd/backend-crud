from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(items):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f)

@app.route('/api/items', methods=['GET'])
def get_items():
    items = load_data()
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.json
    items = load_data()
    items.append(new_item)
    save_data(items)
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = request.json
    items = load_data()
    if 0 <= item_id < len(items):
        items[item_id] = updated_item
        save_data(items)
        return jsonify(updated_item)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = load_data()
    if 0 <= item_id < len(items):
        items.pop(item_id)
        save_data(items)
        return '', 204
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
