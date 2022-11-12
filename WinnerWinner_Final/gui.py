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
        self.width, self.height = self.rect.width, self.image.get_height() - 30
        self.x = WIDTH - self.width - x_offset
        self.y = HEIGHT - y_offset
        self.pos = vec(self.x, self.y)
        self.rect.center = self.pos 
        self.shelved_y_pos = self.pos.y # storing this on init as self vars so we have it
        self.drawered_difference = self.pos.y - self.shelved_y_pos # use this as it starts closed and we dont reset the pos just the rect (?)
        # draw inner faux screen rect to our image on init 
        self.inner_screen_rect_x, self.inner_screen_rect_y = 21, 32
        self.inner_screen_rect_width, self.inner_screen_rect_height = self.width - 40, self.height - 40 # GOOGLEMAPSBLUE MAGENTA
        self.inner_rect = pg.Rect(self.inner_screen_rect_x, self.inner_screen_rect_y, self.inner_screen_rect_width, self.inner_screen_rect_height)
        self.inner_screen_rect = pg.draw.rect(self.image, GOOGLEMAPSBLUE, self.inner_rect, 0, 20) 
        # self.inner_screen_surf = pg.Surface((self.inner_screen_rect_width, self.inner_screen_rect_height)) # for text
        self.inner_shift_y = 20 # for shifting all the stuff in the mobile screen seperately from the exterior image (which really acts like a border)
        # page / state
        self.current_state = "minimap"
        self.clicked_menu_id = False
        # 
        self.home_btn_pos = (32, 70)

    def update(self):
        # simply gives us a fresh state every frame
        self.inner_screen_rect = pg.Rect(self.inner_screen_rect_x, self.inner_screen_rect_y, self.inner_screen_rect_width, self.inner_screen_rect_height)
        if self.current_state == "minimap":
            screen_colour = GOOGLEMAPSBLUE  
        elif self.current_state == "store":
            screen_colour = BLUEMIDNIGHT # TAN 
        else: 
            screen_colour = SKYBLUE
        self.inner_screen_rect = pg.draw.rect(self.image, screen_colour, self.inner_rect, 0, 20) 
        # self.image = self.og_image.copy() # < now the player cant walk off the 'edge' of the phone screen but if they could, or for another reason idk why yet but incase then do dis, basically just redraw the phone too, like we do for the inner screen rect above

    def check_click_home_buttons(self):
        if self.current_state == "home":
            mouse = pg.mouse.get_pos()
            for id_tuple, a_rect in self.icons_rects_dict.items():
                if id_tuple == (0,0):
                    print(f"{id_tuple} : {a_rect = }\n{mouse}\n")
                if a_rect.collidepoint(mouse):
                    print(f"Clicked => {id_tuple}")
                    self.clicked_menu_id = id_tuple
                    if id_tuple == (0,0):
                        print(f"Load Store")
                        self.wipe_clicked_menu()
                        self.current_state = "store"
                    if id_tuple == (0,1):
                        print(f"Load Minimap")
                        self.wipe_clicked_menu()
                        self.current_state = "minimap"
                        
    def draw_store_item(self):
        # just the temp quick first implementation of this
        store_title = self.game.FONT_SILK_REGULAR_20.render(f"Zmazon", True, WHITE)
        store_subtitle = self.game.FONT_SILK_REGULAR_14.render(f"Prime", True, WHITE)
        store_wallet_title = self.game.FONT_SILK_REGULAR_12.render(f"Your Balance", True, GREEN) # if gold >= ..., allow negative balance up to X? (process refund lol)
        store_wallet_balance = self.game.FONT_SILK_REGULAR_14.render(f"${self.game.temp_player_wallet:.2f}", True, GREEN) # if gold >= ..., allow negative balance up to X? (process refund lol)
        store_item = self.game.FONT_SILK_REGULAR_22.render(f"Upgrade Item", True, WHITE)
        store_item_price = self.game.FONT_SILK_REGULAR_16.render(f"$195.00", True, GREEN)
        # -- title --
        self.image.blit(store_title, (60, self.home_btn_pos[1] - 5)) # 90
        self.image.blit(store_subtitle, (60, self.home_btn_pos[1] - 12 + store_title.get_height())) # 90
        # -- wallet --
        wallet_title_dest = self.image.blit(store_wallet_title, (self.inner_screen_rect_width - store_title.get_width() - 8, self.home_btn_pos[1] - 3)) # 90
        self.image.blit(store_wallet_balance, (wallet_title_dest.x + store_wallet_balance.get_width() - 14, wallet_title_dest.y + 12)) # 90
        # -- items --
        # yes i want a bg rect... ok well probably idk yet lol
        for i in range(0,5):
            increment_y = 110
            item_start_x, item_start_y = 80, 135
            group_x_nudge, group_y_nudge = 20, 0 # once they are where you want them as a group use these vars to move them together
            # the item text and price (and else, i.e. stars, offer < 100% do offer)
            store_item_title_pos_x = item_start_x + group_x_nudge
            store_item_title_pos_y = item_start_y + (increment_y * i)
            store_item_price_pos_x = item_start_x + group_x_nudge
            store_item_price_pos_y = item_start_y + (store_item.get_height() - 5) + (increment_y * i)
            self.image.blit(store_item, (store_item_title_pos_x, store_item_title_pos_y)) 
            self.image.blit(store_item_price, (store_item_price_pos_x, store_item_price_pos_y)) 
            # buy x add to cart buttons
            test_button_rect = pg.Rect(store_item_price_pos_x, store_item_price_pos_y + 30, 80, 35)
            test_button_rect_2 = pg.Rect(store_item_price_pos_x + 100, store_item_price_pos_y + 30, 80, 35)
            pg.draw.rect(self.image, BLACK, test_button_rect, 4, 4)
            pg.draw.rect(self.image, BLACK, test_button_rect_2, 4, 4)
            # item images
            item_image_surf = pg.Surface((56, 56)).convert_alpha()
            item_image_surf.fill(BLUEMIDNIGHT)
            item_image_surf.blit(self.game.store_item_weapon_upgrade_img, (0,0))
            self.image.blit(item_image_surf, pg.Rect(store_item_title_pos_x - 70, store_item_title_pos_y, 56, 56))

    def draw_store_page(self):
        self.draw_home_button()
        self.draw_store_item()

    def draw_home_button(self): # yh i thought the naming was better but this (with below) is soooo bad XD
        home_btn_size = 20
        home_btn_rect = pg.Rect(self.home_btn_pos[0], self.home_btn_pos[1], home_btn_size, home_btn_size)
        pg.draw.rect(self.image, RED, home_btn_rect)
        true_rect = home_btn_rect.copy()
        true_rect.move_ip(self.x, self.y + self.drawered_difference)
        if true_rect.collidepoint(pg.mouse.get_pos()):
            if self.game.true_check_mouse_click:
                print(f"Leaving {self.current_state}.\nLoading Home...\n")
                self.current_state = "home"

    def draw_home_buttons(self):
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
        self.icons_rects_dict = {} 
        for row in range(0,3): # rows, to hard code
            row_y = icon_y + (y_spacing * row)
            for col in range(0, icons_per_row): # nearly enumerated range... y r u like dis ¯\_(ツ)_/¯
                nudge = -2
                if (row, col) == self.clicked_menu_id:
                    icon_surface.fill(GREEN)
                else:
                    if row == 0 and col == 0:        
                        icon_surface.fill(CYAN)                
                        icon_surface.blit(self.game.shopping_icon_mobile_img, (0,0))
                    elif row == 0 and col == 1:    
                        icon_surface.fill(CYAN)                
                        icon_surface.blit(self.game.maps_icon_mobile_img, (0,0))
                    else:    
                        icon_surface.fill(YELLOW)
                self.image.blit(icon_surface, (icon_x + (icon_length * col) + (icon_padding * col) + nudge, row_y))  
                icon_rect = pg.Rect((icon_x + (icon_length * col) + (icon_padding * col) + nudge) + self.x, row_y + self.y + self.drawered_difference, icon_length, icon_length) # - 268 is the drawer difference (so it does actually have to stay as plus), guess ive forgotten to update it and it starts in the closed position lol, minor af 
                self.icons_rects_dict[(row, col)] = icon_rect

    def outline_mask(self, img, loc, thickness=3, colr=WHITE):
        mask = pg.mask.from_surface(img)
        mask_outline = mask.outline()
        n = 0
        for point in mask_outline:
            mask_outline[n] = point[0] + loc[0], point[1] + loc[1]
            n += 1
        pg.draw.polygon(self.game.screen, (colr), mask_outline, thickness)  

    def draw_time(self):
        temp_time_text = f"9:00am" if self.current_state == "minimap" else f"11:00pm" # ¯\_(ツ)_/¯ + FONT_SILK_REGULAR_16 = lawd
        time_text_surf = self.game.FONT_SILK_REGULAR_16.render(temp_time_text, True, BLACK)
        time_text_destination = pg.Rect(self.pos.x, self.pos.y, time_text_surf.get_width(), time_text_surf.get_height())
        time_text_destination.move_ip(32, 36)
        self.game.screen.blit(time_text_surf, time_text_destination)

    def update_mobile_position(self, y_pos=500): # super temp implementation, just toggles the pos
        self.pos.y = y_pos if self.pos.y == self.shelved_y_pos else self.shelved_y_pos
        self.drawered_difference = self.pos.y - self.shelved_y_pos # use this as it starts closed and we dont reset the pos just the rect (?)
    
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
        elif self.current_state == "store":
            self.draw_store_page()
        elif self.current_state == "home":            
            self.draw_home_buttons()

    def draw_minimap(self):
        self.draw_home_button()
        for loot_x, loot_y in self.game.all_lootable_positions:
            pass
            # self.draw_lootables(loot_x, loot_y)
        self.draw_player() # draw player last so its on top of the other icons if they are at the same or near positions


    def draw_player(self):
        self.true_player_minimap_pos = self.image.blit(self.game.player_p_img, ((self.inner_screen_rect.width / 2) + 10, (self.inner_screen_rect.height / 2) - 40)) # pos / rect
        print(self.true_player_minimap_pos)
        return self.true_player_minimap_pos

    def draw_workbenches(self, bench_pos_x, bench_pos_y):
        wall_workbench_x_percent = (bench_pos_x / self.game.map.width) * 100
        wall_workbench_x_pos = (self.inner_screen_rect_width / 100) * wall_workbench_x_percent 
        wall_workbench_y_percent = (bench_pos_y / self.game.map.height) * 100
        wall_workbench_y_pos = (self.inner_screen_rect_height / 100) * wall_workbench_y_percent + self.inner_shift_y 
        wall_workbench_surf = self.game.wrench_img
        workbench_destination_rect = pg.Rect(wall_workbench_x_pos, wall_workbench_y_pos, wall_workbench_surf.get_width(), wall_workbench_surf.get_height())
        final_dest = self.game.camera.apply_rect_minimap_camera(workbench_destination_rect, self.inner_screen_rect.width, self.inner_screen_rect.height / 2, self.draw_player())
        print(f"{final_dest = }")
        self.image.blit(wall_workbench_surf, final_dest)

    def draw_player_old(self):
        # x and y but should just be seperate functions that will work for both player and zombie, its my first attempt which im actually super chuffed with tbf
        player_minimap_x_percent = (self.game.player.pos.x / self.game.map.width) * 100
        player_minimap_x_pos = (self.inner_screen_rect_width / 100) * player_minimap_x_percent # its calculated using 1% the size of the minimap multiplied by the above percent
        # y
        player_minimap_y_percent = (self.game.player.pos.y / self.game.map.height) * 100
        player_minimap_y_pos = (self.inner_screen_rect_height / 100) * player_minimap_y_percent + self.inner_shift_y # its calculated using 1% the size of the minimap multiplied by the above percent, innershift is new extra
        self.player_minimap_surf = self.game.player_p_img
        # final blit
        top_of_screen = 54 # is after icons, true top of mobile screen is more like 32
        player_minimap_y_pos = max(player_minimap_y_pos, top_of_screen) # cap it here so the player cant walk around the edges of the phone on the minimap
        if player_minimap_y_pos > top_of_screen: # dont blit the player if they walk off the top, had considered a "target disconnected" but diminishing returns
            self.image.blit(self.player_minimap_surf, (player_minimap_x_pos, player_minimap_y_pos))
       

    def draw_lootables(self, loot_pos_x, loot_pos_y):
        wall_minimap_x_percent = (loot_pos_x / self.game.map.width) * 100
        wall_minimap_x_pos = (self.inner_screen_rect_width / 100) * wall_minimap_x_percent 
        wall_minimap_y_percent = (loot_pos_y / self.game.map.height) * 100
        wall_minimap_y_pos = (self.inner_screen_rect_height / 100) * wall_minimap_y_percent + self.inner_shift_y 
        wall_minimap_surf = self.game.jackpot_img
        self.image.blit(wall_minimap_surf, (wall_minimap_x_pos, wall_minimap_y_pos))

    def draw_workbenches_old(self, bench_pos_x, bench_pos_y):
        wall_workbench_x_percent = (bench_pos_x / self.game.map.width) * 100
        wall_workbench_x_pos = (self.inner_screen_rect_width / 100) * wall_workbench_x_percent 
        wall_workbench_y_percent = (bench_pos_y / self.game.map.height) * 100
        wall_workbench_y_pos = (self.inner_screen_rect_height / 100) * wall_workbench_y_percent + self.inner_shift_y 
        wall_workbench_surf = self.game.wrench_img
        self.image.blit(wall_workbench_surf, (wall_workbench_x_pos, wall_workbench_y_pos))
            
    def wipe_clicked_menu(self): 
        if self.clicked_menu_id:
            self.clicked_menu_id = False
            
        