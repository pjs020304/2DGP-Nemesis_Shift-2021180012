from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDL_QUIT, SDLK_SPACE, SDLK_0, SDLK_1, SDLK_2

import game_framework
from pico2d import get_time, clear_canvas, get_events, update_canvas, load_image, load_music

import game_world
import play_mode

from pico2d import load_image

class Layer:
    def __init__(self):
        self.layer = load_image('Resource\\THE_END.png')
        self.bgm = load_music('Resource\\ending_sound.mp3')
        self.bgm.set_volume(20)
        self.bgm.repeat_play()
    def draw(self):
        self.layer.draw(500, 400, 1000, 1000)

    def update(self):
        pass




def init():
    global layer

    layer = Layer()
    game_world.add_obj(layer, 1)



def finish():
    game_world.remove_object(layer)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

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