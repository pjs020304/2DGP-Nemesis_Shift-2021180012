from pico2d import *
import game_world
import play_mode
import player
import game_framework

class PlayerATKMonster:
    def __init__(self, x, y, size_x, size_y):
        self.x, self.y= x, y
        self.size_x, self.size_y = size_x, size_y
        self.current = get_time()
    def draw(self):
        if play_mode.collider_trig:
            draw_rectangle(*self.get_bb())
    def update(self):
        if get_time() - self.current > 0.3:
            game_world.remove_object(self)
        pass
    def get_bb(self):
        return self.x - self.size_x//2, self.y - self.size_y//2, self.x + self.size_x//2, self.y + self.size_y//2
    def handle_collision(self, group, other):
        if group == 'playerATK:monster' and other.state != 'Die':
            game_world.remove_object(self)



class MonsterATKPlayer:
    def __init__(self, x, y, size_x, size_y):
        self.x, self.y= x, y
        self.size_x, self.size_y = size_x, size_y
        self.current = get_time()
    def draw(self):
        if play_mode.collider_trig:
            draw_rectangle(*self.get_bb())
    def update(self):
        if get_time() - self.current > 0.3:
            game_world.remove_object(self)
        pass
    def get_bb(self):
        return self.x - self.size_x//2, self.y - self.size_y//2, self.x + self.size_x//2, self.y + self.size_y//2
    def handle_collision(self, group, other):
        if group == 'monsterATK:player':
            game_world.remove_object(self)


class MonsterFarATKPlayer:
    def __init__(self, x, y, size_x, size_y):
        self.x, self.y= x, y
        self.size_x, self.size_y = size_x, size_y
        self.current = get_time()
        self.image = load_image('Resource\\Dusk Bomb.png')
        self.frame=0
    def draw(self):
        self.image.clip_draw(int(self.frame) * 31, 0, 31, 38, self.x,
                             self.y, self.size_x, self.size_y)
        if play_mode.collider_trig:
            draw_rectangle(*self.get_bb())
    def update(self):
        self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - self.current > 0.5:
            game_world.remove_object(self)
        pass
    def get_bb(self):
        return self.x - self.size_x//2, self.y - self.size_y//2, self.x + self.size_x//2, self.y + self.size_y//2
    def handle_collision(self, group, other):
        if group == 'monsterFarATK:player' and get_time() - self.current > 0.2:
            game_world.remove_object(self)
            other.hp -= 1
            other.y += 30
            other.vertical += 10
            other.fall = True