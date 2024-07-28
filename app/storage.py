import json
import os

class Storage:
    def __init__(self, filename='data.json'):
        self.filename = filename

    def save(self, products):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        updated_data = existing_data + products
        with open(self.filename, 'w') as file:
            json.dump(updated_data, file, indent=4)
