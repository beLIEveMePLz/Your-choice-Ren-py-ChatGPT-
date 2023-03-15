import msvcrt # this module allows us to get input from the keyboard without waiting for a newline character

class CellCreator:
    def __init__(self, location):
        self.location = location
        self.current_cell = None
        self.directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        self.current_position = (0, 0) # starting position
        self.cells_created = 0

    def create_cells(self):
        self.current_cell = Cell() # initialize current cell
        self.current_cell.add_connection("up", None) # set the connections to None for now
        self.current_cell.add_connection("down", None)
        self.current_cell.add_connection("left", None)
        self.current_cell.add_connection("right", None)
        self.current_position = (0, 0) # reset the starting position
        self.cells_created = 0 # reset the cell count
        while self.cells_created < self.location.num_cells:
            self.display_map() # display the map with the current cell highlighted
            direction = self.get_direction() # get the direction from the user
            if direction in self.directions:
                new_position = (self.current_position[0] + self.directions[direction][0], self.current_position[1] + self.directions[direction][1])
                if self.valid_position(new_position):
                    self.create_cell_at_position(new_position) # create the new cell
            elif direction == "q":
                break
        print("Done creating cells.")

    def create_cell_at_position(self, position):
        # create the new cell and set its connections to None for now
        new_cell = Cell()
        new_cell.add_connection("up", None)
        new_cell.add_connection("down", None)
        new_cell.add_connection("left", None)
        new_cell.add_connection("right", None)

        # connect the cells
        if self.current_position[0] < position[0]:
            self.current_cell.set_connection("down", new_cell)
            new_cell.set_connection("up", self.current_cell)
        elif self.current_position[0] > position[0]:
            self.current_cell.set_connection("up", new_cell)
            new_cell.set_connection("down", self.current_cell)
        elif self.current_position[1] < position[1]:
            self.current_cell.set_connection("right", new_cell)
            new_cell.set_connection("left", self.current_cell)
        elif self.current_position[1] > position[1]:
            self.current_cell.set_connection("left", new_cell)
            new_cell.set_connection("right", self.current_cell)

        # update the current cell and position
        self.current_cell = new_cell
        self.current_position = position
        self.cells_created += 1

    def valid_position(self, position):
        # check if the position is within the bounds of the location
        return position[0] >= 0 and position[0] < self.location.num_rows and position[1] >= 0 and position[1] < self.location.num_cols

    def get_direction(self):
        # get input from the keyboard without waiting for a newline character
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode("utf-8")
                if key == "\r": # the user pressed the enter key
                    continue
                elif key in self.directions or key == "q":
                    return key

    def
