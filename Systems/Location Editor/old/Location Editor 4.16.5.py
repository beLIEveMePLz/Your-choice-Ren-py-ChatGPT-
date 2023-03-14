import json

class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "4.16"

    def __init__(self, file_path):
        self.file_path = file_path
        self.locations = {}
        self.load_locations()

    def load_locations(self):
    try:
        with open(self.file_path, "r") as file:
            self.locations = json.load(file)
    except FileNotFoundError:
        print("Location file not found. Creating empty file...")
        with open(self.file_path, "w") as file:
            json.dump({}, file, indent=4)
        self.locations = {}

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
            "cells": {
                "cell_id": {
                    "name": "",
                    "description": "",
                    "type": "",
                    "exits": {}
                }
            }
        }
        return template
