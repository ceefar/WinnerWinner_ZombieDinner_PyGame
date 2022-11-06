import pygame as pg
from random import choice, random, randint # , uniform
from settings import *
from sprites import collide_with_walls
vec = pg.math.Vector2


class Zombie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # -- object shapes and images --
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        # -- movement --
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player
        # -- practically finalised --
        self.vision_detect_radius = 300
        self.my_name = self.get_first_name()
        self.my_id = len(self.game.mobs) + 1
        # -- power level & experience --
        self.power_level = self.set_power_level() # important! => starting health is reliant on power_level
        # -- health --
        base_min_hp_amount, base_max_hp_amount = 200, 300 # likely remain constants
        self.max_hp_amount, self.min_hp_amount = self.adjust_hp_for_level(base_max_hp_amount), self.adjust_hp_for_level(base_min_hp_amount)
        self.max_health = round_to_base(self.set_initial_health()) # adds a randomised element to the zombie hp based on its level, then rounds it to 5
        self.current_health = self.max_health     
        # -- status and other ui --
        self.my_status = self.get_status()
        
    # -- OG --

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < self.vision_detect_radius ** 2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.current_health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))

    # -- Mob UI & Other Functions

    def get_first_name(self): 
        list_of_names = ["Zob", "Zenjamin", "Zames", "Zohn", "Zichard", "Zhomas", "Zhristopher", "Zaniel", 
                            "Znthony", "Zucian", "Zeo", "Zathan", "Zoby", "Zean", "Zim", "Zteven", "Zosh", "Zohnathon", "Zyson", "Zo", "Zike", "Zohnny", "Zanny"]
        return choice(list_of_names)

    def draw_unit_name(self): 
        # put all these offset x/y things into one function duh
        offset_x, offset_y = int(TILESIZE/2) + int(TILESIZE/2), int(TILESIZE/2) - 10
        x, y = self.pos.x + offset_x, self.pos.y -  offset_y
        self.name_textsurface = self.game.FONT_SILK_REGULAR_14.render(f"{self.my_name}", True, WHITE) # "text", antialias, color 
        test_rect = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_rect(test_rect).copy()
        destination.move_ip(2, -20) # better way to handle moving things btw donkey!, also btw, ip = in place
        self.game.screen.blit(self.name_textsurface, destination)
       
    def get_status(self): 
        # just as temp af rn so can randomise the status just to see how the display will look at certain char widths, not intended to be planned implementation of statuses
        list_of_statuses = ["Roaming", "Hunting",f"{self.speed}kph", f"{self.speed}mph"]
        return choice(list_of_statuses) 

    def draw_unit_status(self): 
        offset_x, offset_y = int(TILESIZE/2) + int(TILESIZE/2), int(TILESIZE/2) + 20
        x, y = self.pos.x + offset_x, self.pos.y -  offset_y
        # set the status to be a string with commas if it is a list, else its just the given string
        status = self.my_status if isinstance(self.my_status, str) else ", ".join(self.my_status)
        self.name_textsurface = self.game.FONT_SILK_REGULAR_10.render(f"{status}", True, RED) # "text", antialias, color
        destination = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_rect(destination).copy()
        self.game.screen.blit(self.name_textsurface, destination)

    # 100% want this stuff to be in a unit parent class
    def draw_unit_level(self): # [CUSTOM]
        UNIT_LEVEL_BOX_SIZE = 28  
        offset_x, offset_y = int(TILESIZE/2), int(TILESIZE/2) + 1
        x, y = self.pos.x + offset_x, self.pos.y -  offset_y
        offset_text = ((UNIT_LEVEL_BOX_SIZE/2 - 6), 1) # centralises the int level text inside the box
        self.level_textsurface = self.game.FONT_SILK_REGULAR_18.render(f"{self.power_level}", True, WHITE) # "text", antialias, color
        # note this should be slightly bigger than the unit health bar size btw so when hardcoding do this properly, aka dynamic from it
        level_box_fill = pg.Rect(x, y, UNIT_LEVEL_BOX_SIZE, UNIT_LEVEL_BOX_SIZE)
        level_box_outline_rect = pg.Rect(x, y, UNIT_LEVEL_BOX_SIZE, UNIT_LEVEL_BOX_SIZE)
        # before we draw it apply the camera to it
        level_box_fill = self.game.camera.apply_rect(level_box_fill).copy()
        level_box_outline_rect = self.game.camera.apply_rect(level_box_outline_rect).copy()
        # then draw to screen
        pg.draw.rect(self.game.screen, BLUEMIDNIGHT, level_box_fill)
        pg.draw.rect(self.game.screen, DARKGREY, level_box_outline_rect, 3)
        # finally draw the actual number representing this unit/zombies level in that box
        destination = pg.Rect(x, y, 300, 100) # a temporary rect to store the x, y positions we want to be at, so we can adjust it for the camera
        destination = self.game.camera.apply_rect(destination).copy()
        destination.move_ip(offset_text) # then do an additional nudge to centralise the text
        self.game.screen.blit(self.level_textsurface, destination)

    # -- Zombie Health & HP UI Functions --

    def draw_unit_health(self):
        # create the rectangles we need for drawning the hp bars based on the percent, returns that percent too so we can apply color to the surface (and also use alpha as we go for a surf here instead of a rect for this exact reason)
        outline_rect, background_rect, health_remaining_percent = self.create_health_bar_rects()
        col = GREEN if health_remaining_percent >= 0.6 else YELLOW if health_remaining_percent >= 0.3 else RED # green -> yellow -> red based on rougly even percentages, may add a proper gradient here at some point
        # !!!!!! =>> should make the below stuff a function and pass it a list
        background_rect = self.game.camera.apply_rect(background_rect, return_copy=True) # make our new backgrounds of our the created rects, 
        outline_rect = self.game.camera.apply_rect(outline_rect, return_copy=True) # then move these bars based on the cameras position too, ensure we use copies as multiple zombie instances using same img - the apply rect funct does this already  
        background_surf = pg.Surface((outline_rect.width, outline_rect.height))
        hp_bar_surf = pg.Surface((background_rect.width, background_rect.height))
        self.handle_hp_bar_alpha() # soon to be implemented based on clumping 
        self.alpha_colour_surfs([background_surf, hp_bar_surf], [LIGHTGREY, col], [140, 255]) # colour the surfs
        self.handle_unit_debug_display(background_rect)
        # draw the health segements (50,100,150...) onto the zombie hp bars
        self.draw_segments(background_surf, hp_bar_surf)
        # then draw the hp bars onto the screen
        self.game.screen.blit(background_surf, background_rect)                      
        self.game.screen.blit(hp_bar_surf, background_rect)
        # finally draw an outline rect around the entire thing to keep it clean
        pg.draw.rect(self.game.screen, DARKGREY, outline_rect, 2)

    def adjust_hp_for_level(self, base_hp_amount):
        """ adjusts the zombies hp based on its level, which scales as the game progresses through days (over time)
            usage is accepted for either mix or max, it doesnt matter the calculation is the same, base amount is constant """ 
        level_adjusted_hp = base_hp_amount + (50 * (self.power_level - 1)) # -1 so at level 1 there is no additional bonus, can be altered
        return level_adjusted_hp

    def set_initial_health(self): 
        """ adds a slight randomised element to the zombie hp from their initial hp which is set based on level """
        random_hp = randint(self.min_hp_amount, self.max_hp_amount)
        # if not more than a 50% increase, set it to the min/floor value to give game difficuly more consistency 
        return random_hp if random_hp >= self.min_hp_amount * 1.2 else self.min_hp_amount 

    def set_power_level(self):
        """ note zombie level affects zombie starting hp, leaving as a function as planning to improve this eventually """
        return randint(1,5)

    def draw_segments(self, background_surf, hp_bar_surf):
        # loop to draw the segments, which are stubby split indicator bars between to show blocks/chunks of hp 
        for i in range(int(self.BAR_SEGMENT_COUNT)):
            # if the segment would be placed at the very end of the bar (5% buffer to the end), due to border and small width placing it outside the outline rect, then dont place it outside the rect)
            if not int(self.SEGMENT_LENGTH * (i+1)) >= ((MOB_HEALTH_BAR_LENGTH / 100) * 95): 
                # for segment bar height have longer/shorter for the 50s units and then 100s units seperately
                segment_height = 2.5 if i % 2 == 0 else 1.8 # it is even make it longer
                segment_rect = pg.Rect((self.SEGMENT_LENGTH * (i+1)), 0, 2, (MOB_HEALTH_BAR_HEIGHT / segment_height)) # for width -> 2 = thin, 1 = waffer thin, 4 = pretty chunky 
                # draw the segment lines directly onto the surface of both the foreground health bar and the alpha altered background bar for a nice effect
                pg.draw.rect(background_surf, DARKGREY, segment_rect, 2)   
                pg.draw.rect(hp_bar_surf, DARKGREY, segment_rect, 2) 

    def create_health_bar_rects(self):
        """ does all the tedious formatting of shapes n stuff, setting the health bar to the percent based on max hp vs current hp, etc, etc """ 
        # how much to offset the position of the unit health bar in relation to the unit surface, this sets it to up right of the sprite
        offset_x, offset_y = int(TILESIZE/2) + int(TILESIZE/2), int(TILESIZE/2) - 10 
        x, y = self.pos.x + offset_x, self.pos.y -  offset_y
        self.BAR_SEGMENT_COUNT = self.max_health / HP_BAR_HP_SEGMENT # hard coded so we dont run over and print a tiny bar at the end that looks stupid
        self.SEGMENT_LENGTH = MOB_HEALTH_BAR_LENGTH / self.BAR_SEGMENT_COUNT # set the x segments even based on the BAR_SEGMENT_HP e.g. 50, 100, 150 for 175 hp
        if self.current_health < 0: # in cases when we pass a negative, pin it at 0 so it doesnt go under
            self.current_health = 0 # calculate the percentage of hp remaining and convert it based on the bar size
        health_remaining_percent = self.current_health / self.max_health
        fill = MOB_HEALTH_BAR_LENGTH * health_remaining_percent
        # define the inner fill rect and outer outline rect objects that will be drawn to create the hp bar
        outline_rect = pg.Rect(x, y, MOB_HEALTH_BAR_LENGTH, MOB_HEALTH_BAR_HEIGHT)
        background_rect = pg.Rect(x, y, fill, MOB_HEALTH_BAR_HEIGHT)
        return outline_rect, background_rect, health_remaining_percent

    def handle_hp_bar_alpha(self):
        ...        
        # if self.my_id in self.game.clumping_mobs:
        #     s.set_alpha(50)    
        # else:
        #     s.set_alpha(255) 

    def alpha_colour_surfs(self, surfaces:list, colours:list, alphas:list):
        for surf, clr, alp in zip(surfaces, colours, alphas):
            surf.set_alpha(alp)
            surf.fill(clr)

    def handle_unit_debug_display(self, background_rect):
        if self.game.draw_debug:
            offset_x = background_rect.x - 50
            self.game.draw_text_alt(f"info: {self.my_id} {self.my_name}", self.game.FONT_SILK_REGULAR_10, DARKGREY, offset_x, background_rect.y - 5)
            self.game.draw_text_alt(f"hp: {self.current_health} {self.max_health}", self.game.FONT_SILK_REGULAR_10, DARKGREY, offset_x, background_rect.y - 25)  


    

