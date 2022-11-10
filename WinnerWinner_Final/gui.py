from random import randint
from settings import *

# todo
# - moving mobile [DONE-BASIC]
# - time [DONE-BASIC]
# - true dynamic time
# - basic af dynamic maps gui [NEXT]
# - blit icons seperately now

class Mobile_Minimap(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = EFFECTS_LAYER # MENU_LAYER 
        self.groups = game.all_sprites, game.minimaps 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # image + rect
        self.og_image = self.game.mobile_img.copy()
        self.image = self.game.mobile_img
        self.rect = self.image.get_rect()
        # positioning
        x_offset = 30
        y_offset = 100
        self.width, self.height, = self.rect.width, self.rect.height  
        self.x = WIDTH - self.width - x_offset
        self.y = HEIGHT - y_offset
        self.pos = vec(self.x, self.y)
        self.rect.center = self.pos 
        self.shelved_y_pos = self.pos.y # storing this on init as self vars so we have it
        # draw inner faux screen rect to our image on init 
        self.inner_screen_rect_x, self.inner_screen_rect_y = 21, 32
        self.inner_screen_rect_width, self.inner_screen_rect_height = self.width - 40, self.height - 40 # GOOGLEMAPSBLUE MAGENTA
        self.inner_rect = pg.Rect(self.inner_screen_rect_x, self.inner_screen_rect_y, self.inner_screen_rect_width, self.inner_screen_rect_height)
        self.inner_screen_rect = pg.draw.rect(self.image, GOOGLEMAPSBLUE, self.inner_rect, 0, 20) 
        # self.inner_screen_surf = pg.Surface((self.inner_screen_rect_width, self.inner_screen_rect_height)) # for text
        self.inner_shift_y = 20 # for shifting all the stuff in the mobile screen seperately from the exterior image (which really acts like a border)
        # page / state
        self.current_state = "minimap"
        # test
        self.clicked_menu_id = False

    def update(self):
        # simply gives us a fresh state every frame
        self.inner_screen_rect = pg.Rect(self.inner_screen_rect_x, self.inner_screen_rect_y, self.inner_screen_rect_width, self.inner_screen_rect_height)
        screen_colour = GOOGLEMAPSBLUE if self.current_state == "minimap" else SKYBLUE
        self.inner_screen_rect = pg.draw.rect(self.image, screen_colour, self.inner_rect, 0, 20) 
        # self.image = self.og_image.copy() # < now the player cant walk off the 'edge' of the phone screen but if they could, or for another reason idk why yet but incase then do dis, basically just redraw the phone too, like we do for the inner screen rect above

    def check_click_home_icon(self):
        if self.current_state == "home":
            mouse = pg.mouse.get_pos()
            for id_tuple, a_rect in self.icons_rects_dict.items():
                if id_tuple == (0,0):
                    print(f"{id_tuple} : {a_rect = }\n{mouse}\n")
                if a_rect.collidepoint(mouse):
                    print(f"Clicked => {id_tuple}")
                    self.clicked_menu_id = id_tuple

    def draw_home_icons(self): # icon_type
        # photos, maps, store, camera, stats, settings, else?
        # yes just 3 is fine here
        # guna prerender the image with the text here to save blitting it
        # as also have forgotten about spacing here for the text so we'll likely need some extra y_spacing
        # this is fine as the bottom 3 icons will be duds anyway or maybe just pure dev mode and or easter eggs
        icon_padding = 15
        icons_per_row = 3
        icon_x, icon_y = 38, 90
        true_size = self.inner_screen_rect_width - (38 * 2) + icon_padding
        icon_length = (true_size / icons_per_row)  # just make it size, so len == height # i think 38 is the guttering here but not sure yet once it is should hard code it
        y_spacing = (icon_length + icon_padding) + 10
        icon_surface = pg.Surface((icon_length, icon_length))
        icon_surface.fill(YELLOW)
        self.icons_rects_dict = {} 
        for row in range(0,3): # rows, to hard code
            row_y = icon_y + (y_spacing * row)
            for col in range(0, icons_per_row): # nearly enumerated this... y r u like dis ¯\_(ツ)_/¯
                nudge = -2
                if (row, col) == self.clicked_menu_id:
                    icon_surface.fill(GREEN)
                else:
                    icon_surface.fill(YELLOW)
                self.image.blit(icon_surface, (icon_x + (icon_length * col) + (icon_padding * col) + nudge, row_y))    
                icon_rect = pg.Rect((icon_x + (icon_length * col) + (icon_padding * col) + nudge) + self.x, row_y + self.y - 268, icon_length, icon_length) # is the drawer difference, guess ive forgotten to update it and it starts in the closed position lol, minor af 
                self.icons_rects_dict[(row, col)] = icon_rect

    def draw_time(self):
        temp_time_text = f"9:00am" if self.current_state == "minimap" else f"11:00pm" # ¯\_(ツ)_/¯ + FONT_SILK_REGULAR_16 = lawd
        time_text_surf = self.game.FONT_SILK_REGULAR_16.render(temp_time_text, True, BLACK)
        time_text_destination = pg.Rect(self.pos.x, self.pos.y, time_text_surf.get_width(), time_text_surf.get_height())
        time_text_destination.move_ip(32, 36)
        self.game.screen.blit(time_text_surf, time_text_destination)

    def update_mobile_position(self, y_pos=500): # super temp implementation, just toggles the pos
        self.pos.y = y_pos if self.pos.y == self.shelved_y_pos else self.shelved_y_pos
    
    def draw_icons(self): # to section into own functions
        # -- battery --
        if self.game.player_battery_level >= 50:
            battery_surf = self.game.battery_full_img # if doing this dynamically just use an empty charge image and do the percentage bar as a dynamically drawn rect
        else:
            battery_surf = self.game.battery_empty_img # if doing this dynamically just use an empty charge image and do the percentage bar as a dynamically drawn rect
        battery_destination = pg.Rect(self.pos.x, self.pos.y, battery_surf.get_width(), battery_surf.get_height())
        battery_destination.move_ip(self.inner_screen_rect_width - 25, 38)
        self.game.screen.blit(battery_surf, battery_destination)

    def draw_current_page(self):
        if self.current_state == "minimap":
            self.draw_minimap()
        else:
            self.draw_home_icons()

    def draw_minimap(self):
        for loot_x, loot_y in self.game.all_lootable_positions:
            self.draw_lootables(loot_x, loot_y)
        # draw the player after as we're doing circles in the hacky way which means its got a background coloured rect underneath it
        self.draw_player()

    def draw_player(self):
        # x and y but should just be seperate functions that will work for both player and zombie, its my first attempt which im actually super chuffed with tbf
        player_minimap_x_percent = (self.game.player.pos.x / self.game.map.width) * 100
        player_minimap_x_pos = (self.inner_screen_rect_width / 100) * player_minimap_x_percent # its calculated using 1% the size of the minimap multiplied by the above percent
        # y
        player_minimap_y_percent = (self.game.player.pos.y / self.game.map.height) * 100
        player_minimap_y_pos = (self.inner_screen_rect_height / 100) * player_minimap_y_percent + self.inner_shift_y # its calculated using 1% the size of the minimap multiplied by the above percent, innershift is new extra
        # circle for the player location
        self.player_minimap_surf = pg.Surface((18, 18))
        self.player_minimap_surf.fill(GOOGLEMAPSBLUE)
        pg.draw.circle(self.player_minimap_surf, BLUEMIDNIGHT, (12,12), 4)
        # final blit
        top_of_screen = 54 # is after icons, true top of mobile screen is more like 32
        player_minimap_y_pos = max(player_minimap_y_pos, top_of_screen) # cap it here so the player cant walk around the edges of the phone on the minimap
        if player_minimap_y_pos > top_of_screen: # dont blit the player if they walk off the top, had considered a "target disconnected" but diminishing returns
            self.image.blit(self.player_minimap_surf, (player_minimap_x_pos, player_minimap_y_pos))
        # print(f"{player_minimap_y_pos = }")

    def draw_lootables(self, loot_pos_x, loot_pos_y):
        wall_minimap_x_percent = (loot_pos_x / self.game.map.width) * 100
        wall_minimap_x_pos = (self.inner_screen_rect_width / 100) * wall_minimap_x_percent 
        wall_minimap_y_percent = (loot_pos_y / self.game.map.height) * 100
        wall_minimap_y_pos = (self.inner_screen_rect_height / 100) * wall_minimap_y_percent + self.inner_shift_y # its calculated using 1% the size of the minimap multiplied by the above percent, innershift is new extra
        # circle for this lootable's location
        wall_minimap_surf = pg.Surface((12, 12))
        wall_minimap_surf.fill(GOOGLEMAPSBLUE)
        pg.draw.circle(wall_minimap_surf, PURPLE, (8,8), 4)
        # final blit
        self.image.blit(wall_minimap_surf, (wall_minimap_x_pos, wall_minimap_y_pos))

            
            
        