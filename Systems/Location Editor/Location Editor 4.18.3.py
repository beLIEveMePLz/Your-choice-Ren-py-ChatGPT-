import json
import os

class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "4.18"

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
        confirmation = input(f"Are you sure you want to delete the file at {self.file_path}? This action cannot be undone. (y/n): ")
        if confirmation.lower() == "y":
            os.remove(self.file_path)
            print(f"File {self.file_path} deleted.")
        else:
            print("File deletion canceled.")

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
                    "gateways": {}
                }
            }
        }
        return template

class Cell:
    """
    A class representing a cell within a location.
    """
    def __init__(self, name="", description="", type_="", connections=None):
        self.name = name
        self.description = description
        self.type = type_
        self.connections = connections or {}

    def add_connection(self, direction, cell_id):
        if direction in self.connections:
            print(f"A connection already exists in direction {direction}.")
            return False
        else:
            self.connections[direction] = cell_id
            return True

    def edit_connection(self, direction, new_cell_id):
        if direction not in self.connections:
            print(f"No connection exists in direction {direction}.")
            return False
        else:
            self.connections[direction] = new_cell_id
            return True

    def delete_connection(self, direction):
        if direction not in self.connections:
            print(f"No connection exists in direction {direction}.")
            return False
        else:
            del self.connections[direction]
            return True

          
class ConnectionChecker:
    """
    A class for checking connections between two cells in a location.
    """
    def __init__(self, location):
        self.location = location

    def check_connection(self, cell1, direction, cell2):
        """
        Checks whether a connection between cell1 and cell2 in the given direction is valid.
        Returns True if the connection is valid, and False otherwise.
        """
        if direction not in cell1.connections:
            print(f"No connection exists in direction {direction} for cell {cell1.name}.")
            return False
        elif cell1.connections[direction] != cell2.name:
            print(f"Cell {cell2.name} is not connected in direction {direction} from cell {cell1.name}.")
            return False
        elif direction not in cell2.connections or cell2.connections[direction] != cell1.name:
            print(f"Cell {cell1.name} is not connected in direction {direction} to cell {cell2.name}.")
            return False
        else:
            return True

class Location:
    """
    A class representing a location in a game.
    """
    def __init__(self, loc_id, name, description, type_, level, cells):
        self.loc_id = loc_id
        self.name = name
        self.description = description
        self.type = type_
        self.level = level
        self.cells = cells
