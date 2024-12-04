from pico2d import *
import game_world
import game_framework
import pause_mode
import player as character
import blocks as bridge
import background
import monster
import start_mode
import death_mode
import play_mode

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
    global game_over
    global game_change_1_2
    global backgrounds
    global portal

    game_over = False
    game_change_1_2 = False

    collider_trig = False
    gravity = 1

    backgrounds = background.BackGround(1)
    game_world.add_obj(backgrounds,0)

    2680
    portal = background.Portal(500, 270)
    game_world.add_obj(portal, 1)
    game_world.add_collision_pair('player:portal', None, portal)

    player = character.Player()
    game_world.add_obj(player,1)
    game_world.add_collision_pair('player:portal', player, None)
    game_world.add_collision_pair('player:block', player, None)
    game_world.add_collision_pair('player:monster', player, None)
    game_world.add_collision_pair('monsterATK:player', None, player)
    game_world.add_collision_pair('monsterFarATK:player', None, player)

    global lords
    lords = [
        monster.LordOfFrames(0, 6, 145, 47, 8, 800, 100, 150, 100, 800 + 200, 300 - 200)
    ]
    for lord in lords:
        game_world.add_obj(lord, 1)
        game_world.add_collision_pair('player:monster', None, lord)
        game_world.add_collision_pair('playerATK:monster', lord, None)
        game_world.add_collision_pair('playerFarATK:monster', lord, None)

    blocks = [
        bridge.Block(30, 176, 82, 22, 600, 175+100, 300, 100),
        bridge.Block(30, 176, 82, 22, 1000, 175, 500, 100),
        bridge.Block(30, 176, 82, 22, 1300, 250, 100, 100),
        bridge.Block(30, 176, 82, 22, 1700, 350, 700, 100),
        bridge.Block(30, 176, 82, 22, 2150, 350, 80, 100),
        bridge.Block(30, 176, 82, 22, 2300, 340, 70, 100),
        bridge.Block(30, 176, 82, 22, 2450, 380, 90, 100),
        bridge.Block(30, 176, 82, 22, 2000, 260, 400, 100),
        bridge.Block(30, 176, 82, 22, 2710, 250, 280, 100),

    ]
    for block in blocks:
        game_world.add_obj(block, 0)

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
        game_world.add_collision_pair('playerFarATK:monster', panda, None)

    dustjumpers = [
        monster.DustJumper(0, 12, 42, 91, 8, 2000, 300, 150, 100, 2000 + 200, 2000 - 200)
    ]
    for dustjumper in dustjumpers:
        game_world.add_obj(dustjumper, 1)
        game_world.add_collision_pair('player:monster', None, dustjumper)
        game_world.add_collision_pair('playerATK:monster', dustjumper, None)
        game_world.add_collision_pair('playerFarATK:monster', dustjumper, None)

def init2():
    global blocks
    global pandas
    global dustjumpers
    global backgrounds
    global portal2
    global player
    global background

    player.x, player.y = 400,90
    game_world.add_collision_pair('player:portal2', player, None)

    backgrounds = background.BackGround(2)
    game_world.add_obj(backgrounds, 0)

    blocks = [
        bridge.Block(30, 176, 82, 22, DK_width//2, 100, 3000, 100),
        bridge.Block(30, 176, 82, 22, DK_width//2, 250, 3000, 100)
    ]
    for block in blocks:
        game_world.add_obj(block, 0)

    for block in blocks:
        game_world.add_collision_pair('player:block', None, block)

    #portal2 = background.Portal(2680, 270)
    #game_world.add_obj(portal, 1)
    #game_world.add_collision_pair('player:portal2', None, portal)



def update():
    if game_over:
        game_framework.change_mode(death_mode)
    if play_mode.game_change_1_2:
        for block in play_mode.blocks:
            game_world.remove_object(block)
        for o in play_mode.pandas:
            game_world.remove_object(o)
        for o in play_mode.dustjumpers:
            game_world.remove_object(o)
        game_world.remove_object(play_mode.portal)
        play_mode.game_change_1_2 = False
        init2()
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
    global dustjumpers
    for dustjumper in dustjumpers:
        game_world.remove_object(dustjumper)
    del dustjumpers
    game_world.clear()


DK_width, DK_height = 1000, 700

def pause():
    pass
def resume():
    pass