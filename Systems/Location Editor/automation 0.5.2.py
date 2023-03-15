class Cell:
    def __init__(self, name: str, description: str, x: int, y: int):
        self.name = name
        self.description = description
        self.connections = {'north': None, 'south': None, 'east': None, 'west': None}
        self.x = x
        self.y = y

    def get_direction(self, key):
        """
        Returns the direction of the key press (up, down, left, right)
        """
        if key == 'w':
            return 'north'
        elif key == 's':
            return 'south'
        elif key == 'd':
            return 'east'
        elif key == 'a':
            return 'west'
        else:
            return None
