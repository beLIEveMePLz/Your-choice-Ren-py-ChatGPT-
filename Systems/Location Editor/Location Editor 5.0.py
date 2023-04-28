import json
import os


VERSION = "5.0.0"


locations_path = os.path.join(os.getcwd(), "locations.txt")

print(f"Locations file path: {locations_path}")


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


class Cell:
    def __init__(self, cell_id, name, description="", type_=""):
        self.cell_id = cell_id
        self.name = name
        self.description = description or "Default description"
        self.type_ = type_
        self.connections = {}

    def add_connection(self, direction, target_id):
        self.connections[direction] = target_id

    def to_dict(self):
        return {
            "id": self.cell_id,
            "name": self.name,
            "description": self.description,
            "type": self.type_,
            "connections": self.connections
        }


class Location:
    def __init__(self, loc_id, name, description="", type_="", level="normal", cells=None):
        self.loc_id = loc_id
        self.name = name
        self.description = description or "Default description"
        self.type_ = type_
        self.level = level
        self.cells = cells or {}

    def to_dict(self):
        cells_dict = {cell_id: cell.to_dict() for cell_id, cell in self.cells.items()}
        return {
            "id": self.loc_id,
            "name": self.name,
            "description": self.description,
            "type": self.type_,
            "level": self.level,
            "cells": cells_dict
        }


