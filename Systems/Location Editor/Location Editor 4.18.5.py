import json
import os


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
                    "connections": {}
                }
            }
        }
        return template
      
      
class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "4.18.5"

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
            
            
class Cell:
    """
    A class representing a cell within a location in a game.
    """
    def __init__(self, cell_id, name, description, cell_type):
        self.cell_id = cell_id
        self.name = name
        self.description = description
        self.cell_type = cell_type
        self.connections = {}

    def add_connection(self, direction, cell_id):
        if direction in self.connections:
            print(f"Connection already exists in direction {direction}.")
        else:
            self.connections[direction] = cell_id

    def edit_connection(self, direction, new_cell_id):
        if direction not in self.connections:
            print(f"No connection exists in direction {direction}.")
        else:
            old_cell_id = self.connections[direction]
            del self.connections[direction]
            if old_cell_id != new_cell_id:
                self.add_connection(direction, new_cell_id)
                return old_cell_id

    def delete_connection(self, direction):
        if direction not in self.connections:
            print(f"No connection exists in direction {direction}.")
        else:
            cell_id = self.connections[direction]
            del self.connections[direction]
            return cell_id
          
          
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
        
        
class Connection:
    """
    A class representing a connection between two cells in a location.
    """
    def __init__(self, destination_cell_id, is_open=True):
        self.destination_cell_id = destination_cell_id
        self.is_open = is_open

        
class ConnectionChecker:
    """
    A class that checks connections between cells in a location.
    """
    def __init__(self, location):
        self.location = location
    
    def check_connection(self, cell_id, direction):
        """
        Checks if a connection in a given direction from a cell is valid.
        Returns True if the connection is valid, False otherwise.
        """
        cell = self.location.cells[cell_id]
        # Check if the given direction is valid for the cell
        if direction not in cell.directions:
            print(f"Invalid direction '{direction}' for cell '{cell_id}'")
            return False
        # Check if the cell is already connected in the given direction
        if direction in cell.connections:
            print(f"Cell '{cell_id}' is already connected in direction '{direction}'")
            return False
        # Check if the destination cell exists in the location
        destination_cell_id = cell.directions[direction]
        if destination_cell_id not in self.location.cells:
            print(f"Cell '{destination_cell_id}' not found in location")
            return False
        # Check if the destination cell has a connection back to the current cell
        destination_cell = self.location.cells[destination_cell_id]
        if cell_id not in destination_cell.connections:
            print(f"Cell '{destination_cell_id}' is not connected back to cell '{cell_id}'")
            return False
        # Check if the connection is open
        connection = destination_cell.connections[cell_id]
        if not connection.is_open:
            print(f"Connection to cell '{destination_cell_id}' in direction '{direction}' is closed")
            return False
        return True
