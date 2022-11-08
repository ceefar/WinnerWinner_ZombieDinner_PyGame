# -- imports --
from settings import *
from random import randint, choice, choices
   
   
class Lootable(pg.sprite.Sprite):
    loot_counter = 220 # for counting every individual piece of loot created at any given lootable

    def __init__(self, game, x, y, type):
        # -- general setup --
        self._layer = ITEMS_LAYER # need to sort the layering for this and the menus tbf, likely own layer
        self.groups = game.lootables, game.all_sprites, game.walls # confirm if we want/need all of these here btw
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)        
        self.my_id = len(game.lootables) + 1
        # -- lookup dictionary --
        self.lootboxes_setup = {"small":[ # "Mini Fridge","School Backpack", "Amazon Package","Small Briefcase"...
                                            {"visual_type":"work briefcase", "image":self.game.lootbox_small_1_img, "lrg_image":self.game.lootbox_small_1_large_img, "size_range":(1,6), "rarity_range":(3,8)},
                                            {"visual_type":"luxury shopping bag", "image":self.game.lootbox_small_2_img, "lrg_image":self.game.lootbox_small_2_large_img, "size_range":(1,4), "rarity_range":(5,8)},
                                            {"visual_type":"lunchbox", "image":self.game.lootbox_small_3_img, "lrg_image":self.game.lootbox_small_3_large_img, "size_range":(1,4), "rarity_range":(1,3)},
                                            {"visual_type":"kids backpack", "image":self.game.lootbox_small_4_img, "lrg_image":self.game.lootbox_small_4_large_img, "size_range":(1,5), "rarity_range":(1,4)},
                                            {"visual_type":"toolbox", "image":self.game.lootbox_small_5_img, "lrg_image":self.game.lootbox_small_5_large_img, "size_range":(1,5), "rarity_range":(1,5)},
                                            {"visual_type":"picnic basket", "image":self.game.lootbox_small_6_img, "lrg_image":self.game.lootbox_small_6_large_img, "size_range":(1,6), "rarity_range":(1,3)}
                                        ]}                 
        # -- rarity --
        # needed before everything else         
        self.rarities = {"trash":{"diff_buffer":400, "colour":TAN},"basic":{"diff_buffer":320, "colour":SKYBLUE},"uncommon":{"diff_buffer":25, "colour":LIME},"fancy":{"diff_buffer":20, "colour":PURPLE},"uber-rare":{"diff_buffer":15, "colour":BLUEGREEN},"epic":{"diff_buffer":10, "colour":YELLOW},"legendary":{"diff_buffer":5, "colour":MAGENTA},"god-tier":{"diff_buffer":0, "colour":CYAN}}
        self.rarity = choices(list(self.rarities.keys()), weights=[8,15,12,10,5,3,2,1], k=1)[0] # returns a list so just set it to the 0 index here so we get just the string
        self.rarity_int = list(self.rarities.keys()).index(self.rarity) + 1 # of 8, zero indexed (so 7), so + 1
        self.rarity_colour = self.get_rarity_colour()
        # we also use the size to confirm which type of loot to get so we need to do this first too
        self.my_size = randint(1,6) # actually decided to keep size completely random and not reliant on other variables (as was considering direct rarity relationship)
        # -- core lootable setup -- 
        if type == "lootable_box_small":
            potential_lootboxes = [] # getting the potential lootboxes that are available for our randomly set rarity
            for lootbox_config in self.lootboxes_setup["small"]:
                if self.rarity_int >= lootbox_config["rarity_range"][0] and self.rarity_int <= lootbox_config["rarity_range"][1]:
                    if self.my_size >= lootbox_config["size_range"][0] and self.my_size <= lootbox_config["size_range"][1]:
                        potential_lootboxes.append(lootbox_config)
            # -- set the base vars from the returned dict, e.g. image, size, type, i.e. lunchbox, toolbox, etc, etc --
            try:
                selected_lootbox_info = self.get_lootbox_image_and_type(potential_lootboxes)
            except IndexError as ndxErr:
                print(f"{ndxErr}\n{self.my_size}, {self.rarity_int}")
            if self.my_size >= 5:
                self.image = selected_lootbox_info["lrg_image"]
            else:
                self.image = selected_lootbox_info["image"]
            self.my_type = selected_lootbox_info["visual_type"]
            self.display_name = f"{self.get_display_size()} {self.my_type}".title()
            self.my_size = randint(selected_lootbox_info["size_range"][0], selected_lootbox_info["size_range"][1])
            # -- rect setup stuff --
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.hit_rect = self.rect # used for drawing dev mode debug display so dont remove though isnt really used                       
            # -- lootable unlock stuff --
            self.lock_diff_time = self.set_lock_difficulty_time()  
            self.chargebar_failure_text = choice(["- idk wtf to do here?","- next time check first?"]) # previous faux implementation with "requires HAMMER" removed, not intending on doing it properly though it could easily be added in a variety of ways


        # to finish up boshhh
        self.my_loot = self.get_a_loot()
        [print(f"{a_id = } : {a_loot = }") for a_id, a_loot in self.my_loot.items()]     
        # do the unpack stuff here as own function bosh


        if self.game.draw_debug: 
            print(f"Debuggy:\n{self.my_id = } {self.rarity = }\n{self.my_type = } {self.rarity_int = }\n{selected_lootbox_info = } {self.lock_diff_time = }\n{self.display_name = }")

    # -- basically finalised --
    def outline_mask(self, img, loc, thickness=3, colr=WHITE):
        mask = pg.mask.from_surface(img)
        mask_outline = mask.outline()
        n = 0
        for point in mask_outline:
            mask_outline[n] = point[0] + loc[0], point[1] + loc[1]
            n += 1
        pg.draw.polygon(self.game.screen, (colr), mask_outline, thickness)  

    def set_lock_difficulty_time(self): # to want to update this to weighting instead of current implementation so it better covers the high range and actually covers the low range (which we dont right now, which is fine tbf but ideally i would like it updated)
        random_buffer = randint(100, 800 - self.rarities[self.rarity]["diff_buffer"]) # we are having long unlock timers as we want to increase the zombie alert range when the player is unlocking lootboxes (with the potential to add a noise_level variable to these lootboxes in future)
        return random_buffer

    def can_player_open(self):
        return False if self.lock_diff_time > (self.game.player.lockpicking_skill_points * 100) else True
    
    def get_display_size(self):
        sizes = {1:"tiny", 2:"small", 3:"avg", 4:"avg", 5:"large", 6:"huge"}
        return f"{sizes[self.my_size]}"

    def get_lootbox_image_and_type(self, potential_lootboxes):    
        rng_selection = choice(potential_lootboxes)
        return rng_selection

    def get_lock_difficulty_display(self): # if the player can open it the display message is based on how long it will take to open, self confessed very rudimentary but it can easily be built on
        adjusted_time_difficulty = (self.game.player.lockpicking_skill_points * 100) - self.lock_diff_time # essentially the same as can player open, if it is a negative number then the player cant open it
        if self.can_player_open():            
            return f"Shut : {(self.lock_diff_time / 100):.1f} difficulty" if adjusted_time_difficulty < 50 else f"Jammed : {(self.lock_diff_time / 100):.1f} difficulty"
        else:
            return f"Locked Flimsy : +{(adjusted_time_difficulty // 100) * -1} exp" if adjusted_time_difficulty > -100 else f"Locked Tight : +{(adjusted_time_difficulty // 100) * -1} exp"
        
    def get_rarity_colour(self): 
        return self.rarities[self.rarity]["colour"]                

    def draw_lil_line(self):
        start_rect = pg.Rect(self.pos.x, self.pos.y, 10, 10)
        start_rect = self.game.camera.apply_rect(start_rect)
        end_rect = pg.Rect(self.title_destination.x - 2, self.title_destination.y - self.info_box_info_surf.get_height(), 2, 2)         
        pg.draw.line(self.game.screen, BLUEMIDNIGHT, start_rect.center, end_rect.center, 3) # self.title_destination.topleft

    def get_failure_text(self):
        # created a function for this to expand the functionality in future
        return self.chargebar_failure_text

    def blit_chargebar(self, pct):
        # setup the what text will be displayed based on game condtions
        if pct >= 100: # if the bar is fully charged show either open or oof if you've just tried to open a locked lootbox (greater than your skill level)
            pct = 100
            chargebar_text = f"- open" if self.can_player_open() else f"- oof"
        else:
            chargebar_text = f"- opening..." if self.can_player_open() else self.get_failure_text()    
        # the actual charging up bar
        chargebar_surf = pg.Surface(((self.info_box_info_surf.get_width() / 100) * pct, self.info_box_info_surf.get_height()))
        chargebar_surf.fill(ORANGE)
        # create the text with masking effect and blit it to the charging bar surface
        opening_text_surf = self.game.FONT_SILK_REGULAR_12.render(chargebar_text, True, BLACK) # "text", antialias, color
        chargebar_surf.blit(opening_text_surf, (int(self.padding_x/2), int(self.padding_y/2)))
        # blit the charging bar with text on top
        self.game.screen.blit(chargebar_surf, self.title_destination)

    # -- to refactor / optimise --
    def draw_lootable_info(self): 
        x, y = self.pos.x, self.pos.y 
        self.padding_x, self.padding_y = 20, 14
        # text setup
        self.info_box_info_text_surf = self.game.FONT_SILK_REGULAR_12.render(f"- {self.get_lock_difficulty_display()}", True, WHITE) # "text", antialias, color
        self.info_box_header_surf = self.game.FONT_SILK_REGULAR_14.render(f"{self.display_name}", True, WHITE) # "text", antialias, color
        self.info_box_rarity_surf = self.game.FONT_SILK_REGULAR_14.render(f"{self.rarity}", True, BLUEMIDNIGHT) # "text", antialias, color
        text_rect = pg.Rect(x, y, self.info_box_header_surf.get_width() + self.padding_x, self.info_box_header_surf.get_height() + self.padding_y) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        rarity_text_rect = pg.Rect(x, y, self.info_box_rarity_surf.get_width() + self.padding_x, self.info_box_rarity_surf.get_height() + self.padding_y) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        # positioning
        in_place_move = 40, -70 
        rarity_move = text_rect.width, 0
        title_in_place_move = 0, text_rect.height
        destination = self.game.camera.apply_rect(text_rect)
        destination.move_ip(in_place_move)
        rarity_destination = destination.copy()
        rarity_destination.move_ip(rarity_move)
        self.title_destination = destination.copy()
        self.title_destination.move_ip(title_in_place_move)
    	# blit header part
        info_box_header_bg_surf = pg.Surface((text_rect.width, text_rect.height))
        info_box_header_bg_surf.fill(BLUEMIDNIGHT)
        info_box_header_bg_surf.blit(self.info_box_header_surf, (int(self.padding_x/2), int(self.padding_y/2)))
        self.game.screen.blit(info_box_header_bg_surf, destination)
        # blit header rarity part
        info_box_rarity_bg_surf = pg.Surface((rarity_text_rect.width, rarity_text_rect.height))
        rarity_clr = self.rarity_colour
        info_box_rarity_bg_surf.fill(rarity_clr) 
        info_box_rarity_bg_surf.blit(self.info_box_rarity_surf, (int(self.padding_x/2), int(self.padding_y/2)))
        self.game.screen.blit(info_box_rarity_bg_surf, rarity_destination)        
        # blit info part
        self.info_box_info_surf = pg.Surface((text_rect.width + rarity_text_rect.width, text_rect.height)) # + rarity_text_rect.height
        self.info_box_info_surf.fill(LIGHTGREY)
        self.info_box_info_surf.set_alpha(190)
        self.info_box_info_surf.blit(self.info_box_info_text_surf, (int(self.padding_x/2), int(self.padding_y/2)))
        self.game.screen.blit(self.info_box_info_surf, self.title_destination)
        # little line that connects the box to the menu it shows
        self.draw_lil_line()


    # -- in progress --


    # first need to have unlocking tbf then can do below
    # - loot id (unique identifier)
    # - rarity
    # - loot type
    #   - consumable hp
    #   - insta hp
    #   - gold
    #   - buff
    #   - ammo
    #   - weapon
    #   - part / collectible 
    #   - clothing
    #   - weapon part / upgrade
    #   - enery drink (is a buff ig?)
    #   - else?
    #   - battery / phone ? (maybe u have to charge it tho ooo)
    # - loot value
    # - position / rect position / array position / which inventory ?

    # foods = {"chocolate":20, "mouldy sandwich":15, "pasta bake":50}
    # medkits = {"large medkit":300, "plasters":50, "bandages":100, "painkillers":250, "small medkit":200}
    # ["Baby Gold", "Basic Gold", "Uber Gold", "Nada", "Epic Item", "HP Medkit", "HP Food", "Ammo"]   
    
    # doing consumable and stackable immediately after its working
    # just leaving here as comment is it worth having them as bools here, is that more efficient or less?
    
    # note have removed sub type

    def get_a_loot(self):
        final_return_dict = {}
        print(f"\n- - - - - - \nCreating New Loot - {self.my_id} {self.my_size} {self.rarity}")
        for _ in range(self.my_size): 
            # create id 
            Lootable.loot_counter += 1
            loot_item_id = Lootable.loot_counter
            loot_item_details_dict = {"loot_id": loot_item_id} # fill this up as we go, its the inner nested dict which is a value to the key id
            # create and add type
            item_types = ["gold", "health", "weapon", "item", "ammo"] # add weightings, move this above or own function whatever
            rng_type = choice(item_types)
            loot_item_details_dict["loot_type"] = rng_type
            # item rect
            loot_item_details_dict["loot_rect"] = False
            # loot rarity
            max_rarity = self.rarity_int + 1 if self.rarity_int < 7 else self.rarity_int # defining this as dont want it to go over and readability gets lost on a single line
            loot_rarity_int = randint(1, max_rarity) # ideally have this weighted to trend closer to the lootboxes actual rarity
            loot_item_details_dict["loot_rarity"] = loot_rarity_int

            print(f"{loot_item_details_dict = }")

            # loot value - is related to this new rarity we've just set, as well as the type, for all of these make own functions anyway but this will suffice for now
            if loot_item_details_dict["loot_type"] == "gold": # ["gold", "health", "weapon", "item", "ammo"]
                adjusted_gold_loot_range = loot_rarity_int * 100 # adjusted based on rarity
                loot_value = randint(50, adjusted_gold_loot_range)
            else:
                # switch to handle current loot types seperately, again own function and will do properly just rushing this bit as is purely cosmetic
                loot_value = "to do"
            loot_item_details_dict["loot_value"] = loot_value
            # loot name - do name and value together, just as seperate functions, but just doing like this for now while finalising concept
            loot_name = f"{loot_item_details_dict['loot_type']} {loot_item_details_dict['loot_id']}" # super super temp implementation for now to get them unique
            loot_item_details_dict["loot_name"] = loot_name
            # finally nest dem all
            loot_item_dict = {loot_item_id: loot_item_details_dict}
            print(f"\n{loot_item_dict = }")   
            final_return_dict[loot_item_id] = loot_item_details_dict
        print(f"\n- - - - - - \n{final_return_dict = }")   
        return final_return_dict

        # {"loot_name":"gold", "loot_type":"gold", "loot_value":420, "loot_rarity":1, "loot_rect": False}
            
