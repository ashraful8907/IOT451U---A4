import json

def save_to_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent = 4)

def load_from_json(file_path, data):
    with open(file_path, 'r') as f:
        return json.load(f)