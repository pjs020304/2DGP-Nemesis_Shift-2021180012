from pico2d import *
import game_world
import game_framework
import pause_mode
import player as character
import blocks as bridge
import background
import monster
import start_mode

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_mode(pause_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            game_framework.change_mode(start_mode)
        else:
            player.handle_event(event)

def init():
    global player
    global gravity
    global blocks
    global DK_width, DK_height
    global collider_trig
    global pandas
    global dustjumpers

    collider_trig = False
    gravity = 1

    backgrounds = background.BackGround()
    game_world.add_obj(backgrounds,0)

    player = character.Player()
    game_world.add_obj(player,1)
    game_world.add_collision_pair('player:block', player, None)
    game_world.add_collision_pair('player:monster', player, None)
    game_world.add_collision_pair('monsterATK:player', None, player)
    game_world.add_collision_pair('monsterFarATK:player', None, player)

    blocks = [
        bridge.Block(30, 176, 82, 22, 600, 175+100, 300, 100),
        bridge.Block(30, 176, 82, 22, 1000, 175, 500, 100)
    ]
    for block in blocks:
        game_world.add_obj(block, 0)
        pass
    for block in blocks:
        game_world.add_collision_pair('player:block', None, block)

    pandas = [
        monster.Panda(0, 12, 103, 33, 8, 1000, 225, 150, 100, 1000+250, 1000 - 250),
        monster.Panda(0, 12, 103, 33, 8, 600, 275+50, 150, 100, 600 + 150, 600-150)
    ]
    for panda in pandas:
        game_world.add_obj(panda, 1)
        game_world.add_collision_pair('player:monster', None, panda)
        game_world.add_collision_pair('playerATK:monster', panda, None)

    dustjumpers = [
        monster.DustJumper(0, 12, 42, 91, 8, 900, 225, 150, 100, 1000 + 250, 1000 - 250),
        monster.DustJumper(0, 12, 42, 91, 8, 550, 275 + 50, 150, 100, 600 + 150, 600 - 150)
    ]
    for dustjumper in dustjumpers:
        game_world.add_obj(dustjumper, 1)
        game_world.add_collision_pair('player:monster', None, dustjumper)
        game_world.add_collision_pair('playerATK:monster', dustjumper, None)

def update():
    game_world.update()
    game_world.handle_collisions()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    # game_world.clear()
    global player
    game_world.remove_object(player)
    del player
    global gravity
    del gravity
    global blocks
    for block in blocks:
        game_world.remove_object(block)
    del blocks
    global collider_trig
    del collider_trig
    global pandas
    for panda in pandas:
        game_world.remove_object(panda)
    del pandas
DK_width, DK_height = 1000, 700

def pause():
    pass
def resume():
    pass