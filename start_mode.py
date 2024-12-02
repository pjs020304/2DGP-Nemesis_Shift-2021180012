from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDL_QUIT, SDLK_SPACE

import game_framework
from pico2d import get_time, clear_canvas, get_events, update_canvas, load_image, load_music

import play_mode


def init():
    global image
    global sound

    sound = load_music('Resource\\UI_Sound.mp3')
    sound.set_volume(20)
    sound.repeat_play()
    image = load_image('Resource\\Start_UI.jpg')

def finish():
    global image
    del image
    global sound
    del sound

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)
def draw():
    clear_canvas()
    image.draw(play_mode.DK_width//2,play_mode.DK_height//2,play_mode.DK_width,play_mode.DK_height)
    update_canvas()

def update():
    pass


def pause():
    pass
def resume():
    pass