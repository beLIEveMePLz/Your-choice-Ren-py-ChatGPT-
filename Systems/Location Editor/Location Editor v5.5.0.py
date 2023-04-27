import json
import os

VERSION = "5.5.0"

file_path = os.path.join(os.getcwd(), "locations.txt")

print(f"Locations file path: {file_path}")

class LocationTemplate:
    """
    A class that creates an empty location template.
    """
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
                "level": "",
                "connections": {}
            }
        }
    }

    @staticmethod
    def get_template():
        return LocationTemplate.template
      

class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "4.2.0"

    def __init__(self, file_path):
        self.file_path = file_path
        self.locations = {}
        self.load_file()

    def load_file(self):
        if os.path.exists(self.file_path):
            if os.stat(self.file_path).st_size == 0:
                template = LocationTemplate.get_template()
                self.locations = template
                self.save_file()
             else:
                with open(self.file_path, "r") as file:
                    self.locations = json.load(file)
        else:
            print("Location file not found. Creating empty file...")
            print("===============================================")
            with open(self.file_path, "w") as file:
                template = LocationTemplate.get_template()
                json.dump(template, file, indent=4)
            print("Location file created as empty file.")
            print("Populating file with template...")
            print("===============================================")
            self.locations = template
            print("Location file created with template inside.")
            print("===============================================")

    def save_file(self):
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
            print("Directory of file not found. Creating directories...")
            print("===============================================")
        tmp_file_path = self.file_path + ".tmp"
        with open(tmp_file_path, "w") as file:
            json.dump(self.locations, file, indent=4)
        os.rename(tmp_file_path, self.file_path)
        print("File saved successfully!")
        print("===============================================")

    def update_location(self, location_id, changes):
        """
        Update the specified location with the given changes and save the changes to the file.
        Args:
        - location_id (str): The ID of the location to update.
        - changes (dict): A dictionary of changes to apply to the location. Only keys that already exist in the location
                          will be updated; any new keys will be ignored.
        """
        if location_id in self.locations:
            location = self.locations[location_id]
            location.update(changes)
            self.save_file()
            print(f"Location '{location_id}' updated.")
            print("===============================================")
        else:
            print(f"Location ID '{location_id}' not found.")
            print("===============================================")
