import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from sprites import collide_with_walls, Bullet, MuzzleFlash
from itertools import chain

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        # -- shooting --
        self.last_shot = 0
        self.weapon = 'pistol'
        # -- health --
        self.health = PLAYER_HEALTH
        self.damaged = False
        # -- actions x inventory --
        self.charging = 0
        self.player_inventory = {0:{"loot_name":"gold", "loot_type":"gold", "loot_value":69, "loot_rarity":1}} # image, rect etc # {loot_id:{loot_info/details}, etc} ['Uber Gold - $585', 'Epic Item - legendary'] 
        # -- skills x abilities --
        self.default_skill_points = {"lockpicking": 3} # default is 3 for lockpicking as we use it comparative to seconds for opening things, works well as is especially as a start value vs other items rarity x unlock difficulty tbf (i.e. 7 second lock, player has a 3 second unlock skill - note we may or may not buffer this, taking away the player unlock time from the actual time)
        self.lockpicking_skill_points = 4  # would convert skills and abilities to a player dictionary too, or class, as it could become sizeable but opting for simpler implementation for this first time pygame project
    
    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        # -- movement input --
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        # -- action input --
        if keys[pg.K_e]:
            # -- make this a function - handle_unlock --
            unlock_speed_bonus = self.lockpicking_skill_points % self.default_skill_points["lockpicking"] # for every point over the default you get a bonus to the unlock speed
            unlock_speed = 2 # can use this as a toggle for god mode / dev mode - default is 1
            if unlock_speed_bonus: # is greater than or equal to 1 but not 0
                self.charging += unlock_speed + int(unlock_speed / 10) # plus 10% extra speed for each skill point in lockpicking
            else:
                self.charging += unlock_speed # swerve the zero div error preemptively
        else:
            if self.charging:  # empty it if it isnt being charged but it hasnt filled up yet, charging here is the amount charged as int not a boolean
                if self.charging <= self.game.current_lock_time: # this is the difficulty time of the currently selected lootbox "lock" - aka lock_diff_time
                    self.charging -= 1
        if keys[pg.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game, pos)

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

