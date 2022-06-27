import pygame,sys,math
import json

atlas_tilesize = 16 # the size of tiles inside the atlas
local_tilesize = 64 # the size of tiles displayed on the screen
local_width, local_height = 1500,720 # the size of the pygame window and save image surface

level = {}

def load_tile_atlas(tile_atlas):
    width = int(tile_atlas.get_width()//atlas_tilesize)
    height = int(tile_atlas.get_height()//atlas_tilesize)
    atlas = {}
    for x in range(width):
        for y in range(height):
            # blit each tile onto a tile surface and put it inside of the atlas dictionary
            # each key corresponding tile in the atlas
            tile = pygame.Surface((atlas_tilesize,atlas_tilesize))
            tile.blit(tile_atlas,(0,0),(x*atlas_tilesize,y*atlas_tilesize,atlas_tilesize,atlas_tilesize))
            tile = pygame.transform.scale(tile,(local_tilesize,local_tilesize))
            atlas[x+width*y] = tile
    return atlas

pygame.init()
pygame.display.set_caption("level editor")
display_surface = pygame.display.set_mode((local_width,local_height))
clock = pygame.time.Clock()

# take inputs
tile_name = input('Path to tile atlas: ')
# save files default to new_map
save_file = input('Path to .json save file: ')  or 'new_map.json'
image_save = input('Path to .png save file: ') or 'new_map.png'
atlas_tilesize = int(input('Tile size of tile atlas: '))
local_tilesize = int(input('Tile size of the level: '))
image_width = int(input('Image width (# of tiles): ')) * local_tilesize
image_height = int(input('Image height (# of tiles): ')) * local_tilesize
image_surface = pygame.Surface((image_width,image_height))

# create the tile atlas dictionary and get the current tile (index 0)
tile_img = pygame.image.load(tile_name)
tiles = load_tile_atlas(tile_img)
current_index = 0
current_img = tiles[current_index]
toggle_obstacle = False

# get the save data from .json file
with open(save_file, 'a+') as json_file:
    try:
        level = json.load(json_file)
    except json.JSONDecodeError:
        pass
# move the anchor position for scrolling (if the image res is larger than the window res)
def move_anchor(x, y):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and x>0:
        x-=1
    elif keys[pygame.K_d]:
        x+=1
    
    if keys[pygame.K_w] and y>0:
        y-=1
    elif keys[pygame.K_s]:
        y+=1
    
    return x, y

anchor_x = 0
anchor_y = 0

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # upon game close, save the .json file and .png file
            with open(save_file,'w') as outfile:
                json.dump(level,outfile)
            pygame.image.save(image_surface, image_save)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                # upon game close, save the .json file and .png file
                with open(save_file,'w') as outfile:
                    json.dump(level,outfile)
                pygame.image.save(image_surface, image_save)
                pygame.quit()
                sys.exit()
            if event.key==pygame.K_DELETE:
                level.clear()
            if event.key==pygame.K_SPACE:
                toggle_obstacle = not toggle_obstacle
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                current_index-=1
            elif event.button == 5:
                current_index+=1
            current_index%=len(tiles)
            current_img = tiles[current_index]
    # change the anchor based on user input with wasd
    anchor_x, anchor_y = move_anchor(anchor_x,anchor_y)

    # check if user wants to delete or add new tile to the map
    if pygame.mouse.get_pressed(3)[0] or pygame.mouse.get_pressed(3)[2]:
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1] 
        if mx<1000:
            row = int(math.floor(my/local_tilesize))+anchor_y
            col = int(math.floor(mx/local_tilesize))+anchor_x
            if str(row) in level:
                col_tiles = level[str(row)]
            else:
                col_tiles = {}
            if pygame.mouse.get_pressed(3)[0]:
                # saves the image index based on the atlas and if the tile is an obstacle
                col_tiles[str(col)] = [current_index, toggle_obstacle]
            elif pygame.mouse.get_pressed(3)[2] and str(col) in col_tiles:
                del col_tiles[str(col)]
            
            level[str(row)] = col_tiles

    display_surface.fill('black')
    image_surface.fill('black')

    # draw everything to the display_surface
    # draw tile information to image_surface but no debug information
    for row in level:
        for col in level[str(row)]:
            img = tiles[level[str(row)][str(col)][0]]
            x = int(col)*local_tilesize
            y = int(row)*local_tilesize
            image_surface.blit(img,(x,y))
            x -= anchor_x*local_tilesize
            y -= anchor_y*local_tilesize
            display_surface.blit(img,(x,y))
    
    mx, my = pygame.mouse.get_pos()
    display_surface.blit(current_img, (mx-current_img.get_width()/2,my-current_img.get_height()/2))
    pygame.draw.rect(display_surface,
                    'red',
                    (mx-current_img.get_width()/2,
                    my-current_img.get_height()/2,
                    current_img.get_width(),
                    current_img.get_height()),
                    3) if toggle_obstacle else None

    # display the atlas on the right
    display_surface.blit(tile_img, (1000,0))
    tile_x = current_index%(tile_img.get_width()//atlas_tilesize)
    tile_y = current_index//(tile_img.get_width()//atlas_tilesize)
    pygame.draw.rect(display_surface,'white',(tile_x*atlas_tilesize+1000,tile_y*atlas_tilesize,atlas_tilesize,atlas_tilesize),3)
    pygame.display.update()
    clock.tick(60)
    

