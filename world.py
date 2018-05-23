import json
import sys

import tiles

_world = {}
starting_position = (0, 0)


def tile(x, y):
    return _world.get((x, y))


class WorldLoader:
    """Loads a location from a JSON file"""
    def load_locations(self):
        with open('locations/sewers.json') as f:
            data = json.load(f)
        # TODO is valid json
        size_x = data['size_x']
        size_y = data['size_y']
        print(f"Generating World {size_x} by {size_y}")
        self.populate_with_empty_tiles(size_x, size_y)

        for room in data['tiles']:
            try:
                x, y = room['coordinate_x'], room['coordinate_y']
                tile_type = room['tile_type']
                tile_content = room[tile_type] if tile_type in room else None
                intro_text = room['intro_text']
                print(f"Populating tile {x,y} with {tile_type}. Intro text: {intro_text}")
                _world[(x, y)] = self.create_tile(intro_text, tile_content, tile_type, x, y)
            except KeyError as e:
                print(e)
            except BaseException as e:
                print("Oh My Goodness! An exception: ", e)

    def create_tile(self, intro_text, tile_content, tile_type, x, y):
        """Creates a tile based on the information supplied inside JSON"""
        if tile_type.startswith("Exit"):
            generated_object = tiles.ExitRoom(x, y, intro_text=intro_text)
        elif tile_type.startswith("Start"):
            generated_object = tiles.StartingRoom(x, y, intro_text=intro_text)
        elif tile_type == "Enemy":
            content = self.string_to_class('enemies', tile_type)(**tile_content)
            generated_object = tiles.GenerateEnemyRoom(x, y, content, intro_text=intro_text)
        elif tile_type in {"Weapon", "Gold"}:
            content = self.string_to_class('items', tile_type)(**tile_content)
            generated_object = tiles.GenerateLootRoom(x, y, content, intro_text=intro_text)
        else:
            generated_object = tiles.GenerateEmptyRoom(x, y)
        return generated_object

    @staticmethod
    def populate_with_empty_tiles(size_x, size_y):
        for x in range(size_x):
            for y in range(size_y):
                _world[(x, y)] = tiles.GenerateEmptyRoom(x, y)

    @staticmethod
    def string_to_class(namespace, class_name):
        return getattr(sys.modules[namespace], class_name)


if __name__ == '__main__':
    wl = WorldLoader()
    wl.load_locations()
    print(_world)
