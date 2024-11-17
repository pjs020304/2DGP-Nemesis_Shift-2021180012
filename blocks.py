from pico2d import *
import play_mode
import player
import game_framework

class Block:
    def __init__(self, frame_x, action_y, width, height, position_x, position_y, size_x, size_y):
        self.frame, self.action =frame_x, action_y
        self.width, self.height = width, height
        self.x, self.y = position_x, position_y
        self.size_x, self.size_y = size_x, size_y

        # self.image = load_image('DARK Edition Tileset No background.png')
        self.image = load_image('DARK Edition Tileset No background.png')

    def update(self):
        if play_mode.player.dir == 1:
            if play_mode.player.x >= 700:
                self.x -= player.RUN_SPEED_PPS * game_framework.frame_time
        elif play_mode.player.dir == -1:
            if play_mode.player.x <= 300:
                self.x += player.RUN_SPEED_PPS * game_framework.frame_time

        pass
    def draw(self):
        self.image.clip_draw(self.frame, self.action, self.width, self.height, self.x, self.y, self.size_x, self.size_y)
        if play_mode.collider_trig:
            draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - self.size_x // 2 + 20, self.y, self.x + self.size_x // 2-20, self.y + self.size_y // 4
    def handle_collision(self, group, other):
        if group == 'player:block':
            pass