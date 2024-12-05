from pico2d import *
import play_mode
import player
import game_framework
class BackGround:
    def __init__(self, stage):
        if stage == 1:
            self.layer1 = load_image('Resource\\layer 1.png')
            self.layer3 = load_image('Resource\\layer 3.png')
            self.layer4 = load_image('Resource\\layer 4.png')
            self.bgm = load_music('Resource//1Stage_Sound.mp3')
            self.bgm.set_volume(20)
            self.bgm.repeat_play()
        if stage == 2:
            self.layer1 = load_image('Resource\\layer 1_2.png')
            self.layer3 = load_image('Resource\\layer 3_2.png')
            self.layer4 = load_image('Resource\\layer 4_2.png')
            self.bgm2 = load_music('Resource//2Stage_Sound.mp3')
            self.bgm2.set_volume(20)
            self.bgm2.repeat_play()
        if stage == 3:
            self.layer1 = load_image('Resource\\layer 1_3.png')
            self.layer3 = load_image('Resource\\layer 3_3.png')
            self.layer4 = load_image('Resource\\layer 4_3.png')
            self.bgm2 = load_music('Resource//Final_Stage_Music.mp3')
            self.bgm2.set_volume(20)
            self.bgm2.repeat_play()
        self.layer2 = load_image('Resource\\layer 2.png')
        self.layer5 = load_image('Resource\\layer 5.png')
        self.floor = load_image('Resource\\DARK Edition Tileset No background.png')
        self.x = [play_mode.DK_width // 2, play_mode.DK_width // 2, play_mode.DK_width // 2, play_mode.DK_width // 2, play_mode.DK_width // 2]
        self.y = [play_mode.DK_height//2,play_mode.DK_height//2,play_mode.DK_height//2,play_mode.DK_height//2,play_mode.DK_height//2]
        self.speed = 1


    def update(self):
        if play_mode.player.dir == 1:
            if -1500<self.x[4] and play_mode.player.x >= 700 :
                self.x[2] -= player.RUN_SPEED_PPS * game_framework.frame_time/3
                self.x[3] -= player.RUN_SPEED_PPS * game_framework.frame_time/2
                self.x[4] -= player.RUN_SPEED_PPS * game_framework.frame_time
        elif play_mode.player.dir == -1:
            if   play_mode.player.x <= 300 and self.x[4]<1500:
                self.x[2] += player.RUN_SPEED_PPS * game_framework.frame_time/3
                self.x[3] += player.RUN_SPEED_PPS * game_framework.frame_time/2
                self.x[4] += player.RUN_SPEED_PPS * game_framework.frame_time


    def draw(self):
        self.layer1.draw(self.x[0], self.y[0], 3500, 800)
        self.layer2.draw(self.x[1], self.y[1],1600, 800)
        self.layer3.draw(self.x[2], self.y[2],3500, 800)
        self.layer4.draw(self.x[3], self.y[3],3500, 800)
        self.layer5.draw(self.x[4], self.y[4],5000, 800)
        self.floor.clip_draw(30, 200, 600,30, self.x[4], 30, 5000, 110)
        pass

class Portal:
    def __init__(self, x, y):
        self.image = load_image('Resource\\portal.png')
        self.x, self.y = x,y
        self.size_x, self.size_y = 100, 180
        self.frame = 0
    def update(self):
        if play_mode.player.dir == 1:
            if play_mode.player.x >= 700 and -1500 < play_mode.backgrounds.x[4]:
                self.x -= player.RUN_SPEED_PPS * game_framework.frame_time
        elif play_mode.player.dir == -1:
            if play_mode.player.x <= 300 and 1500 > play_mode.backgrounds.x[4]:
                self.x += player.RUN_SPEED_PPS * game_framework.frame_time

        self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        self.image.clip_draw(int(self.frame)*250, 0, 250, 592, self.x, self.y+80, self.size_x, self.size_y)
        if play_mode.collider_trig:
            draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.size_x , self.y, self.x + self.size_x , self.y + self.size_y

    def handle_collision(self, group, other):
        if group == 'player:portal':
            pass