import json
import os


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
    VERSION = "4.18.5"

    def __init__(self, file_path):
        self.file_path = file_path
        self.locations = {}
        self.load_file()

    def load_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.locations = json.load(file)
