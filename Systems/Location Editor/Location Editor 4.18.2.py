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
    A class to check if a connection is valid and connected to the next cell.
    """
    def __init__(self, location_data):
        self.location_data = location_data

    def is_valid_direction(self, direction):
        if direction not in ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]:
            print("Invalid direction.")
            return False
        return True

    def is_valid_connection(self, current_cell, direction, next_cell):
        if current_cell.cell_id in next_cell.gateways.values():
            print("Connection already exists.")
            return False
        if next_cell.cell_id in current_cell.gateways.values():
            print("Connection already exists.")
            return False
        if not self.is_valid_direction(direction):
            return False
        if direction not in next_cell.gateways:
            print("Connection is not valid.")
            return False
        if next_cell.gateways[direction] != current_cell.cell_id:
            print("Connection is not valid.")
            return False
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
