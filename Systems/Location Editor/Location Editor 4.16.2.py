import json
import os

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
        self.load_file()

    def load_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.locations = json.load(file)
        else:
            print("Location file not found. Creating empty file...")
            with open(self.file_path, "w") as file:
                template = LocationTemplate.get_template()
                json.dump(template, file, indent=4)
            with open(self.file_path, "r") as file:
                self.locations = json.load(file)
    
    def save_file(self):
        with open(self.file_path, "w") as file:
            json.dump(self.locations, file, indent=4)

    def delete_file(self):
        confirmation = input("Are you sure you want to delete the location file? (y/n) ")
        if confirmation.lower() == "y":
            os.remove(self.file_path)
            print("Location file deleted.")
        else:
            print("File deletion cancelled.")

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
