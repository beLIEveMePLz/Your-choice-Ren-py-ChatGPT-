import curses

class LocationEditor:
    def __init__(self, location_dict):
        self.location_dict = location_dict
        self.current_cell = None
        self.direction = None
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.screen.keypad(True)
        self.screen.clear()
        self.draw_location()

    def draw_location(self):
        # code to draw the location in ascii art

    def add_cell(self):
        # code to add a new cell to the location dictionary

    def validate_cell(self, cell):
        # code to validate that a cell can be added to the location dictionary

    def run(self):
        while True:
            key = self.screen.getch()
            if key == curses.KEY_UP:
                self.direction = "north"
            elif key == curses.KEY_DOWN:
                self.direction = "south"
            elif key == curses.KEY_LEFT:
                self.direction = "west"
            elif key == curses.KEY_RIGHT:
                self.direction = "east"
            elif key == ord("a"):
                if self.direction and self.current_cell:
                    new_cell = Cell()
                    if self.validate_cell(new_cell):
                        self.add_cell()
                        self.draw_location()
            elif key == ord("q"):
                break

        curses.endwin()

if __name__ == "__main__":
    location_dict = {} # initialize the location dictionary
    editor = LocationEditor(location_dict)
    editor.run()
