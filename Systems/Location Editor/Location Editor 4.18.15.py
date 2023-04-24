class LocationEditor:
    """
    A class for editing locations in a game.
    Attributes:
    - file_path (str): The path to the file containing the location data.
    - locations (dict): A nested dictionary of location data.
    """
    VERSION = "4.18.15"

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

    def create_location(self, name, description, type_, level, num_cells_horizontal, num_cells_vertical):
        """
        Creates a new location template with the specified parameters.
        """
        loc_id = str(uuid.uuid4())
        cells = {}

        # Create cells
        for i in range(num_cells_horizontal):
            for j in range(num_cells_vertical):
                cell_id = f"{i}_{j}"
                cell_name = f"Cell {i}, {j}"
                cell_description = ""
                cell_type = ""
                cells[cell_id] = Cell(cell_id, cell_name, cell_description, cell_type)

                # Add connections between cells
                if i > 0:
                    cells[cell_id].add_connection("west", f"{i-1}_{j}")
                    cells[f"{i-1}_{j}"].add_connection("east", cell_id)
                if j > 0:
                    cells[cell_id].add_connection("north", f"{i}_{j-1}")
                    cells[f"{i}_{j-1}"].add_connection("south", cell_id)

        # Create location
        location = Location(loc_id, name, description, type_, level, cells)
        self.locations[loc_id] = location.__dict__

        return loc_id
