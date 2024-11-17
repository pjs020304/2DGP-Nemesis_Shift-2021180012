from pico2d import *
import play_mode
import game_framework
import player

class Monster:
    def __init__(self, frame_x, action_y, width, height,frame_count, position_x, position_y, size_x, size_y, max_x, min_x):
        self.x, self.y = position_x, position_y
        self.frame, self.action = frame_x, action_y
        self.width, self.height = width, height
        self.frame_count = frame_count
        self.dir = 1
        self.size_x, self.size_y = size_x, size_y
        self.max_x, self.min_x = max_x, min_x

        self.state = 'Idle'
    def update(self):
        if self.state != 'Die':
            self.x += self.dir * player.RUN_SPEED_PPS * game_framework.frame_time
            self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time) % self.frame_count
        if play_mode.player.dir == 1:
            if play_mode.player.x >= 700:
                self.x -= player.RUN_SPEED_PPS * game_framework.frame_time
                self.max_x-=player.RUN_SPEED_PPS * game_framework.frame_time
                self.min_x-=player.RUN_SPEED_PPS * game_framework.frame_time
        elif play_mode.player.dir == -1:
            if play_mode.player.x <= 300:
                self.x += player.RUN_SPEED_PPS * game_framework.frame_time
                self.max_x+=player.RUN_SPEED_PPS * game_framework.frame_time
                self.min_x+=player.RUN_SPEED_PPS * game_framework.frame_time

        if self.x >= self.max_x or self.x <= self.min_x:
            self.dir = self.dir*(-1)
    def handle_event(self, event):
        pass
    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * self.width, self.action * self.height, self.width, self.height, self.x, self.y, self.size_x, self.size_y)
        else:
            self.image.clip_composite_draw(int(self.frame) * self.width, self.action * self.height, self.width, self.height,0,'h', self.x, self.y, self.size_x, self.size_y)
        if play_mode.collider_trig:
            draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x-self.size_x//5, self.y-self.size_y//4, self.x+self.size_x//5, self.y+self.size_y//4




class Panda(Monster):
    def __init__(self, frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x):
        super().__init__(frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x)
        self.image = load_image('Tiny Panda Evil Version 103x33.png')
        self.run_action = 12
        self.basic_atk_action= 3
        self.skill_atk_action = 6
        self.basic_atk_size_x, self.basic_atk_size_y = 130, 50
        self.skill_atk_size_x, self.skill_atk_size_y = 180, 100
        self.fall_action = 11
        self.idle_action = 13
        self.png = 'Tiny Panda Evil Version 103x33.png'
    def update(self):
        self.action = 12
        super().update()

        if self.state == 'Basic_Attack':
            self.action = 4
            self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time)
            if self.frame >=4:
                self.state = 'Idle'

        elif self.state == 'Die':
            self.action = 0
            if int(self.frame) <=8:
                self.frame = self.frame + player.FRAMES_PER_ACTION/4 * player.ACTION_PER_TIME * game_framework.frame_time



    def handle_collision(self, group, other):
        if group == 'playerATK:monster':
            self.state = 'Die'
            self.dir = 0