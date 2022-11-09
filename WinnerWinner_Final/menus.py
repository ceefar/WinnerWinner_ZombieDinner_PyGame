from settings import *



class Inventory_Menu(pg.sprite.Sprite): # ideally would do a parent menu class just havent got round to it yet... also should rename to just inventory menu, and also should be snake_case, oh the shame XD
    def __init__(self, game, inventory_info:dict): # new default param on the_lootable allows us to blit this without having to have a lootable box near by (tho need to update appropriate mouse click functions if this is opened by pressing key i for inventory)
        self._layer = MENU_LAYER # ITEMS_LAYER 
        self.groups = game.menus 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game, self.player = game, game.player
        # -- position, dimensions, image (just a coloured surf), & rect setup --  
        nudge_x, nudge_y = 350, 100
        max_menu_items = 4.5 # just incase i wanna tweak it a bit, *8 *9 or *10 seems to be a good range, well depending on loot item container height tbf
        self.item_container_height = 46 # for each individual item not the menu itself, needed for dynamic resizing and scroll, plus ease of testing ui is nice
        height = ((len(inventory_info)) + 1) * self.item_container_height # dynamically sets the height 
        min_height = 3 * max_menu_items # the minimum height its 3x for simplicity here but 150 - 200 is a nice range to hardcode it
        max_height =  self.item_container_height * max_menu_items 
        if len(inventory_info) > max_menu_items:
            self.needs_scroll = True
        else:
            self.needs_scroll = False
        if not isinstance(self, Lootable_Menu):
            ... # not implementing yet tho will do in future for sure, i really enjoy this kinda stuff tho it brings very little value to this actual project lol
        self.height = 0
        if isinstance(self, Lootable_Menu):
            self.height = max(height, min_height)
        else:
            self.height = max(max_height, min_height)
        self.length = 300
        self.image = pg.Surface((self.length, self.height))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect() # self.rect.center = self.pos 
        self.pos = vec((self.player.pos.x - nudge_x), self.player.pos.y - nudge_y)
        # -- reorder passed inventory dict param so it starts with gold, then store the result as an instance variable --
        # use this handy func, but move it tbf
        def reorder_dict(a_dict_value): # im **really** proud of this implementation tbf, and could be a lambda too tbf <3 but do actually wanna re-use it lol
            return 0 if a_dict_value["loot_type"] == "gold" else 1 # return false is if loot type is gold else true which sets our gold to 0 pos then the rest to whatever as it doesnt matter the remaining order and we can easily change this to stackable loot_type in future to expand the functionality        
        final_inventory_info_dict = {}
        reordered_dict_list = sorted(inventory_info.values(), key=reorder_dict) # reorder the dict using a custom key function
        for a_dict in reordered_dict_list: # un-nest from a list of dicts to nested dicts
            final_inventory_info_dict[a_dict["loot_id"]] = a_dict 
        self.inventory_dict = final_inventory_info_dict # defo pass this as a parameter incase we want to have companion units with inventorys too
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
            item_title, item_value = item["loot_name"], item["loot_value"]
            # these are probably here just for testing so can delete em when finalised
            item_id = item["loot_id"]
            item_rarity = item["loot_rarity"]
            # 100% needs to be a function huh
            if "gold" in item_title.lower():
                if item_value < 50:
                    name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"Baby {item_title}", True, WHITE)
                elif item_value >= 50 and item_value < 200:
                    name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"Basic {item_title}", True, WHITE)
                elif item_value >= 200 and item_value < 400:
                    name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"Decent {item_title}", True, WHITE)
                elif item_value >= 400 and item_value < 650:
                    name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"Uber {item_title}", True, WHITE)
                elif item_value >= 650 and item_value < 1000:
                    name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"Uber {item_title}", True, WHITE)
                elif item_value >= 1000 and item_value < 1400:
                    name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"Uber {item_title}", True, WHITE)
                elif item_value >= 1400 and item_value < 2000:
                    name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"Uber {item_title}", True, WHITE)
                else:                    
                    name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"Giga {item_title}", True, WHITE)
            else:                 
                name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"{item_title}", True, WHITE)
            if isinstance(self, Lootable_Menu):
                name_subtextsurface = self.game.FONT_SILK_REGULAR_12.render(f"{item_value}", True, self.the_lootable.rarity_colour)
            else:
                name_subtextsurface = self.game.FONT_SILK_REGULAR_12.render(f"{item_value}", True, CYAN) # self.get_rarity_colour(self.player.open_box_rarity) <<< this will now be part of the items dictionary !
            destination = (10, 5) 
            sub_destination = (10, 25) 
            item_text_rect = pg.rect.Rect(0, i* self.item_container_height, self.length,  self.item_container_height)
            item_text_bg_surf = pg.Surface((self.length,  self.item_container_height))
            if i % 2 == 0:
                item_text_bg_surf.fill(DARKGREY)
            else:
                item_text_bg_surf.fill(NICEGREY)
            item_text_bg_surf.blit(name_textsurface, destination)
            item_text_bg_surf.blit(name_subtextsurface, sub_destination)                
            self.image.blit(item_text_bg_surf, item_text_rect)
            if isinstance(self, Lootable_Menu):
                self.item_rects[indx_id] = pg.rect.Rect(self.pos.x, self.pos.y + (i *  self.item_container_height), self.length,  self.item_container_height)
                # print(f"HERE > {self.item_rects = } {self.item_rects[indx_id] = }")
            else:    
                self.game.player.player_inventory[indx_id]["loot_rect"] = pg.rect.Rect(self.pos.x, self.pos.y + (i *  self.item_container_height), self.length,  self.item_container_height)
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

    def add_gold(self, gold_to_add):
        for id, info_dict in self.game.player.player_inventory.items():
            if "gold" in info_dict["loot_type"]:
                final_gold = info_dict["loot_value"] + gold_to_add
                info_dict["loot_value"] = final_gold

    
