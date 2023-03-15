class LocationEditor:
    def __init__(self):
        self.locations = {}

    def create_location(self, name, description):
        if name not in self.locations:
            self.locations[name] = {'description': description, 'cells': {(0, 0): Cell()}}

    def create_cell(self, location, position):
        if location in self.locations:
            cells = self.locations[location]['cells']
            if position in cells:
                print("A cell already exists at this position.")
            else:
                cells[position] = Cell()
        else:
            print("Location not found.")

    def print_location_map(self, location):
        if location in self.locations:
            cells = self.locations[location]['cells']
            max_x = max(cells, key=lambda c: c[0])[0]
            min_x = min(cells, key=lambda c: c[0])[0]
            max_y = max(cells, key=lambda c: c[1])[1]
            min_y = min(cells, key=lambda c: c[1])[1]

            for y in range(min_y, max_y + 1):
                row = ''
                for x in range(min_x, max_x + 1):
                    if (x, y) in cells:
                        cell = cells[(x, y)]
                        row += cell.get_representation()
                    else:
                        row += '.'
                print(row)

    def automate_add_cells(self, location):
        print("Use arrow keys to add cells. Press 'q' to stop.")
        current_position = (0, 0)
        while True:
            self.print_location_map(location)
            print("Current position:", current_position)
            direction = input("Enter direction (up, down, left, right) or 'q' to stop: ")
            if direction == 'q':
                break
            elif direction == 'up':
                new_position = (current_position[0], current_position[1] - 1)
            elif direction == 'down':
                new_position = (current_position[0], current_position[1] + 1)
            elif direction == 'left':
                new_position = (current_position[0] - 1, current_position[1])
            elif direction == 'right':
                new_position = (current_position[0] + 1, current_position[1])
            else:
                print("Invalid direction.")
                continue

            self.create_cell(location, new_position)
            current_position = new_position
