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
    A class representing a cell in a location.
    """
    def __init__(self, cell_id, name, description, type_, gateways):
        self.cell_id = cell_id
        self.name = name
        self.description = description
        self.type = type_
        self.gateways = gateways

    def add_gateway(self, direction, target_cell):
        if direction in self.gateways:
            print("Gateway already exists.")
            return False
        self.gateways[direction] = target_cell.cell_id
        return True

    def edit_gateway(self, direction, target_cell):
        if direction not in self.gateways:
            print("Gateway not found.")
            return False
        self.gateways[direction] = target_cell.cell_id
        return True

    def delete_gateway(self, direction):
        if direction not in self.gateways:
            print("Gateway not found.")
            return False
        del self.gateways[direction]
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
