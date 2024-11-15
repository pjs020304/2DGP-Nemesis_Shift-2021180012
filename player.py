from pico2d import *
import play_mode
import game_framework
# 움직임 속도
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# 액션 속도
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Player:
    def __init__(self):
        self.x, self.y = 400,90
        self.size_x, self.size_y = 120, 120
        self.frame = 0
        self.action = 0
        self.dir = 0
        self.image = load_image('Sci-fi hero 64x65.png')
        # 떨어짐 체크
        self.vertical = 0
        self.fall = False
        self.min_x, self.max_x = 0, 1000

        self.mx, self.my = 0,0
    def update(self):

        if self.dir == -1:
            if self.x >= 300:
                self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            self.action = 11
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        elif self.dir == 1:
            if self.x <= 700:
                self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
            self.action = 11
        else:
            self.action =18
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12

        # 중력 적용
        if self.fall:
            self.y += self.vertical
            self.vertical -= (play_mode.gravity* RUN_SPEED_PPS * game_framework.frame_time)//2
            self.action = 9
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        # 땅과의 충돌 체크


        if self.y <= 90:
            self.y = 90
            self.vertical = 0
            self.fall = False

        if self.x <self.min_x or self.x > self.max_x:
            self.fall = True
            self.min_x, self.max_x = 0, 1000



    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.dir -=1
            if event.key == SDLK_d:
                self.dir +=1
            if event.key == SDLK_SPACE and self.fall == False:
                self.frame = 0
                self.fall = True
                self.vertical = 16
        elif event.type == SDL_KEYUP:
            self.frame = 0
            if event.key == SDLK_a:
                self.dir +=1
            if event.key == SDLK_d:
                self.dir -=1

        elif event.type == SDL_MOUSEMOTION:
            self.mx, self.my = event.x , play_mode.DK_height - 1 - event.y
    def draw(self):
        if dir != 0:
            if self.x < self.mx:
                self.image.clip_draw(int(self.frame) * 64, self.action * 65, 60, 65, self.x, self.y, self.size_x, self.size_y)
            elif self.x >= self.mx:
                self.image.clip_composite_draw(int(self.frame) * 64, self.action * 65, 60, 65,0,'h', self.x, self.y, self.size_x, self.size_y)
        else:
            self.image.clip_draw(int(self.frame)* 64, self.action * 65, 60, 65, self.x, self.y, self.size_x, self.size_y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x-self.size_x//4, self.y-self.size_y//4, self.x+self.size_x//4, self.y+self.size_y//4

    def handle_collision(self, group, other):
        if group == 'player:block' and self.vertical < 0:
            self.y = other.y + (other.size_y // 2) + 25  # 블록 위에 위치
            self.vertical = 0
            self.fall = False
            self.min_x, self.max_x = other.x - (other.size_x // 2), other.x + (other.size_x // 2)
            pass
