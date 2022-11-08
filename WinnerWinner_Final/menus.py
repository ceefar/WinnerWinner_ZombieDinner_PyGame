from settings import *

class Inventory_Menu(pg.sprite.Sprite): # ideally would do a parent menu class just havent got round to it yet... also should rename to just inventory menu, and also should be snake_case, oh the shame XD
    def __init__(self, game, inventory_info): # new default param on the_lootable allows us to blit this without having to have a lootable box near by (tho need to update appropriate mouse click functions if this is opened by pressing key i for inventory)
        self._layer = MENU_LAYER # ITEMS_LAYER 
        self.groups = game.menus 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game, self.player = game, game.player
        # -- position, dimensions, image (just a coloured surf), & rect setup --  
        nudge_x, nudge_y = 350, 100
        height = ((len(inventory_info)) + 1) * 50 # dynamically sets the height 
        min_height = 200
        self.height = max(height, min_height)
        self.length = 300
        self.image = pg.Surface((self.length, self.height))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect() # self.rect.center = self.pos 
        self.pos = vec((self.player.pos.x - nudge_x), self.player.pos.y - nudge_y)
        # -- store the passed inventory parameter --
        self.inventory_dict = inventory_info # pass this as a parameter incase we want to have companion units with inventorys
        # -- rects/positions of ui elements that have actions, e.g. undo, close window, scroll, etc --
        self.undo_button_rect = False

    def draw_inventory_styling(self):
        """ basically just drawing the header """
        # setup title text surf and header offset position
        if isinstance(self, Lootable_Menu):
            header_text_surf = self.game.FONT_SILK_REGULAR_14.render("Lootbox Contents", True, self.the_lootable.rarity_colour)
        else:           
            header_text_surf = self.game.FONT_SILK_REGULAR_14.render("Player Inventory", True, CYAN)
        header_text_surf_height = header_text_surf.get_height()
        header_offsest = (0, -header_text_surf_height - 16) # in place move co-ordinates vs the menu bg img position         
        # create rect for the position of the title, then move that position based on the cameras positon on the map, 
        destination = pg.Rect(self.pos.x, self.pos.y, 300, 50) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_rect(destination).copy()
        destination.move_ip(header_offsest) # move the text to the bg box position
        # bg of the header title
        header_bg_surf = pg.Surface((300, header_text_surf_height + 10)).convert_alpha()
        header_bg_surf.fill(DARKGREY)
        header_bg_surf.set_alpha(220)
        # undo button, surf dest and temp 'u' text
        undo_text_surf = self.game.FONT_SILK_REGULAR_12.render("U", True, BLACK)
        undo_center_offset = (int(header_text_surf_height - undo_text_surf.get_width())/2, int(header_text_surf_height - undo_text_surf.get_height())/2)
        undo_button_surf = pg.Surface((header_text_surf_height, header_text_surf_height)).convert_alpha()
        undo_button_surf.fill(BLUEGREEN)
        undo_button_surf.blit(undo_text_surf, undo_center_offset)
        undo_button_dest = destination.copy()
        undo_button_dest.move_ip(300 - (header_text_surf_height * 2) + 10, 5)
        undo_button_rect = undo_button_dest
        self.undo_button_rect = undo_button_rect
        # centralise the text
        header_destination = destination.copy()
        header_destination.move_ip(5, 3)
        # finally blit directly to the screen, not to the surface, because i want the surface to have a slight alpha channel value and the text wont
        self.game.screen.blit(header_bg_surf, destination)
        if not isinstance(self, Lootable_Menu):
            if self.game.player_undo:
                self.game.screen.blit(undo_button_surf, undo_button_dest)
        else:
            if self.game.lootable_undo:
                self.game.screen.blit(undo_button_surf, undo_button_dest)
        self.game.screen.blit(header_text_surf, header_destination)

    def update(self):
        if isinstance(self, Lootable_Menu):
            self.item_rects = {}
            # self.inventory_dict = self.inventory_dict[0]
        # loop all the items in the given inventory dictionary  
        for i, (indx_id, item) in enumerate(self.inventory_dict.items()):

            # first handle any stacking objects
            if item["loot_type"] == "gold": # types more important now, see below
                # actually will be stackable only for player inventory instance, for other it should just go by types, and multiple uber gold, uber gold, should be allowed tbf
                pass # literally just guna have different text, the difficult part is the stacking on click lol so do that first duh

            box_height = 46
            item_title = item["loot_name"]
            item_subtext = item["loot_value"]
            # these are likely for debugging so can delete when finalised
            item_id = item["loot_id"]
            item_rarity = item["loot_rarity"]
            name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"{item_title}", True, WHITE)
            if isinstance(self, Lootable_Menu):
                name_subtextsurface = self.game.FONT_SILK_REGULAR_12.render(f"{item_subtext}", True, self.the_lootable.rarity_colour)
            else:
                name_subtextsurface = self.game.FONT_SILK_REGULAR_12.render(f"{item_subtext}", True, CYAN) # self.get_rarity_colour(self.player.open_box_rarity) <<< this will now be part of the items dictionary !
            destination = (10, 5) 
            sub_destination = (10, 25) 
            item_text_rect = pg.rect.Rect(0, i*box_height, self.length, box_height)
            item_text_bg_surf = pg.Surface((self.length, box_height))
            if i % 2 == 0:
                item_text_bg_surf.fill(DARKGREY)
            else:
                item_text_bg_surf.fill(NICEGREY)
            item_text_bg_surf.blit(name_textsurface, destination)
            item_text_bg_surf.blit(name_subtextsurface, sub_destination)                
            self.image.blit(item_text_bg_surf, item_text_rect)
            if isinstance(self, Lootable_Menu):
                self.item_rects[indx_id] = pg.rect.Rect(self.pos.x, self.pos.y + (i * box_height), self.length, box_height)
                # print(f"HERE > {self.item_rects = } {self.item_rects[indx_id] = }")
            else:    
                self.game.player.player_inventory[indx_id]["loot_rect"] = pg.rect.Rect(self.pos.x, self.pos.y + (i * box_height), self.length, box_height)
        # blit the whole menu
        destination = pg.rect.Rect(self.pos.x, self.pos.y, self.length, self.height)
        self.game.screen.blit(self.image, self.game.camera.apply_rect(destination))

    def check_user_click_menu(self, mouse):
        if self.undo_button_rect.collidepoint(mouse):   
            self.game.handle_player_undo() 
        for id, info_dict in self.game.player.player_inventory.items(): # _ if not using id
            rect = self.game.camera.apply_rect(info_dict["loot_rect"])
            if rect.collidepoint(mouse): # print(f"{rect = }") # print(f"{info_dict = }") # print(f"{self.inventory_dict[id] = }")
                return(info_dict)        

    
