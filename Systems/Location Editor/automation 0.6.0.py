import msvcrt  # for Windows keyboard input

class LocationEditor:
    def __init__(self, location):
        self.location = location

    # ... methods for location editing and validation ...

    def add_cell_automation(self, name='default_name', description='default_description'):
        # Get location size
        size = self.get_location_size()
        if size is None:
            print('Error: location size could not be determined.')
            return

        # Initialize current position to center of location
        current_pos = [size[0]//2, size[1]//2]

        # Loop until 'q' key is pressed
        while True:
            # Display current map
            self.show_location_map()

            # Get direction from arrow keys
            direction = self.get_direction()

            # Calculate new position
            new_pos = [current_pos[0], current_pos[1]]
            if direction == 'up':
                new_pos[0] -= 1
            elif direction == 'down':
                new_pos[0] += 1
            elif direction == 'left':
                new_pos[1] -= 1
            elif direction == 'right':
                new_pos[1] += 1

            # Check if new position is valid
            if not self.is_position_valid(new_pos):
                print('Error: invalid position.')
                continue

            # Create new cell at new position
            self.location[current_pos[0]][current_pos[1]].add_connection(direction, name, description)
            self.location[new_pos[0]][new_pos[1]] = Cell()
            self.location[new_pos[0]][new_pos[1]].add_connection(self.opposite_direction(direction), name, description)

            # Update current position
            current_pos = new_pos

            # Prompt user to continue or quit
            print('Press any arrow key to continue adding cells or "q" to quit.')
            key = msvcrt.getch().decode('utf-8')
            if key == 'q':
                break

        # Final map display
        self.show_location_map()
