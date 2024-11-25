from random import randint
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import *
import play_mode
import game_framework
import player
import random
import attack
import game_world

class Monster:
    def __init__(self, frame_x, action_y, width, height,frame_count, position_x, position_y, size_x, size_y, max_x, min_x):
        self.x, self.y = position_x, position_y
        self.frame, self.action = frame_x, action_y
        self.width, self.height = width, height
        self.frame_count = frame_count
        self.dir = 1
        self.size_x, self.size_y = size_x, size_y
        self.max_x, self.min_x = max_x, min_x
        self.hp_png = load_image('Resource\\health_bar.png')
        self.state = 'Walk'
        self.current_time = get_time()
        self.attack_cooldown = randint(3,6)
        self.build_behavior_tree()

    def update(self):
        if self.state != 'Die':
            self.x += self.dir * player.RUN_SPEED_PPS * game_framework.frame_time
            if self.state == 'Walk':
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

    def set_target_location(self, x=None, y=None):
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS
    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (play_mode.PIXEL_PER_METER * r) ** 2
    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = play_mode.RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
    def set_random_location(self):
        self.tx, self.ty = random.randint(self.min_x, self.y), random.randint(self.min_x, self.y)
        return BehaviorTree.SUCCESS
    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
    def is_boy_nearby(self, distance):
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
    def attack_player(self):
        self.state = 'Basic_Attack'
        self.move_slightly_to(self.tx, self.ty)
        if get_time() - self.current_time > self.attack_cooldown and self.state != 'Die':
            if self.dir == 1:
                monsteratk = attack.MonsterATKPlayer(self.x + 25, self.y, self.basic_atk_size_x, self.basic_atk_size_y)
            elif self.dir == -1:
                monsteratk = attack.MonsterATKPlayer(self.x - 25, self.y, self.basic_atk_size_x, self.basic_atk_size_y)
            game_world.add_obj(monsteratk, 1)
            game_world.add_collision_pair('monsterATK:player', monsteratk, None)
            self.frame = 0
            self.state = 'Basic_Attack'
            self.current_time = get_time()
    def build_behavior_tree(self):
        # a1 = Action('Set target lacation', self.set_target_location(), 1000,1000)
        # root = self.move_to_target_location = Sequence('Move to target location', a1, a2)

        a1 = Action('Move to', self.move_to)
        a2 = Action('Set random location', self.set_random_location)
        root = wander = Sequence('Wander', a2, a1)

        c1 = Condition('소년이 근처에 있는가?', self.is_boy_nearby, 7)
        a3 = Action('Attack player', self.attack_player)
        root = chase_boy = Sequence('소년을 추적', c1, a3)

        # root = runaway_chase_or_flee = Selector('추적 또는 후퇴 또는 배회', run_away_boy, chase_boy, wander)

        self.bt = BehaviorTree(root)

class Panda(Monster):
    def __init__(self, frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x):
        super().__init__(frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x)
        self.image = load_image('Resource\\Tiny Panda Evil Version 103x33.png')
        self.run_action = 12
        self.basic_atk_action= 3
        self.skill_atk_action = 6
        self.basic_atk_size_x, self.basic_atk_size_y = 130, 50
        self.skill_atk_size_x, self.skill_atk_size_y = 180, 100
        self.fall_action = 11
        self.idle_action = 13
        self.currenthp =5
        self.maxhp = 5
        self.png = 'Resource\\Tiny Panda Evil Version 103x33.png'
    def update(self):
        self.action = 12
        super().update()

        if self.state == 'Basic_Attack':
            self.action = self.basic_atk_action
            self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time)
            if self.frame >=4:
                self.action = self.idle_action
                self.state = 'Walk'
                self.frame = 0
                self.current_time = get_time()
        elif self.state == 'Die':
            self.action = 0
            if int(self.frame) <=8:
                self.frame = self.frame + player.FRAMES_PER_ACTION/4 * player.ACTION_PER_TIME * game_framework.frame_time

    def draw(self):
        super().draw()
        for i in range(self.currenthp):
            self.hp_png.draw(self.x-40 + i*20, self.y+20, 20, 30)

    def handle_collision(self, group, other):
        if group == 'playerATK:monster':
            self.currenthp -=1
            if self.currenthp <=0:
                self.state = 'Die'
                self.dir = 0


class DustJumper(Monster):
    def __init__(self, frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x):
        super().__init__(frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x)
        self.image = load_image('Resource\\Dust Jumper Sprite Sheet 42x91.png')
        self.run_action = 4
        self.basic_atk_action= 7
        self.skill_atk_action = -1
        self.basic_atk_size_x, self.basic_atk_size_y = 200, 50
        self.skill_atk_size_x, self.skill_atk_size_y = -1, -1
        self.fall_action = 6
        self.idle_action = 8
        self.currenthp =2
        self.maxhp = 2
        self.png = 'Resource\\Dust Jumper Sprite Sheet 42x91.png'
    def update(self):
        self.action = self.run_action
        super().update()

        if self.state == 'Basic_Attack':
            self.action = self.basic_atk_action
            self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time)
            if self.frame >=4:
                self.action = self.idle_action
                self.state = 'Walk'
                self.frame = 0
                self.current_time = get_time()
        elif self.state == 'Die':
            self.action = 0
            if int(self.frame) <=8:
                self.frame = self.frame + player.FRAMES_PER_ACTION/4 * player.ACTION_PER_TIME * game_framework.frame_time

        if get_time() - self.current_time > self.attack_cooldown and self.state != 'Die':
            if self.dir == 1:
                monsteratk = attack.MonsterATKPlayer(self.x + 25, self.y, self.basic_atk_size_x, self.basic_atk_size_y)
            elif self.dir == -1:
                monsteratk = attack.MonsterATKPlayer(self.x - 25, self.y, self.basic_atk_size_x, self.basic_atk_size_y)
            game_world.add_obj(monsteratk, 1)
            game_world.add_collision_pair('monsterATK:player', monsteratk, None)
            self.frame = 0
            self.state = 'Basic_Attack'
            self.current_time = get_time()

    def draw(self):
        super().draw()
        for i in range(self.currenthp):
            self.hp_png.draw(self.x-40 + i*20, self.y+20, 20, 30)

    def handle_collision(self, group, other):
        if group == 'playerATK:monster':
            self.currenthp -=1
            if self.currenthp <=0:
                self.state = 'Die'
                self.dir = 0