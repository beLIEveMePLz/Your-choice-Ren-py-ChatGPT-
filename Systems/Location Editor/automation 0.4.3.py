class LocationBuilder:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.location = self.create_location()

    def create_location(self):
        location = {}
        for r in range(self.rows):
            row = {}
            for c in range(self.cols):
                row[c] = Cell()
            location[r] = row
        return location
