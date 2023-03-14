import random

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Cell:
    def __init__(self, location, connections=None):
        self.location = location
        self.connections = connections or {"N": None, "S": None, "E": None, "W": None, "NE": None, "NW": None, "SE": None, "SW": None}
    
    def add_connection(self, direction, cell):
        self.connections[direction] = cell
        cell.connections[get_opposite_direction(direction)] = self
    
    def remove_connection(self, direction):
        cell = self.connections[direction]
        self.connections[direction] = None
        cell.connections[get_opposite_direction(direction)] = None
    
class ConnectionChecker:
    @staticmethod
    def is_valid_connection(cell1, cell2, direction):
        if not cell1 or not cell2:
            return False
        if direction == "N":
            return cell1.location.x == cell2.location.x and cell1.location.y == cell2.location.y - 1
        elif direction == "S":
            return cell1.location.x == cell2.location.x and cell1.location.y == cell2.location.y + 1
        elif direction == "E":
            return cell1.location.x == cell2.location.x + 1 and cell1.location.y == cell2.location.y
        elif direction == "W":
            return cell1.location.x == cell2.location.x - 1 and cell1.location.y == cell2.location.y
        elif direction == "NE":
            return cell1.location.x == cell2.location.x + 1 and cell1.location.y == cell2.location.y - 1
        elif direction == "NW":
            return cell1.location.x == cell2.location.x - 1 and cell1.location.y == cell2.location.y - 1
        elif direction == "SE":
            return cell1.location.x == cell2.location.x + 1 and cell1.location.y == cell2.location.y + 1
        elif direction == "SW":
            return cell1.location.x == cell2.location.x - 1 and cell1.location.y == cell2.location.y + 1
        return False

class CellCreator:
    @staticmethod
    def create_cell(location):
        return Cell(location)

class Automator:
    @staticmethod
    def add_cell(direction, current_cell, cells):
        if current_cell.connections[direction]:
            print("Connection already exists in that direction.")
            return
        location = None
        if direction == "N":
            location = Location(current_cell.location.name, current_cell.location.description)
            location.y -= 1
        elif direction == "S":
            location = Location(current_cell.location.name, current_cell.location.description)
            location.y += 1
        elif direction == "E":
            location = Location(current_cell.location.name, current_cell.location.description)
            location.x += 1
        elif direction == "W":
            location = Location(current_cell.location.name, current_cell.location.description)
            location.x -= 1
        elif direction == "NE":
            location = Location(current_cell.location.name, current_cell.location.description)
            location.x += 1
            location.y -= 1
        elif direction == "NW":
            location = Location(current_cell.location.name, current_cell.location.description)
            location.x -= 1
            location.y -= 1
        elif direction == "SE":
            location = Location(current_cell.location.name, current_cell.location.description)
           
