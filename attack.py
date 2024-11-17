from pico2d import *
import game_world

class PlayerATKMonster:
    def __init__(self, x, y, size_x, size_y):
        self.x, self.y= x, y
        self.size_x, self.size_y = size_x, size_y
        self.current = get_time()
    def draw(self):
        draw_rectangle(*self.get_bb())
    def update(self):
        if get_time() - self.current > 2:
            game_world.remove_object(self)
        pass
    def get_bb(self):
        return self.x - self.size_x//2, self.y - self.size_y//2, self.x + self.size_x//2, self.y + self.size_y//2
    def handle_collision(self, group, other):
        if group == 'playerATK:monster':
            game_world.remove_object(self)