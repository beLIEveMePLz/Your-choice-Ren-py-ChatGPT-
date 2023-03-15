from collections import defaultdict

class LocationMap:
    def __init__(self, locations):
        self.locations = locations
        self.graph = defaultdict(list)
        self.visited = set()

        self.build_graph()

    def build_graph(self):
        for loc_id, loc_data in self.locations.items():
            for conn_id, conn_data in loc_data['connections'].items():
                if conn_id not in self.graph[loc_id]:
                    self.graph[loc_id].append(conn_id)
                    self.graph[conn_id].append(loc_id)

    def traverse_map(self):
        maps = []

        for loc_id in self.locations.keys():
            if loc_id not in self.visited:
                maps.append(self.traverse(loc_id))

        return maps

    def traverse(self, loc_id):
        self.visited.add(loc_id)
        loc_data = self.locations[loc_id]
        rows, cols = loc_data['size']
        map_rows = ['.' * (cols * 4 + 1)]

        for row in range(rows):
            map_row = ['|']

            for col in range(cols):
                if row == 0 and 'north' in loc_data['cells'][row][col].walls:
                    map_row.append('---')
                else:
                    map_row.append('   ')

                if col == cols - 1:
                    map_row.append('|')
                elif 'east' in loc_data['cells'][row][col].walls:
                    map_row.append('|')
                else:
                    map_row.append(' ')

            map_rows.append(''.join(map_row))
            map_row = ['|']

            for col in range(cols):
                if row == rows - 1 and 'south' in loc_data['cells'][row][col].walls:
                    map_row.append('---')
                else:
                    map_row.append('   ')

                if col == cols - 1:
                    map_row.append('|')
                else:
                    map_row.append(' ')

            map_rows.append(''.join(map_row))

        map_rows.append('.' * (cols * 4 + 1))

        for conn_id in self.graph[loc_id]:
            if conn_id not in self.visited:
                map_rows += self.traverse(conn_id)

        return map_rows
