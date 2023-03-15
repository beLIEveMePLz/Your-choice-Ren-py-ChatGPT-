import sys

class Template:
    def validate_data(self, data):
        raise NotImplementedError

class LocationTemplate(Template):
    def validate_data(self, data):
        if len(data) != 2:
            raise ValueError("Location data must contain 2 integers")
        try:
            rows, cols = map(int, data)
            if rows <= 0 or cols <= 0:
                raise ValueError("Rows and cols must be positive integers")
        except ValueError:
            raise ValueError("Invalid location data, must contain positive integers")

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.connections = {"N": None, "S": None, "W": None, "E": None}

class Location:
    def __init__(self, rows, cols):
        self.cells = {}
        for row in range(1, rows+1):
            for col in range(1, cols+1):
                self.cells[(row, col)] = Cell(row, col)

    def get_cell(self, row, col):
        return self.cells.get((row, col))

class ConnectionChecker:
    def __init__(self, location):
        self.location = location

    def check_connection(self, cell, direction):
        row = cell.row
        col = cell.col
        if direction == "N":
            return self.location.get_cell(row-1, col)
        elif direction == "S":
            return self.location.get_cell(row+1, col)
        elif direction == "W":
            return self.location.get_cell(row, col-1)
        elif direction == "E":
            return self.location.get_cell(row, col+1)

class LocationEditor:
    def __init__(self, template):
        self.template = template

    def edit_location(self):
        while True:
            data = input("Enter location data (rows, cols): ")
            try:
                self.template.validate_data(data.split())
                rows, cols = map(int, data.split())
                break
            except ValueError as e:
                print(str(e))
                continue

        location = Location(rows, cols)
        connection_checker = ConnectionChecker(location)
        self.print_location(location)

        while True:
            choice = input("Do you want to add a cell? (y/n): ")
            if choice.lower() != "y":
                break

            current_row, current_col = map(int, input("Enter current cell location (row, col): ").split())
            direction = self.get_direction()

            if direction not in ["N", "S", "W", "E"]:
                print("Invalid direction")
                continue

            existing_cell = connection_checker.check_connection(location.get_cell(current_row, current_col), direction)

            if existing_cell is None:
                new_cell = Cell(current_row, current_col)
                location.cells[(current_row, current_col)].connections[direction] = new_cell
                if direction == "N":
                    new_cell.connections["S"] = location.get_cell(current_row-1, current_col)
                elif direction == "S":
                    new_cell.connections["N"] = location.get_cell(current_row+1, current_col)
                elif direction == "W":
                    new_cell.connections["E"] = location.get_cell(current_row, current_col-1)
                elif direction == "E":
                    new_cell.connections["W"] = location.get_cell(current_row, current_col+1)
                self.print_location(location)
            else:
                print("Cell already exists in that direction")

    def get_direction(self):
        while True:
            direction = input("Enter direction to add cell (N/S/W/E): ")
           