# quick child implementation, do ideally need to refactor above to be a true Menu parent class and have two children one Lootable_Menu and one Player_Menu
class Lootable_Menu(Inventory_Menu):
    def __init__(self, game, inventory_info, the_lootable): 
        super().__init__(game, inventory_info)
        self.the_lootable = the_lootable
        nudge_x, nudge_y = -40, -50
        self.pos = vec((the_lootable.pos.x - nudge_x), the_lootable.pos.y - nudge_y)

    def check_user_click_menu(self, mouse):
        if self.undo_button_rect.collidepoint(mouse):
            self.game.handle_lootable_undo()
        # print(f"All item rects in this menu : {self.item_rects}")
        for loot_id, loot_item_rect in self.item_rects.items():
            rect = self.game.camera.apply_rect(loot_item_rect)
            if rect.collidepoint(mouse):
                return self.inventory_dict[loot_id]   
    

# remember types, stacking, consuming, undo, delete, etc, see todo notes and lootable.py notes
# - especially cause why stylise especially as colours n shit until items done especially as i said for rarity

    
class Achievement(pg.sprite.Sprite): # atleast so this semi properly so you can pass it either a string, or some kinda dict that will have id keys for these kinda events (string is fine lmao)
    def __init__(self, game):
        self.groups = game.menus # , game.all_sprites
        self.game = game
        width, height = 400, 90 
        self.image = pg.Surface((width, height))
        self.image.fill(BLUEMIDNIGHT)
        # self.rect = self.image.get_rect() # self.rect.center = self.pos 
        self.pos = vec((WIDTH / 2) - (width / 2), HEIGHT - height - 50)
        self.rect = pg.Rect(self.pos.x, self.pos.y, width, height)
    
    def draw(self):
        # main title
        cheevo_text_surf = self.game.FONT_SILK_REGULAR_18.render("YOLO! Dropped over 100 gold", True, WHITE)
        cheevo_text_width, cheevo_text_height = cheevo_text_surf.get_width(), cheevo_text_surf.get_height()
        self.image.blit(cheevo_text_surf, ((self.rect.width / 2) - (cheevo_text_width / 2), (self.rect.height / 2) - (cheevo_text_height / 2) - cheevo_text_height + 15)) # one extra height to have it be a header
        # card header
        cheevo_card_text_surf = self.game.FONT_SILK_REGULAR_10.render("Achievement Unlocked!", True, WHITE)
        self.image.blit(cheevo_card_text_surf, (5, 5)) # top right of the bg rect
        # achievement value subtext
        cheevo_subtext_surf = self.game.FONT_SILK_REGULAR_14.render("if you undo i wont tell anyone dw", True, WHITE)
        cheevo_subtext_width, cheevo_subtext_height = cheevo_subtext_surf.get_width(), cheevo_subtext_surf.get_height()
        self.image.blit(cheevo_subtext_surf, ((self.rect.width / 2) - (cheevo_subtext_width / 2), (self.rect.height / 2) - (cheevo_subtext_height / 2) + 15)) # one extra height to have it be a header
        self.game.screen.blit(self.image, self.rect)
        