# quick child implementation, do ideally need to refactor above to be a true Menu parent class and have two children one Lootable_Menu and one Player_Menu
class Lootable_Menu(Inventory_Menu):
    def __init__(self, game, inventory_info, the_lootable): 
        super().__init__(game, inventory_info)
        self.the_lootable = the_lootable
        nudge_x, nudge_y = -40, -50
        self.pos = vec((the_lootable.pos.x - nudge_x), the_lootable.pos.y - nudge_y)

    # CLEARLY WHERE THE DEBUG PRINTS SHOULD BE 
    def check_user_click_menu(self, mouse):
        if self.undo_button_rect.collidepoint(mouse):
            self.game.handle_lootable_undo()
        # print(f"All item rects in this menu : {self.item_rects}")
        for loot_id, loot_item_rect in self.item_rects.items():
            rect = self.game.camera.apply_rect(loot_item_rect)
            if rect.collidepoint(mouse):
                return self.inventory_dict[loot_id]   
    

    # legit next thing to do is the lootable menu and the click functionality
    # in all seriousness just think about this as being from the ground up, so if you have to completely change something just do it 

    # so im starting with gold only!
    # - i think have gold be just called uber gold if its a rarer large gold
    # - and inventory gold just stacks as its own kinda seperate ting since you always have gold even if its 0 bosh

    # for rarity have it simply impact sumnt called condition - i.e. rusty ammo, holopoint, titanium, etc
    #   - do want ammo for different weapons remember, 
    #   - dicts can be different based on type which is handy af tbf just need some consistency across the main things like name and value
    
    # remember types, stacking, consuming, undo, delete, etc, see todo notes and lootable.py notes
    # - especially cause why stylise especially as colours n shit until items done especially as i said for rarity
    
    # then clicking and moving stuff with new improved items dict as per init load terminal print



    # def check_click(self, mouse):
    #     for i, rect in enumerate(self.item_rects):
    #         rect = self.game.camera.apply_rect(rect)
    #         if rect.collidepoint(mouse):
    #             # should include take all buttons and return all buttons, as well as close button and obvs close keyboard press option too
    #             print(f"Clicked {i+1} = > {self.game.player.player_inventory[i]}")           
    #             self.game.open_loot_boxes[self.the_lootable.my_id].append(str(i))
    #             return(str(i), self.the_lootable.my_id, f"{self.game.player.player_inventory[i]}") # f"{self.game.player.player_inventory[i]}"




    # def update(self):
    #     self.item_rects = [] # save the rects now so we dont have to loop every instance of the class (could be done better with a game. var duh)
    #     # for each item 
    #     for i, item in enumerate(self.inventory_list):
    #         box_height = 46
    #         split = item.find("-")
    #         item_title = item[:split]
    #         item_subtext = item[split + 1:].strip()
    #         name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"{item_title}", True, WHITE)
    #         name_subtextsurface = self.game.FONT_SILK_REGULAR_12.render(f"{item_subtext}", True, CYAN) # self.get_rarity_colour(self.player.open_box_rarity) <<< this will now be part of the items dictionary !
    #         destination = (10, 5) 
    #         sub_destination = (10, 25) 
    #         item_text_rect = pg.rect.Rect(0, i*box_height, self.length, box_height)
    #         item_text_bg_surf = pg.Surface((self.length, box_height))
    #         if i % 2 == 0:
    #             item_text_bg_surf.fill(DARKGREY)
    #         else:
    #             item_text_bg_surf.fill(NICEGREY)
    #         # heart_img = self.game.heart_img.copy()
    #         # if "HP" in item:                
    #         #     item_text_bg_surf.blit(heart_img, (item_text_rect.width - 40, 12))
    #         item_text_bg_surf.blit(name_textsurface, destination)
    #         item_text_bg_surf.blit(name_subtextsurface, sub_destination)                
    #         self.image.blit(item_text_bg_surf, item_text_rect)
    #         self.item_rects.append(pg.rect.Rect(self.pos.x, self.pos.y + (i * box_height), self.length, box_height))
    #     # blit the whole menu
    #     destination = pg.rect.Rect(self.pos.x, self.pos.y, self.length, self.height)
    #     self.game.screen.blit(self.image, self.game.camera.apply_rect(destination))