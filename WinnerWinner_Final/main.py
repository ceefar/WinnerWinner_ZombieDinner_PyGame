import pygame as pg
import sys
from random import choice, random
from os import path
from zombie import *
from settings import *
from sprites import *
from tilemap import *
from lootable import Lootable, Workbench, Delivery_Locker
from player import Player
from gui import Mobile_Minimap
from menus import Inventory_Menu, Lootable_Menu, Delivery_Locker_Menu, Achievement

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.current_level = 1

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
        self.FONT_SILK_REGULAR_20 = pg.font.Font("C:/Users/robfa/Downloads/PyGame_FinalRefactor/WinnerWinner_Final/fonts/Silkscreen-Regular.ttf", 20)
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
        # -- mobile minimap x hud --
        self.mobile_img = pg.image.load(path.join(img_folder, MOBILE_IMG)).convert_alpha()
        self.mobile_img = pg.transform.scale(self.mobile_img, (320, 660))
        self.battery_full_img = pg.image.load(path.join(img_folder, BATTERY_FULL_IMG)).convert_alpha()
        self.battery_full_img = pg.transform.scale(self.battery_full_img, (34, 18))
        self.battery_empty_img = pg.image.load(path.join(img_folder, BATTERY_EMPTY_IMG)).convert_alpha()
        self.battery_empty_img = pg.transform.scale(self.battery_empty_img, (34, 18))
        self.battery_blank_img = pg.image.load(path.join(img_folder, BATTERY_BLANK_IMG)).convert_alpha()
        self.battery_blank_img = pg.transform.scale(self.battery_blank_img, (34, 18))
        # -- home --
        self.shopping_icon_mobile_img = pg.image.load(path.join(img_folder, SHOPPING_ICON_MOBILE_IMG)).convert_alpha()
        self.shopping_icon_mobile_img = pg.transform.scale(self.shopping_icon_mobile_img, (73, 73))
        self.maps_icon_mobile_img = pg.image.load(path.join(img_folder, MAPS_ICON_MOBILE_IMG)).convert_alpha()
        self.maps_icon_mobile_img = pg.transform.scale(self.maps_icon_mobile_img, (73, 73))
        # -- store --
        self.store_item_casino_img = pg.image.load(path.join(img_folder, STORE_ITEM_IMG_CASINO)).convert_alpha()
        self.store_item_casino_img = pg.transform.scale(self.store_item_casino_img, (56, 56))
        self.store_item_weapon_upgrade_img = pg.image.load(path.join(img_folder, STORE_ITEM_IMG_WEAPON_UPGRADE)).convert_alpha()
        self.store_item_weapon_upgrade_img = pg.transform.scale(self.store_item_weapon_upgrade_img, (56, 56))
        # -- workbench & locker concept test --        
        self.workbench_img = pg.image.load(path.join(img_folder, WORKBENCH_IMG)).convert_alpha()
        self.workbench_img = pg.transform.scale(self.workbench_img, (128, 48))
        self.locker_1_img = pg.image.load(path.join(img_folder, LOCKER_TEST_IMG)).convert_alpha()
        self.locker_1_img = pg.transform.scale(self.locker_1_img, (300, 170))
        # test - group with minimap if keeping
        self.wrench_img = pg.image.load(path.join(img_folder, WRENCH_ICON_IMG)).convert_alpha()
        self.wrench_img = pg.transform.scale(self.wrench_img, (24, 24))
        self.jackpot_img = pg.image.load(path.join(img_folder, JACKPOT_ICON_IMG)).convert_alpha()
        self.jackpot_img = pg.transform.scale(self.jackpot_img, (24, 24))
        self.player_p_img = pg.image.load(path.join(img_folder, PLAYER_P_ICON_IMG)).convert_alpha()
        self.player_p_img = pg.transform.scale(self.player_p_img, (24, 24))

    def play_map_1(self):
        # initialize all variables and do all the setup for a new game
        self.all_map_lootables = {} # includes loot details for each lootable
        self.all_sprites = pg.sprite.LayeredUpdates()
        # -- sprite groups --
        self.walls = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.lootables = pg.sprite.Group()
        self.menus = pg.sprite.Group()
        self.minimaps = pg.sprite.Group()
        # quick test
        self.menuables = pg.sprite.Group()
        self.workbenches = pg.sprite.Group()
        self.delivery_lockers = pg.sprite.Group()
        # -- current level map setup -- 
        self.map = TiledMap(path.join(self.map_folder, 'level_large.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        # -- for minimap --
        self.all_lootable_positions = [] # grab these now for the minimap so we do it once using this setup loop otherwise we would have to do it per frame
        # -- parse all the tiles in the tilemap file and initialise new objects and images -- 
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
                self.all_lootable_positions.append((obj_center.x, obj_center.y))
            if tile_object.name == 'workbench': 
                Workbench(self, obj_center.x, obj_center.y)
            if tile_object.name == "locker_y":
                Delivery_Locker(self, obj_center.x, obj_center.y, orientation="y")
        # -- camera --         
        self.camera = Camera(self.map.width, self.map.height)
        # -- general -- 
        self.paused = False
        self.night = False
        if self.game_volume > 0.0:
            self.effects_sounds['level_start'].play()
        # -- gui setup - minimap x menus --
        self.mobile_minimap = Mobile_Minimap(self) # now starting to move menus here so theyre initialised once at runtime and just drawn when valid
        self.delivery_locker_menu = Delivery_Locker_Menu(self) 
        # self.player_inventory_menu = Inventory_Menu(self, self.player.player_inventory)     
        # self.lootable_inventory_menu = Lootable_Menu(self, sprite.my_loot, sprite)     
        # -- for potential addition --
        self.player_battery_level = 100 # would go for percent ig
        # -- misc --
        self.current_lock_time = 0 # needs to be initialised before starting
        self.player_undo = {} # stores the last thing you removed from the players inventory for undo # player_inventory_undo
        self.lootable_undo = {} # stores the last thing you removed from the lootable inventory for undo # lootable_inventory_undo
        self.last_undo_action = False # stores the last undo action (e.g. inventory->delete, lootable->inventory, etc) the player did as a string
        self.player_threw_gold = False # for faux achievement else would move to player class, not intending on expanding this passed 1 or 2 more than this
        self.cheevo_counter = 0 # wanna replace this for just a close button on the achievement, for now its just a faux timer
        self.achievement_unlocks = False
        self.scroll_offset = 0 # so the scrolling can persist as our menu object is created after runtime as its super lightweight 
        self.true_check_mouse_click = False
        # quick test
        self.change_level = False

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
        # self.check_mouse_click = False
        # self.draw_grid()
        is_near_loot = False  # for resetting the charge meter when the player is out of range of any lootbox
        for sprite in self.all_sprites:
            # -- loop all Zombie instances and draw their gui elements --
            if isinstance(sprite, Zombie):
                sprite.draw_unit_health()   
                sprite.draw_unit_name()
                sprite.draw_unit_status()
                sprite.draw_unit_level()
            # -- loop all lootboxes and draw to their surfaces --
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
                        if self.player.charging >= sprite.lock_diff_time:
                            if sprite.can_player_open():
                                self.player_inventory_menu = Inventory_Menu(self, self.player.player_inventory)      
                                self.lootable_inventory_menu = Lootable_Menu(self, sprite.my_loot, sprite)     
                                self.draw_player_inventory()       
                                self.draw_lootable_menu()       
                                # if the inventory is open then also check for user mouse click inputs
                                self.check_mouse_click = True # could rename this to menu_is_open_check_click for clarity but is a bit wordy huh          
            # -- New Delivery Locker initial test implementation --     
            if isinstance(sprite, Delivery_Locker):
                sprite.outline_mask(self.camera.apply_rect(sprite.rect), 10)
                self.mobile_minimap.draw_workbenches(sprite.pos.x, sprite.pos.y)
                player_distance = (sprite.pos - self.player.pos).length()
                if player_distance < 120:
                    self.delivery_locker_menu.draw(sprite)
            # -- Mobile Minimap initial test implementation --                 
            if isinstance(sprite, Mobile_Minimap):
                sprite.draw_current_page()
                self.screen.blit(self.mobile_minimap.image, self.mobile_minimap.pos)
                sprite.draw_time()
                sprite.draw_icons()
            # -- New Workbench initial test implementation --     
            if isinstance(sprite, Workbench): 
                self.screen.blit(sprite.image, self.camera.apply(sprite))
                did_outline = sprite.outline_mask(self.camera.apply_rect(sprite.rect), 10)
                if did_outline: 
                    self.player_inventory_menu = Inventory_Menu(self, self.player.player_inventory)   
                    self.draw_player_inventory()
                if self.mobile_minimap.current_state == "minimap":
                    self.mobile_minimap.draw_workbenches(sprite.pos.x, sprite.pos.y)
            else: # this if else is specific to Workbench? (as it has the blit done at the start)
                # -- draws every sprite in the `all_sprites` group (except Workbench)
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            # -- draw dev mode / debug mode rects, hit boxes, and info --
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1) # draw the objects hit rect

        # -- resets the chargebar if the player is out of range of any lootbox --
        if not is_near_loot:
            self.player.charging = 0
            self.player_undo = False
            self.lootable_undo = False
            self.last_undo_action = False
        # -- day night cycle --
        if self.night:
            self.render_fog()
        # -- dev mode / debug mode display --
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        # -- HUD functions --
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('Zombies : {}'.format(len(self.zombies)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="topright") # temp af af af
        self.temp_player_wallet = self.process_gold() # overhaul this so we literally just have 1 player gold variable in the Player class
        self.draw_text('Gold : {}'.format(self.temp_player_wallet), self.hud_font, 30, WHITE, WIDTH - 10, 40, align="topright") # temp af af af
        # -- cheevo test --
        if self.player_threw_gold:
            if self.player_undo:
                if list(self.player_undo.values())[0]['loot_value'] >= 200:
                    if self.achievement_unlocks == False:
                        self.handle_achievements()
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    # ---- temp af af af ---- 
    def process_gold(self, ): # refactored so now this can be used to calculate gold stacking via inventory additions but need to actually refactor player currency so its much more simplified
        starting_gold = 0
        for item_id_key, item_info_dict in self.player.player_inventory.items():
            if item_info_dict["loot_type"] == "gold":
                cash_money = item_info_dict["loot_value"]
                starting_gold += cash_money
        return starting_gold
    # ---- end temp af af af ----         

    def draw_player_inventory(self):
        # as its in multiple locations (button press, open lootable object) we keep this in its own function incase we want to expand the functionality
        self.player_inventory_menu.update()  
        self.player_inventory_menu.draw_inventory_styling()

    def draw_lootable_menu(self):
        # as its in multiple locations (button press, open lootable object) we keep this in its own function incase we want to expand the functionality
        self.lootable_inventory_menu.update()  
        self.lootable_inventory_menu.draw_inventory_styling()

    def events(self):
        # handle events here
        for event in pg.event.get():
            # -- mouse events --           
            if event.type == pg.MOUSEBUTTONUP: # <- own function duh
                self.true_check_mouse_click = True
                clicked_home_icon = self.mobile_minimap.check_click_home_buttons() # ik
                try: 
                    if not clicked_home_icon:
                        if self.check_mouse_click: 
                            mouse_pos = pg.mouse.get_pos() # mays well define this here
                            # check click actions in either player inventory or lootable inventory menus
                            selected_loot = self.player_inventory_menu.check_user_click_menu(mouse_pos)
                            selected_inventory_loot = self.lootable_inventory_menu.check_user_click_menu(mouse_pos)
                            # check if player inventory menu has a clicked scroll button
                            self.player_inventory_menu.check_user_click_menu_scroll(mouse_pos)
                            # lootable inventory click actions
                            if selected_inventory_loot:
                                if selected_inventory_loot['is_stackable']:
                                    if selected_inventory_loot['loot_type'] == "gold": # is the only stackable for now anyways but leaving as planning to expand                                      
                                        if self.temp_player_wallet > 0:                                        
                                            self.player_inventory_menu.add_gold(selected_inventory_loot["loot_value"]) # but dont add it to inventory like the others below, bosh
                                            self.last_undo_action = "g>g" # gold stacked on gold, no undo
                                        else:
                                            self.player.player_inventory[selected_inventory_loot['loot_id']] = selected_inventory_loot                            
                                    else:
                                        self.player.player_inventory[selected_inventory_loot['loot_id']] = selected_inventory_loot                            
                                else:
                                    self.player.player_inventory[selected_inventory_loot['loot_id']] = selected_inventory_loot                            
                                self.lootable_inventory_menu.the_lootable.my_loot.pop(selected_inventory_loot['loot_id']) 
                                self.lootable_undo = {selected_inventory_loot['loot_id']: selected_inventory_loot}
                                if not self.last_undo_action == "g>g": # since we set this before we have to make sure it doesnt get overwritten
                                    self.last_undo_action = "i>p"
                            # player inventory click actions
                            if selected_loot:
                                selected_loot_id = selected_loot["loot_id"]
                                del_index = 0
                                for key, item in self.player.player_inventory.items():
                                    if item["loot_id"] == selected_loot_id: # note - this problem actually would be easily resolved by making the id also the key but im totally unsure of the interactions until i test it so just trying one implementation first to see which feels best
                                        del_index = key
                                self.player_undo = {del_index:self.player.player_inventory[del_index]}
                                self.player.player_inventory.pop(del_index)
                                if not self.last_undo_action == "g>g":
                                    self.last_undo_action = "p>d"
                                self.player_threw_gold = True
                                for a_item_dict in self.player.player_inventory.values():
                                    if "gold" in a_item_dict["loot_type"]:
                                        self.player_threw_gold = False
                # incase you click when the menu isnt up, can add a bool to supercede this shortly
                except AttributeError as atrErr:
                    print(f"{atrErr = }")  
                # #     except TypeError as typErr:
                # #         print(f"{typErr = }")   
            else:
                self.true_check_mouse_click = False                
            # -- quit event --
            if event.type == pg.QUIT:
                self.quit()
            # -- key down events --
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
                    self.player.charging = 0 # should make a handler function for this now huh
                    self.player_undo = False
                    self.lootable_undo = False
                if event.key == pg.K_i: # 'inventory' menu   
                    self.mobile_minimap.update_mobile_position(400)
                if event.key == pg.K_l: # change 'level' - test af
                    print(f"{self.current_level = }")
                    self.current_level = 2 if self.current_level == 1 else 1
                    self.playing = False
                    self.change_level = True 
                if event.key == pg.K_o: # temp for changing mobile menus
                    mobile_page = self.mobile_minimap.current_state
                    # toggle o just always takes us home
                    if mobile_page != "home":
                        self.mobile_minimap.current_state = "home"
                    
                    # need to implement this
                    # ... # needs to be flags as cant use this event loop for drawing per frame remember 

    def handle_lootable_undo(self): 
        undo_item_id = list(self.lootable_undo.keys())[0]
        undo_item_dictionary = list(self.lootable_undo.values())[0]
        if self.last_undo_action == "i>p": # if the last action was inventory to player
            self.lootable_inventory_menu.the_lootable.my_loot[undo_item_id] = undo_item_dictionary
            self.player.player_inventory.pop(undo_item_id) # also remove form the player since we've brought it back to the lootable with this undo
            self.player_undo = False # wipe this we put loot from the lootable to the player, then we undid that so its back with the lootable not the player, if the player could undo they would take it back i think ?
            self.last_undo_action = False # always gets reset once the undo is complete (as the last action was simply an undo)
            self.lootable_undo = False 
        if self.last_undo_action == "g>g":
            self.player_undo = False
            self.last_undo_action = False
            self.lootable_undo = False 
        
    def handle_player_undo(self): 
        undo_item_id = list(self.player_undo.keys())[0]
        undo_item_dictionary = list(self.player_undo.values())[0]
        self.player.player_inventory[undo_item_id] = undo_item_dictionary
        if self.last_undo_action == "p>d": # if you've just done a player delete action you've invalidated any lootable undo *if* you had placed a loot from the lootable to your inventory
            self.last_undo_action = False # always gets reset once the undo is complete (as the last action was simply an undo)
            self.lootable_undo = False # basically this is no longer valid
            self.player_undo = False
        if self.last_undo_action == "g>g":
            self.player_undo
            self.last_undo_action = False
            self.lootable_undo = False

    def handle_achievements(self): # just temp faux implementation for now, dont even have a close button yet (which imo you need over a timer to close but cba rn)
        if self.cheevo_counter < 300:
            self.cheevo_counter += 1
            self.cheevo = Achievement(self)
            self.cheevo.draw()
        else:
            # reset everything
            self.cheevo_counter = 0
            self.player_threw_gold = False
            self.achievement_unlocks = True

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

    # [ CRIT! ] - again if you're going to keep this functionality 100% refactor so this *just* loads the map, duhhhhhh
    def play_map_2(self):
        # initialize all variables and do all the setup for a new game
        self.all_map_lootables = {} # includes loot details for each lootable
        self.all_sprites = pg.sprite.LayeredUpdates()
        # -- sprite groups --
        self.walls = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.lootables = pg.sprite.Group()
        self.menus = pg.sprite.Group()
        self.minimaps = pg.sprite.Group()
        # quick test
        self.menuables = pg.sprite.Group()
        self.workbenches = pg.sprite.Group()
        self.delivery_lockers = pg.sprite.Group()
        # -- current level map setup -- 
        self.map = TiledMap(path.join(self.map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        # -- for minimap --
        self.all_lootable_positions = [] # grab these now for the minimap so we do it once using this setup loop otherwise we would have to do it per frame
        # -- parse all the tiles in the tilemap file and initialise new objects and images -- 
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
                self.all_lootable_positions.append((obj_center.x, obj_center.y))
            if tile_object.name == 'workbench': 
                Workbench(self, obj_center.x, obj_center.y)
        # -- camera --         
        self.camera = Camera(self.map.width, self.map.height)
        # -- general -- 
        self.paused = False
        self.night = False
        if self.game_volume > 0.0:
            self.effects_sounds['level_start'].play()
        # -- minimap x gui setup --
        self.mobile_minimap = Mobile_Minimap(self)    
        # -- for potential addition --
        self.player_battery_level = 100 # would go for percent ig
        # -- misc --
        self.current_lock_time = 0 # needs to be initialised before starting
        self.player_undo = {} # stores the last thing you removed from the players inventory for undo # player_inventory_undo
        self.lootable_undo = {} # stores the last thing you removed from the lootable inventory for undo # lootable_inventory_undo
        self.last_undo_action = False # stores the last undo action (e.g. inventory->delete, lootable->inventory, etc) the player did as a string
        self.player_threw_gold = False # for faux achievement else would move to player class, not intending on expanding this passed 1 or 2 more than this
        self.cheevo_counter = 0 # wanna replace this for just a close button on the achievement, for now its just a faux timer
        self.achievement_unlocks = False
        self.scroll_offset = 0 # so the scrolling can persist as our menu object is created after runtime as its super lightweight 
        self.true_check_mouse_click = False


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


# create the game object
g = Game()
g.show_start_screen()
while True:
    if g.current_level == 1: 
        g.play_map_1()
        g.run()
        if not g.change_level:
            g.show_go_screen()
    else:
        g.play_map_2()
        g.run()
        if not g.change_level:
            g.show_go_screen()