class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "5.0.0"

    opposite_direction = {"north": "south", "south": "north", "east": "west", "west": "east"}

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
            self.locations = template

    def save_file(self):
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
        with open(self.file_path, "w") as file:
            json.dump(self.locations, file, indent=4)

    def delete_file(self):
        confirmation = input(f"Are you sure you want to delete the file at {self.file_path}? This action cannot be undone. (y/n): ")
        if confirmation.lower() == "y":
            os.remove(self.file_path)
            print(f"File {self.file_path} deleted.")
        else:
            print("File deletion canceled.")

    def update_location(self, location_id, changes):
        if location_id in self.locations:
            self.locations[location_id].update(changes)
            self.save_file()
        else:
            print(f"Location with ID {location_id} not found.")


    def check_id(self, obj_type):
        """
        Check the last used id for an object type and returns the next unique id.
        """
        if obj_type == "location":
            prefix = "loc"
        elif obj_type == "cell":
            prefix = "cell"
        else:
            raise ValueError(f"Unknown object type: {obj_type}")

        max_id = 0
        for loc in self.locations.values():
            for obj_id in loc[obj_type + "s"]:
                if obj_id.startswith(prefix):
                    try:
                        num = int(obj_id[len(prefix):])
                        if num > max_id:
                            max_id = num
                    except ValueError:
                        pass

        return prefix + str(max_id + 1)

    def create_location(self, name, num_cells_horizontal, num_cells_vertical):
        """
        Creates a new location template with the specified parameters.
        """
        loc_id = self.check_id("location")
        cells = {}

        # Create cells
        for i in range(num_cells_horizontal):
            for j in range(num_cells_vertical):
                cell_id = self.check_id("cell")
                cell_name = f"Cell {i}, {j}"
                cells[cell_id] = Cell(cell_id, cell_name)

                # Add connections between cells
                if i > 0:
                    cells[cell_id].add_connection("west", f"cell{i-1}_{j}")
                    cells[f"cell{i-1}_{j}"].add_connection("east", cell_id)
                if j > 0:
                    cells[cell_id].add_connection("north", f"cell{i}_{j-1}")
                    cells[f"cell{i}_{j-1}"].add_connection("south", cell_id)

        # Create location
        location = Location(loc_id, name, type_="", level="normal", cells=cells)
        self.locations[loc_id] = location.to_dict()

        return loc_id

    def edit_location(self, location_id):
        """
        Allows the user to edit the cells of a location.
        """
        # Get the location and its cells
        location_data = self.locations.get(location_id)
        if not location_data:
            print(f"Location with ID {location_id} not found.")
            return
        cells = location_data.get("cells")
        if not cells:
            print(f"No cells found for location with ID {location_id}.")
            return

        # Print the map and move the user to a cell
        print("Use arrow keys to navigate the map. Press 'e' to enter a cell and edit its properties.")
        current_cell = (0, 0)
        while True:
            self.draw_map(cells, current_cell)
            action = getch()
            if action == "e":
                # Enter cell edit mode
                print(f"Editing cell {current_cell}")
                cell_id = f"{current_cell[0]}_{current_cell[1]}"
                cell = cells.get(cell_id)
                if not cell:
                    print(f"Cell {cell_id} not found.")
                    continue
                while True:
                    print("Edit options:")
                    print("  1. Set name")
                    print("  2. Set description")
                    print("  3. Set type")
                    print("  4. Add connection")
                    print("  5. Remove connection")
                    print("  6. Delete cell")
                    print("   7. Exit cell edit mode")
                    choice = input("Select an option: ")
                    if choice == "1":
                        cell.name = input("Enter new name: ")
                    elif choice == "2":
                        cell.description = input("Enter new description: ")
                    elif choice == "3":
                        cell.type_ = input("Enter new type: ")
                    elif choice == "4":
                        direction = input("Enter direction (north, south, east, west): ")
                        target_cell = input("Enter target cell coordinates (e.g. '2_3'): ")
                        if direction not in ["north", "south", "east", "west"]:
                            print("Invalid direction.")
                            continue
                        if target_cell not in cells:
                            print(f"Target cell {target_cell} not found.")
                            continue
                        cell.add_connection(direction, target_cell)
                        target_cell_object = cells[target_cell]
                        target_cell_object.add_connection(self.opposite_direction[direction], cell_id)
                    elif choice == "5":
                        direction = input("Enter direction (north, south, east, west): ")
                        if direction not in ["north", "south", "east", "west"]:
                            print("Invalid direction.")
                            continue
                        if direction not in cell.connections:
                            print(f"No connection in direction {direction}.")
                            continue
                        target_cell = cell.connections[direction]
                        del cell.connections[direction]
                        target_cell_object = cells[target_cell]
                        del target_cell_object.connections[self.opposite_direction[direction]]
                    elif choice == "6":
                        del cells[cell_id]
                        for other_cell_id, other_cell in cells.items():
                            if cell_id in other_cell.connections.values():
                                direction = [k for k, v in other_cell.connections.items() if v == cell_id][0]
                                del other_cell.connections[direction]
                        print(f"Cell {cell_id} deleted.")
                        break
                    elif choice == "7":
                        break
                else:
                    print("Invalid choice.")
            elif action == "up":
                # Move up one row
                if current_cell[0] > 0:
                    current_cell = (current_cell[0] - 1, current_cell[1])
            elif action == "down":
                # Move down one row
                if current_cell[0] < self.map_height - 1:
                    current_cell = (current_cell[0] + 1, current_cell[1])
            elif action == "left":
                # Move left one column
                if current_cell[1] > 0:
                    current_cell = (current_cell[0], current_cell[1] - 1)
            elif action == "right":
                # Move right one column
                if current_cell[1] < self.map_width - 1:
                    current_cell = (current_cell[0], current_cell[1] + 1)
            else:
                print("Invalid action.")


    def draw_location_from_top(self, loc_id):
        """
        Draws a top-down view of the specified location using ASCII characters.
        """
        if loc_id not in self.locations:
            print(f"Location with ID {loc_id} not found.")
            return

        loc_data = self.locations[loc_id]
        cells = loc_data["cells"]
        num_cells_horizontal = loc_data["num_cells_horizontal"]
        num_cells_vertical = loc_data["num_cells_vertical"]

        for j in range(num_cells_vertical):
            # Draw top border of cells
            for i in range(num_cells_horizontal):
                cell = cells[f"{i}_{j}"]
                if j == 0:
                    print("+--" + "-".join(["+" for _ in range(num_cells_horizontal)]) + "--+")
                if i == 0:
                    print("|  ", end="")
                cell_char = "."
                if "north" not in cell["connections"]:
                    cell_char = "-"
                print(f"{cell_char}  ", end="")
                if i == num_cells_horizontal - 1:
                    print("|")
            # Draw middle border of cells
            for i in range(num_cells_horizontal):
                cell = cells[f"{i}_{j}"]
                if i == 0:
                    print("| ", end="")
                if "west" not in cell["connections"]:
                    print("| ", end="")
                else:
                    print("  ", end="")
                print("  ", end="")
                if "east" not in cell["connections"]:
                    print("|", end="")
                else:
                    print(" ", end="")
                if i == num_cells_horizontal - 1:
                    print("|")
            # Draw bottom border of cells
            for i in range(num_cells_horizontal):
                cell = cells[f"{i}_{j}"]
                if i == 0:
                    print("|  ", end="")
                cell_char = "."
                if "south" not in cell["connections"]:
                    cell_char = "-"
                print(f"{cell_char}  ", end="")
                if i == num_cells_horizontal - 1:
                    print("|")
        # Draw bottom border of entire location
        print("+--" + "-".join(["+" for _ in range(num_cells_horizontal)]) + "--+")

    def edit_cell(self):
        current_cell = self.location.get_cell(self.x, self.y)
        if current_cell:
            print(f"Editing cell {current_cell.name} ({current_cell.x}, {current_cell.y}):")
            print(f"1. Edit name ({current_cell.name})")
            print(f"2. Edit description ({current_cell.description})")
            print(f"3. Edit type ({current_cell.type})")
            print(f"4. Add connection")
            print(f"5. Remove connection")
            print(f"6. Delete cell")
            print(f"7. Back to location editor menu")

            choice = input("Enter your choice: ")
            if choice == "1":
                new_name = input("Enter new name: ")
                current_cell.name = new_name
            elif choice == "2":
                new_description = input("Enter new description: ")
                current_cell.description = new_description
            elif choice == "3":
                new_type = input("Enter new type: ")
                current_cell.type = new_type
            elif choice == "4":
                direction = input("Enter direction of connection (north, south, east, or west): ")
                cell_id = input("Enter ID of cell to connect to: ")
                current_cell.add_connection(direction, cell_id)
                self.location.get_cell(cell_id).add_connection(opposite_direction(direction), current_cell.id)
            elif choice == "5":
                direction = input("Enter direction of connection to remove (north, south, east, or west): ")
                current_cell.remove_connection(direction)
                opposite_dir = opposite_direction(direction)
                if current_cell.connections[opposite_dir]:
                    self.location.get_cell(current_cell.connections[opposite_dir]).remove_connection(opposite_dir)
            elif choice == "6":
                confirmation = input(f"Are you sure you want to delete cell {current_cell.name}? This action cannot be undone. (y/n): ")
                if confirmation.lower() == "y":
                    del self.location.cells[current_cell.id]
                    print(f"Cell {current_cell.name} deleted.")
                else:
                    print("Cell deletion canceled.")
            elif choice == "7":
                return
            else:
                print("Invalid choice.")
        else:
            print("Error: Current cell not found.")



    def delete_cell(self, cell_id):
        """Deletes a cell from the location."""
        cell = self.cells.get(cell_id)
        if cell:
            # Remove all connections to and from the cell
            for direction, connected_cell_id in cell.connections.items():
                connected_cell = self.cells.get(connected_cell_id)
                if connected_cell:
                    connected_cell.remove_connection(opposite_direction(direction))
            # Delete the cell
            del self.cells[cell_id]
            print(f"Cell {cell.name} deleted.")
        else:
            print("Cell not found.")
