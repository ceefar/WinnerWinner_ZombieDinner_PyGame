import pygame as pg
import sys
from random import choice, random
from os import path
from zombie import *
from settings import *
from sprites import *
from tilemap import *
from lootable import Lootable
from player import Player

# first
# -
# save to fork

# -
# then
# -
# new fork v1.02
# start adding menus, loot, etc all the fun stuff
# - rememmber c to close should still work btw
# - get i to open independently sorted early too
# - remember to add open text btw
# - may be worth doing tidbits for other on screen ui now too (or maybe nah lol)

# previous notes
# - 
#   - pure bosh straight into our new menu stuff
#   - starting out being sure we have the dict all sorted properly to work flawlessly when passing n deleting
#   - NOT OPTIONAL!!! => with attention now to undo, delete, stacking, and consuming        
#   - remember loot needs shit like its id, rarity, type, etc
#   - and note do want items like clothing so might be worth a quick inclusion
#   - and even stuff i havent done yet that i want like rarity too
#       - and a simple randomiser for the value based on rarity too 
#       - do we then pass the box rarity, yes we must so there we go u gotta think first lol
#       - pseudocode it pls


# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.game_volume = 0.0
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
            s.set_volume(self.game_volume)
            self.effects_sounds[type] = s
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(self.game_volume)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(self.game_volume)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(self.game_volume)
            self.player_hit_sounds.append(s)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(self.game_volume)
            self.zombie_hit_sounds.append(s) 
        # -- misc --
        self.draw_debug = False
        # -- load fonts --
        # [ TODO! ] to make as incrementally function shortly
        self.FONT_SILK_REGULAR_10 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 10) 
        self.FONT_SILK_REGULAR_12 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 12)
        self.FONT_SILK_REGULAR_14 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 14)
        self.FONT_SILK_REGULAR_16 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 16)
        self.FONT_SILK_REGULAR_18 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 18)
        self.FONT_SILK_REGULAR_22 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 22)
        self.FONT_SILK_REGULAR_24 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 24)
        self.FONT_SILK_REGULAR_32 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 32)
        # -- additional images to be sectioned into associated lists or functions for incremental loading --
        self.lootbox_small_1_img = pg.image.load(path.join(img_folder, LOOT_BOX_1_IMG)).convert_alpha()
        self.lootbox_small_2_img = pg.image.load(path.join(img_folder, LOOT_BOX_2_IMG)).convert_alpha()
        self.lootbox_small_3_img = pg.image.load(path.join(img_folder, LOOT_BOX_3_IMG)).convert_alpha()
        self.lootbox_small_4_img = pg.image.load(path.join(img_folder, LOOT_BOX_4_IMG)).convert_alpha()
        self.lootbox_small_5_img = pg.image.load(path.join(img_folder, LOOT_BOX_5_IMG)).convert_alpha()
        self.lootbox_small_6_img = pg.image.load(path.join(img_folder, LOOT_BOX_6_IMG)).convert_alpha()
        # testing resize quickly
        self.lootbox_small_1_img = pg.transform.scale(self.lootbox_small_1_img, (46, 46))
        self.lootbox_small_2_img = pg.transform.scale(self.lootbox_small_2_img, (46, 46))
        self.lootbox_small_3_img = pg.transform.scale(self.lootbox_small_3_img, (46, 46))
        self.lootbox_small_4_img = pg.transform.scale(self.lootbox_small_4_img, (46, 46))
        self.lootbox_small_5_img = pg.transform.scale(self.lootbox_small_5_img, (46, 46))
        self.lootbox_small_6_img = pg.transform.scale(self.lootbox_small_6_img, (46, 46))
        # larger versions
        self.lootbox_small_1_large_img = pg.transform.scale(self.lootbox_small_1_img, (58, 58))
        self.lootbox_small_2_large_img = pg.transform.scale(self.lootbox_small_2_img, (58, 58))
        self.lootbox_small_3_large_img = pg.transform.scale(self.lootbox_small_3_img, (58, 58))
        self.lootbox_small_4_large_img = pg.transform.scale(self.lootbox_small_4_img, (58, 58))
        self.lootbox_small_5_large_img = pg.transform.scale(self.lootbox_small_5_img, (58, 58))
        self.lootbox_small_6_large_img = pg.transform.scale(self.lootbox_small_6_img, (58, 58))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_map_lootables = {} # includes loot details for each lootable
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.lootables = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'level_large.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Zombie(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)
            if tile_object.name == 'lootable_box_small': 
                Lootable(self, obj_center.x, obj_center.y, tile_object.name)                
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False
        self.night = False
        if self.game_volume > 0.0:
            self.effects_sounds['level_start'].play()
        # -- misc --
        self.current_lock_time = 0 # needs to be initialised before starting
        
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        if self.game_volume > 0.0:
            pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # -- game over man --
        if len(self.zombies) == 0:
            self.playing = False
        # -- collision : player > items --
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
                if self.game_volume > 0:
                    self.effects_sounds['health_up'].play()
            if hit.type == 'shotgun':
                hit.kill()
                self.player.weapon = 'shotgun'
                if self.game_volume > 0:
                    self.effects_sounds['gun_pickup'].play()
        # -- collision : player > zombies --
        hits = pg.sprite.spritecollide(self.player, self.zombies, False, collide_hit_rect)
        for hit in hits:
            if self.game_volume > 0:
                if random() < 0.7:
                    choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # -- collision [group] : zombies > bullets [deleted] --
        hits = pg.sprite.groupcollide(self.zombies, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.current_health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        is_near_loot = False  # for resetting the charge meter when the player is out of range of any lootbox
        for sprite in self.all_sprites:
            # -- loop all lootboxes and draw them --
            if isinstance(sprite, Lootable):
                player_distance = (sprite.pos - self.player.pos).length()
                if player_distance < 90: # if the player is near this lootable      
                    is_near_loot = True # for resetting the charge meter when the player is out of range of any lootbox
                    sprite.draw_lootable_info() # draw the tiny menu to show the rarity, name, size, etc
                    if sprite.can_player_open(): # check if the player has a high enough lockpicking skill / meets any requirements to unlock this lootable
                        sprite.outline_mask(sprite.image.copy(), self.camera.apply(sprite), thickness=12, colr=GREEN) # highlight the lootable green if it can be opened by the player
                    else:
                        sprite.outline_mask(sprite.image.copy(), self.camera.apply(sprite), thickness=12, colr=RED) # else highlight it red if its locked                    
                    if self.player.charging:          
                        # if player is charging calculate how much they have charged for the current bar and use a chargebar on the menu to display the current unlock percent         
                        self.current_lock_time = sprite.lock_diff_time # make this a game variable so the player can access it outside of looping all instances 
                        charge_percent = (self.player.charging / sprite.lock_diff_time) * 100 # watch for possible zero div error here tho is an easy fix tbf
                        sprite.blit_chargebar(charge_percent)
                        # print(f"{self.player.charging: = } {sprite.lock_diff_time} {self.player.lockpicking_skill_points * 100}")   
                        if self.player.charging >= sprite.lock_diff_time:
                            if sprite.can_player_open():
                                print(f"Open a bitch")
                
            # -- loop all zombies and draw them --
            if isinstance(sprite, Zombie):
                sprite.draw_unit_health()   
                sprite.draw_unit_name()
                sprite.draw_unit_status()
                sprite.draw_unit_level()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        # -- resets the chargebar if the player is out of range of any lootbox --
        if not is_near_loot:
            self.player.charging = 0
        # -- day night cycle --
        if self.night:
            self.render_fog()
        # -- dev mode / debug mode display --
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('Zombies: {}'.format(len(self.zombies)), self.hud_font, 30, WHITE,
                       WIDTH - 10, 10, align="topright")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_c: # 'close' an open menu
                    self.player.charging = 0

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
 
    # [ TODO-ASAP! ] - refactor these properly so that their usage is more definitive
    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def draw_text_alt(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect = text_surface.get_rect(**{"topleft": (x, y)})
        self.screen.blit(text_surface, text_rect)

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

