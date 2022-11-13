import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
vec = pg.math.Vector2

# -- some general functions for all sprites --

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

# -- sprite classes --

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1


# basically just have to sort this so its now just running when the button press happens, so probably just rename from update and then have a bool flag to toggle on then stays on until completed (both back and forth, bosh), simple flag like delivery_in_progress or sumnt

# -- quick first test implementation for Delivery Drone... should really rename to Delivery Drone too lol --
class Drone(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites # game.drones
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.start_pos = vec(x, y) # < delete ?!
        # -- object shapes and images --
        # self.image = pg.Surface((30, 30))
        # self.image.fill(MAGENTA)
        self.image = game.drone_img
        self.rect = self.image.get_rect()    
        self.size = self.rect.width
        self.rect.center = (x, y)
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center
        # -- movement --
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.speed = 600
        self.target = game.locker_location
        self.target_dist = self.target.pos - self.pos
        self.rot = self.target_dist.angle_to(vec(1, 0))
        self.arrival_time = False
        self.delivered = False
        self.my_cargo = []
        
    def update(self):
        timed_print = pg.time.get_ticks()
        if timed_print % 10_000 < 50:
            print(f"{self.game.start_delivery = }, {self.delivered = }")
        if self.game.start_delivery:
            self.go_to_target()
            if timed_print % 1_000 < 50:
                print(f"{self.my_cargo[0]['loot_name'] = }")
        else:
            pass

    # dont wanna run this all the time by, take it out of all sprites? 
    def go_to_target(self): 
        timed_print = pg.time.get_ticks()
        if timed_print % 2000 < 50:
            print(f"GO TO TARGET > {self.target_dist.length()}")
        if not self.delivered and not self.game.took_locker_loot: # if you've not delivered it and the user hasnt clicked it > then for take off you'll need another time which you should trigger when the player clicks to take the locker loot...
            if self.target_dist.length() > 85:
                if self.target_dist.length() < 1200:
                    if self.speed > 100:
                        self.speed -= int(self.speed / 50) # 1 percent
                        self.arrival_time = pg.time.get_ticks()
                self.rect.center = self.pos
                self.acc = vec(1, 0).rotate(-self.rot)
                self.acc.scale_to_length(self.speed)
                self.acc += self.vel * -1
                self.vel += self.acc * self.game.dt
                self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                self.hit_rect.centerx = self.pos.x # < probably not needed so delete both ?        
                self.hit_rect.centery = self.pos.y
                self.rect.center = self.hit_rect.center
                self.target_dist = self.target.pos - self.pos
                # print(f"{self.target_dist.length():.0f}, {self.speed = } {self.pos = }, {self.target.pos = }")
            else:
                # should defo be a function so can easily do the reverse too duh            
                check_time = pg.time.get_ticks()
                if check_time - self.arrival_time >= 3500: # short pause to simulate landing / take off
                    if self.image.get_width() > 64:                
                        self.image = pg.transform.scale(self.game.drone_img.copy(), (self.image.get_width() - 0.1, self.image.get_height() - 0.1))
                        if self.image.get_width() <= 66:
                            self.delivered = True
                            self.game.start_delivery = False
                            # need to reset the drone here ig btw 
        elif self.delivered and not self.game.took_locker_loot: # its landed and delivered and now just waiting for the player to collect it, and ig then return take off tho is super unnecessary
            pass
            # self.game.start_delivery = False # reset this once the drone has completed its delivery
        # keep setting the rect center regardless of the outcome in the above switch case
        self.rect.center = vec(self.pos.x - (self.image.get_width() / 2), self.pos.y - (self.image.get_height() / 2))
            
