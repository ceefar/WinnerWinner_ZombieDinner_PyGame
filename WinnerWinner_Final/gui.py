from random import randint
from settings import *

# todo
# - moving mobile [DONE-BASIC]
# - time [DONE-BASIC]
# - true dynamic time
# - basic af dynamic maps gui [NEXT]
# - blit icons seperately now
# - add mobs and loot
# - continue

class Mobile_Minimap(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MENU_LAYER 
        self.groups = game.all_sprites, game.minimaps 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # image + rect
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
        self.inner_screen_rect = pg.draw.rect(self.image, GOOGLEMAPSBLUE, pg.Rect(self.inner_screen_rect_x, self.inner_screen_rect_y, self.inner_screen_rect_width, self.inner_screen_rect_height),  0, 20) 
        self.inner_screen_surf = pg.Surface((self.inner_screen_rect_width, self.inner_screen_rect_height)) # for text

    def draw_time(self):
        time_text_surf = self.game.FONT_SILK_REGULAR_16.render(f"9:00am", True, BLACK)
        time_text_destination = pg.Rect(self.pos.x, self.pos.y, time_text_surf.get_width(), time_text_surf.get_height())
        time_text_destination.move_ip(32, 36)
        self.game.screen.blit(time_text_surf, time_text_destination)

    def update_mobile_position(self, y_pos=500): # super temp implementation, just toggles the pos
        self.pos.y = y_pos if self.pos.y == self.shelved_y_pos else self.shelved_y_pos

    def draw_player(self):
        # x and y but should just be seperate functions that will work for both player and zombie, its my first attempt which im actually super chuffed with tbf
        player_minimap_x_percent = (self.game.player.pos.x / self.game.map.width) * 100
        player_minimap_x_pos = (self.inner_screen_rect_width / 100) * player_minimap_x_percent # its calculated using 1% the size of the minimap multiplied by the above percent
        # y
        player_minimap_y_percent = (self.game.player.pos.y / self.game.map.height) * 100
        player_minimap_y_pos = (self.inner_screen_rect_height / 100) * player_minimap_y_percent # its calculated using 1% the size of the minimap multiplied by the above percent
        # circle for the player location
        self.player_minimap_surf = pg.Surface((20, 20))
        self.player_minimap_surf.fill(GOOGLEMAPSBLUE)
        pg.draw.circle(self.player_minimap_surf, BLACK, (10,10), 4)
        # final blit
        self.image.blit(self.player_minimap_surf, (player_minimap_x_pos, player_minimap_y_pos))

            
            
        