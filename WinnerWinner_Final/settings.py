import pygame as pg
vec = pg.math.Vector2

# -- Colours (R, G, B) --
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
SILVER = (211, 211, 211)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
ORANGE = (255,100,10)
BLUEGREEN = (0,255,170)
MARROON = (115,0,0)
LIME = (180,255,100)
PRINT = (255,100,180)           # PINK AF  
PURPLE = (240,0,255)  
GREY = (127,127,127)
NICEGREY = (69,69,69)
MAGENTA = (255,0,230)
BROWN = (100,40,0)
FORESTGREEN = (0,50,0)
NAVYBLUE = (0,0,100)
RUST = (210,150,75)             # GOLD AF
BRIGHTYELLOW = (255,200,0)
HIGHLIGHTER = (255,255,100)     # YELLOW AF
SKYBLUE = (0,255,255)
MIDGREY = (128,128,128)
TAN = (230,220,170)             # PALE YELLOW, DEFO BE GOOD ME THINKS  
COFFEE =(200,190,140)           # ALSO GOOD PALE YELLOW   
MOONGLOW = (235,245,255)        # KINDA CRISPY BRIGHT GREY WITH HINT OF BLUE, QUITE NICE TBF
BROWNTONE1 = (123, 111, 100)    # (119, 99, 80)
BROWNTONE2 = (114, 88, 61)      # FOR BUILDING BARRACADES
BROWNTONE3 = (101, 66, 22)      # FOR BUILDING BARRACADES
BROWNTONE4 = (66, 40, 2)        # HOVERING FULLY BUILT BARRACADE, SHOWS SLIGHTLY DARKER TO INDICATE NULL INTERACTION BETTER THAN NOTHING 
BROWNPALE =  (215, 195, 163)
BLUEMIDNIGHT = (0, 51, 102)
GOOGLEMAPSBLUE = (187,197,233)

# -- General Settings --
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN
# << add game volume here 
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12}

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
SPLAT = 'splat green.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_soft.png"

# Layers
WALL_LAYER = 2
PLAYER_LAYER = 3
BULLET_LAYER = 4
MOB_LAYER = 3
EFFECTS_LAYER = 5
ITEMS_LAYER = 2
ROOF_LAYER = 2
MENU_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'obj_shotgun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 10
BOB_SPEED = 0.3

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}

# UI - Health Bars - Mobs
MOB_HEALTH_BAR_LENGTH, MOB_HEALTH_BAR_HEIGHT = 100, 16
HP_BAR_HP_SEGMENT = 50 # for strips between bars, serves to indicate a block/chunk of hp and ** not ** relative to the bar length

# Lootables
LOOT_BOX_1_IMG = 'lootable_box_1.png'
LOOT_BOX_2_IMG = 'lootable_box_2.png'
LOOT_BOX_3_IMG = 'lootable_box_3.png'
LOOT_BOX_4_IMG = 'lootable_box_4.png'
LOOT_BOX_5_IMG = 'lootable_box_5.png'
LOOT_BOX_6_IMG = 'lootable_box_6.png'

# UI - Mobile Minimap
MOBILE_IMG = "mobile_1.png" # nokia_1

# General Handy Stuff
def round_to_base(x, base=5): 
    """ defaults to 5 """
    return base * round(x/base)