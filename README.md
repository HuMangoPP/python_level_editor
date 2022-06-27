# Tiled Pixel Art Level Editor

## A tile-based pixel art level editor made using python and pygame

This program uses a tile atlas and allows you to place tiles according to the tile atlas.

Upon exit, this program will save a .json file containing tile information (index within tile atlas and boolean value storing the collision state of the tile).

The program will also save a .png file based on the inputted size containing the created level.

This program **does not** support multiple layers. This feature may be coming soon.

### Instructions:

1. Ensure python and pygame are installed. Use links [python](https://www.python.org/) and [pygame](https://www.pygame.org/wiki/GettingStarted) for installation guides
2. Download and unzip the repository
3. Relocated level_editor.py to the game directory
4. Open the terminal and use ```python level_editor.py``` or ```python3 level_editor.py``` to run the file
5. Follow instructions to set the path for the tile atlas, the path for the .json file to be loaded from and saved to, and the path of the .png file to be saved to
6. Input the tile size of the atlas and the tile size of the game window and .png out file
7. Input the dimensions of the level based on the number of tiles (width and height)
8. Begin designing!

### Notes:

1. Use WASD keys to move the anchor for the canvas in cases where the image is larger than the pygame window
2. Use the SPACE key to toggle the collision state on or off (a red outline on the tile will indicate this state)
3. Use the left mouse button to place a tile and the right mouse button to remove a tile
4. Use the mouse wheel to switch between tiles in the atlas
5. If there is no .json file, the program will create one
6. If no .json file or no .png file is specified, the program will create new_map.json and new_map.png in root directory
7. This program is **not** exclusive to python. Any graphics library supporting .png files and languages supporting .json files can easily use this editor
