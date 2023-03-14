import json
from typing import Dict, Any

class AddLocation:
    def __init__(self, cells: Dict[int, Dict[str, Any]]) -> None:
        self.cells = cells

    def run(self) -> Dict[str, Any]:
        loc_id = max(self.cells.keys()) + 1 if self.cells else 1
        name = input("Enter location name: ")
        description = input("Enter location description: ")
        location_type = input("Enter location type from the following list [city, forest, desert, ocean]: ")
        level = int(input("Enter location level: "))
        location = {
            "loc_id": loc_id,
            "name": name,
            "description": description,
            "type": location_type,
            "level": level,
            "cells": []
        }
        self.cells[loc_id] = location
        return location

class FirstLocation:
    """
    A class for managing the first location in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - cells (dict): A dictionary of cell data.
    """
    VERSION = "0.2"

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.cells = {}
        self.load_cells()

    def load_cells(self) -> None:
        try:
            with open(self.file_path, "r") as file:
                self.cells = json.load(file)
        except FileNotFoundError:
            print("Location file not found.")
            pass

        if not self.cells:
            print("Creating template file...")
            self.cells = {
                1: {
                    "loc_id": 1,
                    "name": "First Location",
                    "description": "This is the first location.",
                    "type": "city",
                    "level": 1,
                    "cells": []
                }
            }
            self.save_cells()

    def save_cells(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump(self.cells, file, indent=4)

    def run(self) -> None:
        add_location = AddLocation(self.cells)
        location = add_location.run()
        self.save_cells()
        print(f"Location {location['name']} added to file.")


if __name__ == "__main__":
    LOCATION_FILE = "locations.json"
    first_location = FirstLocation(LOCATION_FILE)
    first_location.run()
