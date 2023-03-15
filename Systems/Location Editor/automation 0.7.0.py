import keyboard
import time

class CellCreator:
    def __init__(self, location):
        self.location = location
        self.current_cell = None
        self.previous_cell = None

    def create_cell(self):
        while True:
            direction = self.get_direction()
            if direction == "STOP":
                break
            new_cell = self.create_new_cell(direction)
            if new_cell:
                self.previous_cell = self.current_cell
                self.current_cell = new_cell
                self.location.add_cell(new_cell)

    def get_direction(self):
        direction = "STOP"
        while True:
            if keyboard.is_pressed("up"):
                direction = "NORTH"
                break
            elif keyboard.is_pressed("down"):
                direction = "SOUTH"
                break
            elif keyboard.is_pressed("left"):
                direction = "WEST"
                break
            elif keyboard.is_pressed("right"):
                direction = "EAST"
                break
            if keyboard.is_pressed("esc"):
                direction = "STOP"
                break
            time.sleep(0.1)
        return direction

    def create_new_cell(self, direction):
        if self.current_cell:
            new_cell = self.current_cell.add_neighbor(direction)
        else:
            new_cell = self.location.create_cell()
        return new_cell
