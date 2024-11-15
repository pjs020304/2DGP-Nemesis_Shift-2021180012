from pico2d import *
import play_mode
import player
import game_framework
class BackGround:
    def __init__(self):
        self.layer1 = load_image('layer 1.png')
        self.layer2 = load_image('layer 2.png')
        self.layer3 = load_image('layer 3.png')
        self.layer4 = load_image('layer 4.png')
        self.layer5 = load_image('layer 5.png')
        self.x = [play_mode.DK_width // 2, play_mode.DK_width // 2, play_mode.DK_width // 2, play_mode.DK_width // 2, play_mode.DK_width // 2]
        self.y = [play_mode.DK_height//2,play_mode.DK_height//2,play_mode.DK_height//2,play_mode.DK_height//2,play_mode.DK_height//2]
        self.speed = 1
    def update(self):
        if play_mode.player.dir == 1:
            if play_mode.player.x >= 700:
                self.x[2] -= player.RUN_SPEED_PPS * game_framework.frame_time/3
                self.x[3] -= player.RUN_SPEED_PPS * game_framework.frame_time/2
                self.x[4] -= player.RUN_SPEED_PPS * game_framework.frame_time
        elif play_mode.player.dir == -1:
            if play_mode.player.x <= 300:
                self.x[2] += player.RUN_SPEED_PPS * game_framework.frame_time/3
                self.x[3] += player.RUN_SPEED_PPS * game_framework.frame_time/2
                self.x[4] += player.RUN_SPEED_PPS * game_framework.frame_time
        else:
            pass
    def draw(self):
        self.layer1.draw(self.x[0], self.y[0], 1600, 800)
        self.layer2.draw(self.x[1], self.y[1],1600, 800)
        self.layer3.draw(self.x[2], self.y[2],2400, 800)
        self.layer4.draw(self.x[3], self.y[3],2400, 800)
        self.layer5.draw(self.x[4], self.y[4],2400, 800)
        pass