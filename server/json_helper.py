import json, threading
from typing import Any
print("rename this quota, should be make_json.py now")

class JSONManager:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._lock = threading.Lock()
        self._load_json()

    def _load_json(self):
        """Loads the JSON data from the file."""
        try:
            with open(self._file_path, 'r') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {}
        except json.JSONDecodeError:
            self._data = {}

    def _save_json(self):
        """Saves the JSON data back to the file."""
        with open(self._file_path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def get_data(self):
        """Returns the JSON data."""
        return self._data

    def update_data(self, key, value):
        """Updates a value in the JSON data and saves it."""
        self._data[key] = value
        self._save_json()

    def delete_key(self, key):
        """Deletes a key from the JSON data and saves it."""
        if key in self._data:
            del self._data[key]
            self._save_json()

    def get_key(self, key: str, default: None = None) -> Any:
        """Gets a key from the JSON data."""
        return self._data.get(key, default)
