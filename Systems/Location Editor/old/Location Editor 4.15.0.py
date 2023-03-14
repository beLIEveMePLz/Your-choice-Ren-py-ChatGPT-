import json

class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "4.15"

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

    def add_location(self, location):
        loc_id = location["loc_id"]
        if loc_id in self.locations:
            print(f"Location with ID '{loc_id}' already exists.")
        else:
            self.locations[loc_id] = location
            print(f"Location with ID '{loc_id}' added.")
        self.save_locations()

    def update_location(self, loc_id, new_data):
        if loc_id not in self.locations:
            print(f"Location with ID '{loc_id}' does not exist.")
        else:
            location = self.locations[loc_id]
            location.update(new_data)
            self.locations[loc_id] = location
            print(f"Location with ID '{loc_id}' updated.")
        self.save_locations()

    def delete_location(self, loc_id):
        if loc_id not in self.locations:
            print(f"Location with ID '{loc_id}' does not exist.")
        else:
            del self.locations[loc_id]
            print(f"Location with ID '{loc_id}' deleted.")
        self.save_locations()


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


if __name__ == "__main__":
    editor = LocationEditor("locations.txt")
    add_location = AddLocation(editor)
    add_location.run()
