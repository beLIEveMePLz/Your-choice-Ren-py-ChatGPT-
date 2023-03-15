class LocationMap:
    def __init__(self, locations):
        self.locations = locations
        self.map = ""
        
    def create_map(self):
        for loc_name, location in self.locations.items():
            # Add location name to map
            self.map += f"{loc_name.upper()}:\n"
            
            # Add cells to map
            rows, cols = location.get_size()
            for row in range(rows):
                row_str = ""
                for col in range(cols):
                    if location.has_cell(row, col):
                        # Check for connections to other locations
                        connected_locs = location.get_connected_locations(row, col)
                        if "up" in connected_locs:
                            row_str += "| x "
                        else:
                            row_str += "|   "
                        if "left" in connected_locs:
                            row_str += "x"
                        else:
                            row_str += " "
                        row_str += " "
                    else:
                        row_str += "+---"
                # Add closing vertical line to row
                row_str += "|\n"
                # Add row to map
                self.map += row_str
            # Add closing horizontal line to map
            self.map += "+---" * cols + "+\n"
        
        return self.map
