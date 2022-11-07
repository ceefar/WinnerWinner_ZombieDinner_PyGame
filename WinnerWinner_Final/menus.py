from settings import *

class PlayerInventoryMenu(pg.sprite.Sprite): # ideally would do a parent menu class just havent got round to it yet... also should rename to just inventory menu, and also should be snake_case, oh the shame XD
    def __init__(self, game, inventory_info, the_lootable=0): # new default param on the_lootable allows us to blit this without having to have a lootable box near by (tho need to update appropriate mouse click functions if this is opened by pressing key i for inventory)
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
        # -- now an optional parameter --
        self.the_lootable = the_lootable # need to handle when this isn't passed as a parameter

    def draw_inventory_styling(self):
        """ basically just drawing the header """
        # setup title text surf and header offset position
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
        # centralise the text
        header_destination = destination.copy()
        header_destination.move_ip(5, 3)
        # finally blit directly to the screen, not to the surface, because i want the surface to have a slight alpha channel value and the text wont
        self.game.screen.blit(header_bg_surf, destination)
        self.game.screen.blit(header_text_surf, header_destination)

    def update(self):
        self.item_rects = [] # save the rects now so we dont have to loop every instance of the class (could be done better with a game. var duh)
        # for each item 
        for i, (id, item) in enumerate(self.inventory_dict.items()):
            # first handle any stacking objects
            # need to start doing inventory dict but just do this very first part as list first ok bosh
            # - but wont be passing stuff like uber gold so urm yeah just ig do from ground up basically 
            if item["loot_type"] == "gold": 
                pass # literally just guna have different text, the difficult part is the stacking on click lol so do that first duh

            box_height = 46
            item_title = item["loot_name"]
            item_subtext = item["loot_value"]
            name_textsurface = self.game.FONT_SILK_REGULAR_16.render(f"{item_title}", True, WHITE)
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
        # blit the whole menu
        destination = pg.rect.Rect(self.pos.x, self.pos.y, self.length, self.height)
        self.game.screen.blit(self.image, self.game.camera.apply_rect(destination))




    # so im starting with gold only!
    # - i think have gold be just called uber gold if its a rarer large gold
    # - and inventory gold just stacks as its own kinda seperate ting since you always have gold even if its 0 bosh
    
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

    # def check_click_alt(self, mouse):
    #     for i, rect in enumerate(self.item_rects):
    #         rect = self.game.camera.apply_rect(rect)
    #         if rect.collidepoint(mouse):
    #             return(str(i), self.the_lootable.my_id)



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