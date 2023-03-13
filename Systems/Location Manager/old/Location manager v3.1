

import os

# Define the name of the file to store the locations
LOCATIONS_FILE = 'locations.txt'

# Define the function for adding a cell to an existing location
def add_cell_to_location():
    # Ask the user to input the ID of the location to add the cell to
    location_id = input("Enter the ID of the location to add the cell to: ")
    
    # Check if the locations file already exists
    if os.path.isfile(LOCATIONS_FILE):
        # If the file exists, read its contents into a dictionary
        with open(LOCATIONS_FILE, 'r') as f:
            locations = eval(f.read())
            
        # Check if the location ID exists in the dictionary
        if location_id in locations:
            # If the ID exists, ask the user to input the name of the new cell
            cell_name = input("Enter the name of the new cell: ")
            
            # Determine the ID number for the new cell by counting the existing cells
            cell_id_count = len(locations[location_id]["cells"]) + 1
            cell_id = f"{location_id}cell{cell_id_count}"
            
            # Create a dictionary to hold the directions for the new cell
            directions = {}
            for dir_name in ['north', 'south', 'east', 'west', 'northeast', 'northwest', 'southeast', 'southwest']:
                print("""*NW * N * NE*
                    * W * o * E *
                    *SW * S * SE*""")
                dir_id = input(f"Enter ID for {dir_name} direction: ")
                directions[dir_name] = dir_id
                
            # Add the new cell to the dictionary of cells for the location
            locations[location_id]["cells"][cell_id] = {
                "cell_name": cell_name,
                "directions": directions
            }
            
            # Write the updated locations dictionary to the file
            with open(LOCATIONS_FILE, 'w') as f:
                f.write(str(locations))
            
            # Print a message to confirm that the cell was added
            print(f"Cell {cell_id} added to location {location_id} successfully!")
        else:
            # If the ID does not exist, print an error message
            print(f"Location {location_id} does not exist!")
    else:
        # If the file does not exist, print an error message
        print("Error: locations file does not exist!")



while True:
    print("Select an option:")
    print("1. Add a new location")
    print("2. Edit an existing location")
    print("3. Delete an existing location")
    print("4. Add a cell to an existing location")
    print("5. Quit")
    
    option = input("Enter your choice (1-5): ")
    
    if option == "1":
        add_location()
    elif option == "2":
        edit_location()
    elif option == "3":
        delete_location()
    elif option == "4":
        add_cell_to_location()
    elif option == "5":
        break
    else:
        print("Invalid option!")
