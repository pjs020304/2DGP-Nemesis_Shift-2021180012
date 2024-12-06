from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDL_QUIT, SDLK_SPACE, SDLK_0, SDLK_1, SDLK_2

import game_framework
from pico2d import get_time, clear_canvas, get_events, update_canvas, load_image, load_font, load_music

import game_world
import play_mode

from pico2d import load_image

class Layer:
    def __init__(self):
        self.layer = load_image('Resource\\layer 1.png')
        self.bgm = load_music('Resource\\story_music.mp3')
        self.bgm.set_volume(20)
        self.bgm.repeat_play()

    def draw(self):
        self.layer.draw(500, 400, 1000, 1000)

    def update(self):
        pass


class TalkBox:
    def __init__(self):
        self.layer = load_image('Resource\\buttonLong_blue_pressed.png')
        self.font = load_font('Resource\\ENCR10B.TTF', 30)
        self.current_time = get_time()
        self.time = 4
        self.boss = load_image('Resource\\Lord of the Poisons spritesheet 145x47 with glow.png')
        self.frame = 0
        self.action = 0
    def draw(self):
        self.boss.clip_composite_draw(0+self.frame, 376-47+ self.action, 145, 47, 0, 'h', 700, 500, 500, 400)
        self.layer.draw(500, 150, 1000, 300)
        if get_time() - self.current_time < self.time:
            self.font.draw(50, 250, 'You killed my son and came here in his guise.', (255, 255, 0))
        if self.time<get_time() - self.current_time < self.time*2:
            self.font.draw(50, 250, 'You must have come to kill me, ', (255, 255, 0))
            self.font.draw(50, 200, 'the one said to ruin the world.', (255, 255, 0))
        if self.time*2<get_time() - self.current_time < self.time*3:
            self.font.draw(50, 250, 'Yet, you mercilessly shattered my world', (255, 255, 0))
            self.font.draw(50, 200, 'and even mocked my son.', (255, 255, 0))

        if self.time*3<get_time() - self.current_time < self.time*4:
            self.font.draw(50, 250, 'To capture a monster like me, ', (255, 255, 0))
            self.font.draw(50, 200, 'you turned into a monster yourself. ', (255, 255, 0))
            self.font.draw(50, 150, 'Are you a savior or a monster?', (255, 255, 0))
        if self.time*4<get_time() - self.current_time < self.time*5:
            self.frame = (5 * 145)
            self.action = (-3 * 47)
            self.font = load_font('Resource\\ENCR10B.TTF', 50)
            self.font.draw(50, 250, 'You must be a Monster!!!"', (255, 0, 0))
            self.font.draw(50, 200, 'Release the tormented souls!!!"', (255, 0, 0))
        if self.time*5<get_time() - self.current_time < self.time*6:
            play_mode.backgrounds.bgm3.repeat_play()
            play_mode.final_lord.current_time =get_time()
            play_mode.final_lord.current_time =get_time()
            game_framework.pop_mode()
    def update(self):
        pass




def init():
    global layer
    global talkbox

    layer = Layer()
    game_world.add_obj(layer, 1)

    talkbox = TalkBox()
    game_world.add_obj(talkbox, 1)

def finish():
    game_world.remove_object(layer)
    game_world.remove_object(talkbox)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def update():
    pass

def pause():
    pass
def resume():
    pass