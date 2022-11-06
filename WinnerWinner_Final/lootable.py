# -- imports --
from settings import *
from random import randint, choice, choices
   
# to finish up
#   - have actually unlocking again
#   - this means blit chargebar too
#   - make sure u clean up and bs and delete bs too, dw have copies / make copies 
# then 
#   - pure bosh straight into our new menu stuff
#   - starting out being sure we have the dict all sorted properly to work flawlessly when passing n deleting
#   - NOT OPTIONAL!!! => with attention now to undo, delete, stacking, and consuming        
#   - remember loot needs shit like its id, rarity, type, etc
#   - and note do want items like clothing so might be worth a quick inclusion
#   - and even stuff i havent done yet that i want like rarity too
#       - and a simple randomiser for the value based on rarity too 
#       - do we then pass the box rarity, yes we must so there we go u gotta think first lol
#       - pseudocode it pls

# obvs chunk up this init into relevant functions once got it all wrapped up
class Lootable(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        # -- general setup --
        self._layer = ITEMS_LAYER # need to sort the layering for this and the menus tbf, likely own layer
        self.groups = game.lootables, game.all_sprites, game.walls # confirm if we want/need all of these here btw
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y)        
        self.my_id = len(game.lootables) + 1
        # -- lookup dictionary --
        self.lootboxes_setup = {"small":[ # "Mini Fridge","School Backpack", "Amazon Package","Small Briefcase"
                                            {"visual_type":"work briefcase", "image":self.game.lootbox_small_1_img, "lrg_image":self.game.lootbox_small_1_large_img, "size_range":(1,6), "rarity_range":(3,8)},
                                            {"visual_type":"luxury shopping bag", "image":self.game.lootbox_small_2_img, "lrg_image":self.game.lootbox_small_2_large_img, "size_range":(1,4), "rarity_range":(5,8)},
                                            {"visual_type":"lunchbox", "image":self.game.lootbox_small_3_img, "lrg_image":self.game.lootbox_small_3_large_img, "size_range":(1,4), "rarity_range":(1,3)},
                                            {"visual_type":"kids backpack", "image":self.game.lootbox_small_4_img, "lrg_image":self.game.lootbox_small_4_large_img, "size_range":(1,5), "rarity_range":(1,4)},
                                            {"visual_type":"toolbox", "image":self.game.lootbox_small_5_img, "lrg_image":self.game.lootbox_small_5_large_img, "size_range":(1,5), "rarity_range":(1,5)},
                                            {"visual_type":"picnic basket", "image":self.game.lootbox_small_6_img, "lrg_image":self.game.lootbox_small_6_large_img, "size_range":(1,6), "rarity_range":(1,3)}
                                        ]
                                }                 
        # -- rarity --
        # needed before everything else         
        self.rarities = {"trash":{"diff_buffer":400, "colour":TAN},"basic":{"diff_buffer":320, "colour":SKYBLUE},"uncommon":{"diff_buffer":25, "colour":LIME},"fancy":{"diff_buffer":20, "colour":PURPLE},"uber-rare":{"diff_buffer":15, "colour":BLUEGREEN},"epic":{"diff_buffer":10, "colour":YELLOW},"legendary":{"diff_buffer":5, "colour":MAGENTA},"god-tier":{"diff_buffer":0, "colour":CYAN}}
        self.rarity = choices(list(self.rarities.keys()), weights=[8,15,12,10,5,3,2,1], k=1)[0] # returns a list so just set it to the 0 index here so we get just the string
        self.rarity_int = list(self.rarities.keys()).index(self.rarity) # of 8, zero indexed (so 7)
        self.rarity_colour = self.get_rarity_colour()
        # we also use the size to confirm which type of loot to get so we need to do this first too
        self.my_size = randint(1,6) # actually decided to keep size completely random and not reliant on other variables (as was considering direct rarity relationship)
        # -- core lootable setup -- 
        if type == "lootable_box_small":
            potential_lootboxes = [] # getting the potential lootboxes that are available for our randomly set rarity
            # print(f"{self.my_size = }  {self.rarity_int = }")
            for lootbox_config in self.lootboxes_setup["small"]:
                # print(f"{lootbox_config = }")
                if self.rarity_int >= lootbox_config["rarity_range"][0] and self.rarity_int <= lootbox_config["rarity_range"][1]:
                    if self.my_size >= lootbox_config["size_range"][0] and self.my_size <= lootbox_config["size_range"][1]:
                        potential_lootboxes.append(lootbox_config)
            # -- set the base vars from the returned dict, e.g. image, size, type, i.e. lunchbox, toolbox, etc, etc --
            selected_lootbox_info = self.get_lootbox_image_and_type(potential_lootboxes)
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
            self.lockpicking_ability = 300 # obvs want this to be part of a player abilites dictionary that is on the player object but just leaving it here for now      
            self.chargebar_failure_text = choice(["- idk wtf to do here?","- next time check first?", "- lockpicking too low", "- requires `HAMMER`"]) # faux implementation, not intending on doing it properly though it could easily be added in a variety of ways
     

        # to finish up boshhh
        self.my_loot = self.get_a_loot()        


        # increase our unlock speed significantly while in dev mode
        if self.game.draw_debug: 
            self.lock_diff_time = int(self.lock_diff_time / 5) 
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

    def set_lock_difficulty_time(self): # simple addition of randomised element is fine for now but does need to be updated to weighting instead of current implementation
        random_buffer = randint(100, 800 - self.rarities[self.rarity]["diff_buffer"])
        # print(f"{random_buffer = }")
        return random_buffer

    def can_player_open(self):
        return False if self.lock_diff_time > self.lockpicking_ability else True
    
    def get_display_size(self):
        sizes = {1:"tiny", 2:"small", 3:"avg", 4:"avg", 5:"large", 6:"huge"}
        return f"{sizes[self.my_size]}"

    def get_lootbox_image_and_type(self, potential_lootboxes):    
        rng_selection = choice(potential_lootboxes)
        return rng_selection

    def get_lock_difficulty_display(self): # havent done it yet but this should change dynamically once adding updatable skills via skill points without any problems 
        # if the player can open it the display message is based on how long it will take to open, self confessed very rudimentary but it can easily be built on
        adjusted_time_difficulty = self.lockpicking_ability - self.lock_diff_time
        if self.can_player_open():            
            return "Shut : Open" if adjusted_time_difficulty < 50 else "Shut : Jammed"
        else:
            return "Locked : Small Padlock" if adjusted_time_difficulty > -100 else "Locked : Large Padlock"

    def get_rarity_colour(self): 
        return self.rarities[self.rarity]["colour"]                


    # -- in progress --
    def get_a_loot(self):
        loot_list = []
        for _ in range(self.my_size):
            loot_list.append(self.loot_maker(choice(["Baby Gold", "Basic Gold", "Uber Gold", "Nada", "Epic Item", "HP Medkit", "HP Food", "Ammo"])))       
        # print(f"{loot_list = }")
        return loot_list
    

    def draw_lil_line(self):
        start_rect = pg.Rect(self.pos.x, self.pos.y, 10, 10)
        start_rect = self.game.camera.apply_rect(start_rect)
        end_rect = pg.Rect(self.title_destination.x - 2, self.title_destination.y - self.info_box_info_surf.get_height(), 2, 2) 
        # GREEN if self.can_player_open() else RED
        pg.draw.line(self.game.screen, BLUEMIDNIGHT, start_rect.center, end_rect.center, 3) # LIGHTGREY # BLUEMIDNIGHT # self.title_destination.topleft

    # taken fron draw_unit_status, worked as expected tbf but just need to heavily customise this
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
        
    def blit_chargebar(self, pct):
        # setup
        if self.can_player_open():
            chargebar_text = f"- opening..."
        else:
            chargebar_text = self.chargebar_failure_text
        if pct >= 100:
            pct = 100
            if self.can_player_open():
                chargebar_text = f"- open"
            else:
                chargebar_text = f"- oof"
        # actual bar
        chargebar_surf = pg.Surface(((self.info_box_info_surf.get_width() / 100) * pct, self.info_box_info_surf.get_height()))
        chargebar_surf.fill(ORANGE)
        # text with mask effect
        opening_text_surf = self.game.FONT_SILK_REGULAR_12.render(chargebar_text, True, BLACK) # "text", antialias, color
        chargebar_surf.blit(opening_text_surf, (int(self.padding_x/2), int(self.padding_y/2)))
        # blit
        self.game.screen.blit(chargebar_surf, self.title_destination)
            
    def loot_maker(self, loot):
        # aite as this is a test guna now add what i want in final even tho it means there will be some duplication
        if "gold" in loot.lower():
            if "baby" in loot.lower():
                return f"{loot} - ${randint(10,50)}"       
            elif "basic" in loot.lower():
                return f"{loot} - ${randint(50,250)}"
            else:
                return f"{loot} - ${randint(250,1000)}"
        if "hp" in loot.lower():
            if "medkit" in loot.lower():
                medkits = {"large medkit":300, "plasters":50, "bandages":100, "painkillers":250, "small medkit":200} # type : max health (which we will randomise as the range)
                selection = choice(list(medkits.keys()))
                return f"{selection.title()} - {randint(int(medkits[selection] / 4), medkits[selection])}"
            elif "food" in loot.lower():
                foods = {"chocolate":20, "mouldy sandwich":15, "pasta bake":50}
                selection = choice(list(foods.keys()))
                return f"{selection.title()} - {randint(10, foods[selection])}"
        else:
            return f"{loot} - {self.rarity[0]}"
                