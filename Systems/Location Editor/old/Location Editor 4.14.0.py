import json
from version_history import VERSION_HISTORY

class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "0.11"

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

    def update_version(self, version):
        self.VERSION = version

    def add_location(self, new_location):
        self.locations[str(new_location['loc_id'])] = new_location
        self.save_locations()

    class FirstLocation:
        """
        A class that creates a location file if it doesn't exist or is empty, and adds a template to it.
        """
        def __init__(self, file_path):
            self.file_path = file_path
            self.add_template()

        def add_template(self):
            try:
                with open(self.file_path, "r") as file:
                    data = json.load(file)
                    if data:
                        return
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            template = LocationTemplate.get_template()
            with open(self.file_path, "w") as file:
                json.dump(template, file, indent=4)


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


class AddLocation:
    """
    A class for adding a new location to the game.
    Attributes:
    - location_editor (LocationEditor): The LocationEditor object that manages the locations in the game.
    """
    def __init__(self, location_editor):
        self.location_editor = location_editor

    def run(self):
        print("Add a new location:")
        name = input("Enter the name: ")
        description = input("Enter the description: ")
        location_type = input("Enter the type (from the list ['type1', 'type2', 'type3']): ")
        level = input("Enter the level: ")
        cells = {}
        loc_id = max(self.location_editor.locations.keys(), default=0) + 1
        new_location = {
            "loc_id": loc_id,
            "name": name,
            "description": description,
            "type": location_type,
            "level": level,
            "cells": cells
        }
        self.location_editor.add_location(new_location)
        print("Location added successfully!")
