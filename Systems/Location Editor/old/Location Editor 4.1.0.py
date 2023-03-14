import json
from version_history import VERSION_HISTORY

class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "0.10"

    def __init__(self, file_path):
        self.file_path = file_path
        self.locations = {}
        self.load_locations()

    def load_locations(self):
        try:
            with open(self.file_path, "r") as file:
                self.locations = json.load(file)
        except FileNotFoundError:
            print("Location file not found.")
            pass

    def save_locations(self):
        with open(self.file_path, "w") as file:
            json.dump(self.locations, file, indent=4)

class LocationTemplate:
    """
    A class that creates an empty location template.
    """
    @staticmethod
    def get_template():
        template = {
            "loc_id": "",
            "name": "",
            "description": "",
            "type": [],
            "level": "",
            "cells": {}
        }
        return template
