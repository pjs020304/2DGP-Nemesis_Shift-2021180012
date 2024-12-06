from random import randint
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import *
import play_mode
import game_framework
import player
import random
import attack
import game_world
import background
import ending_mode


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
        self.tx, self.ty = self.x, self.y

        self.font = load_font('Resource\\ENCR10B.TTF', 20)

    def update(self):
        if self.state != 'Die':
            # self.x += self.dir * player.RUN_SPEED_PPS * game_framework.frame_time
            if self.state == 'Walk':
                self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time) % self.frame_count
        if play_mode.player.dir == 1:
            if play_mode.player.x >= 700 and  -1500<play_mode.backgrounds.x[4]:
                self.x -= player.RUN_SPEED_PPS * game_framework.frame_time
                self.max_x-=player.RUN_SPEED_PPS * game_framework.frame_time
                self.min_x-=player.RUN_SPEED_PPS * game_framework.frame_time
                self.tx -=player.RUN_SPEED_PPS * game_framework.frame_time
        elif play_mode.player.dir == -1:
            if play_mode.player.x <= 300 and 1500>play_mode.backgrounds.x[4]:
                self.x += player.RUN_SPEED_PPS * game_framework.frame_time
                self.max_x+=player.RUN_SPEED_PPS * game_framework.frame_time
                self.min_x+=player.RUN_SPEED_PPS * game_framework.frame_time
                self.tx +=player.RUN_SPEED_PPS * game_framework.frame_time


        # if self.x >= self.max_x or self.x <= self.min_x:
        #     self.dir = self.dir*(-1)
        if self.state != 'Die':
            self.bt.run()
    def handle_event(self, event):
        pass
    def draw(self):
        if math.cos(self.dir) > 0:
            self.image.clip_draw(int(self.frame) * self.width, self.action * self.height, self.width, self.height, self.x, self.y, self.size_x, self.size_y)
        else:
            self.image.clip_composite_draw(int(self.frame) * self.width, self.action * self.height, self.width, self.height,0,'h', self.x, self.y, self.size_x, self.size_y)
        if play_mode.collider_trig:
            draw_rectangle(*self.get_bb())
            draw_rectangle(self.tx-10, self.ty-10,self.tx+10, self.ty+10)
        # self.font.draw(self.x, self.y + self.size_y // 4, f'{get_time() - self.current_time}', (255, 255, 0))

    def get_bb(self):
        return self.x-self.size_x//5, self.y-self.size_y//4, self.x+self.size_x//5, self.y+self.size_y//4

    def set_target_location(self, x=None, y=None):
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS
    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (player.PIXEL_PER_METER * r) ** 2
    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = player.RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
    def set_random_location(self):
        if self.state != 'Die':
            self.tx, self.ty= random.randint(int(self.min_x), int(self.max_x)), self.y
        return BehaviorTree.SUCCESS
    def move_to(self, r=1.5):
        if self.state != 'Die':
            self.move_slightly_to(self.tx, self.ty)
            if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.RUNNING
    def is_player_nearby(self, distance):
        if self.distance_less_than(play_mode.player.x, play_mode.player.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
    def attack_player(self):
        if self.state != 'Die':
            self.move_slightly_to(self.tx, self.ty)
            if get_time() - self.current_time > self.attack_cooldown and self.state != 'Die':
                self.state = 'Basic_Attack'
                if math.cos(self.dir) <= 0:
                    monsteratk = attack.MonsterATKPlayer(self.x - 25, self.y, self.basic_atk_size_x,
                                                         self.basic_atk_size_y)
                else:
                    monsteratk = attack.MonsterATKPlayer(self.x + 25, self.y, self.basic_atk_size_x,
                                                         self.basic_atk_size_y)
                game_world.add_obj(monsteratk, 1)
                game_world.add_collision_pair('monsterATK:player', monsteratk, None)
                self.frame = 0
                self.state = 'Basic_Attack'
                self.current_time = get_time()
                self.basic_atk.play()
                return BehaviorTree.SUCCESS
            if self.distance_less_than(self.tx, self.ty, self.x, self.y, 0.5):
                self.tx, self.ty= random.randint(int(self.min_x), int(self.max_x)), self.y
            return BehaviorTree.RUNNING
        return BehaviorTree.FAIL

    def build_behavior_tree(self):
        # a1 = Action('Set target lacation', self.set_target_location(), 1000,1000)
        # root = self.move_to_target_location = Sequence('Move to target location', a1, a2)

        a1 = Action('Move to', self.move_to)
        a2 = Action('Set random location', self.set_random_location)
        root = wander = Sequence('Wander', a2, a1)

        c1 = Condition('플레이어가 근처에 있는가?', self.is_player_nearby, 7)
        a3 = Action('Attack player', self.attack_player)
        attack_player = Sequence('플레이어를 공격', c1, a3)

        move_and_attack = Selector('공격할건지 안할건지 선택', attack_player, a1)

        root = Sequence('이동하고 공격', move_and_attack,wander)
        # root = attack_or_flee = Selector('공격 또는 무작위 이동', wander, attack_player)


        self.bt = BehaviorTree(root)

class Panda(Monster):
    def __init__(self, frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x):
        super().__init__(frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x)
        self.image = load_image('Resource\\Tiny Panda Evil Version 103x33.png')
        self.run_action = 12
        self.basic_atk_action= 3
        self.skill_atk_action = 6
        self.basic_atk_size_x, self.basic_atk_size_y = 130, 100
        self.skill_atk_size_x, self.skill_atk_size_y = 180, 100
        self.fall_action = 11
        self.idle_action = 13
        self.currenthp =5
        self.maxhp = 5
        self.png = 'Resource\\Tiny Panda Evil Version 103x33.png'
        self.basic_atk = load_wav('Resource\\swing-weapon.mp3')
        self.basic_atk.set_volume(30)
        self.skill = load_wav('Resource\\panda_skill.mp3')
        self.skill.set_volume(30)
        self.hit_sound = [load_wav('Resource\\bear.mp3'), load_wav('Resource\\bear_hit_2.mp3')]
        self.hit_sound[0].set_volume(50)
        self.hit_sound[1].set_volume(50)
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
        if group == 'playerATK:monster' and self.state != 'Die':
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
        self.basic_atk_size_x, self.basic_atk_size_y = 100, 50
        self.skill_atk_size_x, self.skill_atk_size_y = -1, -1
        self.fall_action = 6
        self.idle_action = 8
        self.currenthp =2
        self.maxhp = 2
        self.png = 'Resource\\Dust Jumper Sprite Sheet 42x91.png'
        self.basic_atk = load_wav('Resource\\bear.mp3')
        self.basic_atk.set_volume(30)
        self.skill = load_wav('Resource\\panda_skill.mp3')
        self.skill.set_volume(50)
        self.hit_sound = [load_wav('Resource\\hit_sound_1.mp3'), load_wav('Resource\\hit_sound_2.mp3')]
        self.hit_sound[0].set_volume(50)
        self.hit_sound[1].set_volume(50)

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


    def draw(self):
        super().draw()
        for i in range(self.currenthp):
            self.hp_png.draw(self.x-40 + i*20, self.y+20, 20, 30)

    def handle_collision(self, group, other):
        if group == 'playerATK:monster' and self.state != 'Die':
            self.currenthp -=1
            if self.currenthp <=0:
                self.state = 'Die'
                self.dir = 0.0

    def attack_player(self):
        if self.state != 'Die':
            self.move_slightly_to(self.tx, self.ty)
            if get_time() - self.current_time > self.attack_cooldown and self.state != 'Die':
                self.state = 'Basic_Attack'
                monsteratk = attack.MonsterFarATKPlayer(play_mode.player.x + randint(-20, 20), play_mode.player.y + randint(-20, 20), self.basic_atk_size_x, self.basic_atk_size_y)
                game_world.add_obj(monsteratk, 1)
                game_world.add_collision_pair('monsterFarATK:player', monsteratk, None)
                self.frame = 0
                self.state = 'Basic_Attack'
                self.current_time = get_time()
                return BehaviorTree.SUCCESS
            if self.distance_less_than(self.tx, self.ty, self.x, self.y, 0.5):
                self.tx, self.ty= random.randint(int(self.min_x), int(self.max_x)), self.y
            return BehaviorTree.RUNNING
        return BehaviorTree.FAIL

class LordOfFlames(Monster):
    def __init__(self, frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x):
        super().__init__(frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x)
        self.image = load_image('Resource\\Lord of the Flames spritesheet 145x47 with glow.png')
        self.run_action = 6
        self.basic_atk_action= 5
        self.skill_atk_action = 3
        self.basic_atk_size_x, self.basic_atk_size_y = 160, 100
        self.skill_atk_size_x, self.skill_atk_size_y = 180, 100
        self.fall_action = 1
        self.idle_action = 7
        self.currenthp =1
        self.maxhp = 7
        self.png = 'Resource\\Lord of the Flames spritesheet 145x47 with glow.png'
        self.basic_atk = load_wav('Resource\\fire_sound.mp3')
        self.basic_atk.set_volume(90)
        self.skill = load_wav('Resource\\fire_charge.mp3')
        self.skill.set_volume(50)
        self.hit_sound = [load_wav('Resource\\bear.mp3'), load_wav('Resource\\bear_hit_2.mp3')]
        self.hit_sound[0].set_volume(50)
        self.hit_sound[1].set_volume(50)
        self.sleeping_time = get_time()
        self.teleport_atk = False

    def update(self):
        self.action = self.idle_action
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

        elif self.state == 'heal':
            pass



    def draw(self):
        super().draw()
        for i in range(self.currenthp):
            self.hp_png.draw(self.x-40 + i*20, self.y+20, 20, 30)

    def handle_collision(self, group, other):
        if group == 'playerATK:monster':
            self.currenthp -=1
            if self.currenthp <=0 and self.state != 'Die':
                self.state = 'Die'
                self.dir = 0
                play_mode.portal2 = background.Portal(500, 130)
                game_world.add_obj(play_mode.portal2, 1)
                game_world.add_collision_pair('player:portal2', None, play_mode.portal2)
        if group == 'playerFarATK:monster':
            if self.currenthp <= 0 and self.state != 'Die':
                self.state = 'Die'
                self.dir = 0
                play_mode.portal2 = background.Portal(500, 130)
                game_world.add_obj(play_mode.portal2, 1)
                game_world.add_collision_pair('player:portal2', None, play_mode.portal2)

    def move_to(self, r=1.5):
        if self.state != 'Die':
            self.move_slightly_to(self.tx, self.ty)
            if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
                self.sleeping_time = get_time()
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.RUNNING

    def sleeping_to_action(self):
        self.action = self.idle_action
        if get_time() - self.sleeping_time > 2:
            self.current_time = get_time()
            self.sleeping_time = get_time()
            self.player_x, self.player_y =  play_mode.player.x, play_mode.player.y
            self.old_x, self.old_y = self.x, self.y
            self.select_pattern = randint(0,2)
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def first_pattern_heal(self):
        if self.select_pattern != 0:
            return BehaviorTree.FAIL
        self.state = 'heal'
        self.action = 1
        self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time)
        if self.frame >= 20:
            self.frame =0
            self.action = self.idle_action
            self.currenthp += 3
            self.state = 'Walk'
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING


    def second_pattern_teleport_attack(self):
        if self.select_pattern != 1:
            return BehaviorTree.FAIL
        if play_mode.player.x <= 300 or play_mode.player.x >= 700:
            self.player_x -= play_mode.player.dir* player.RUN_SPEED_PPS * game_framework.frame_time

        self.x, self.y = self.player_x, self.player_y


        if get_time() - self.current_time > 1 and not self.teleport_atk:
            if math.cos(self.dir) <= 0:
                monsteratk = attack.MonsterATKPlayer(self.x - 25, self.y, self.basic_atk_size_x,
                                                     self.basic_atk_size_y)
            else:
                monsteratk = attack.MonsterATKPlayer(self.x + 25, self.y, self.basic_atk_size_x,
                                                     self.basic_atk_size_y)
            game_world.add_obj(monsteratk, 1)
            game_world.add_collision_pair('monsterATK:player', monsteratk, None)
            self.frame = 0
            self.state = 'Basic_Attack'
            self.current_time = get_time()
            self.basic_atk.play()
            self.teleport_atk = True

        if get_time() - self.current_time >1 and self.teleport_atk:
            self.x, self.y = self.old_x, self.old_y
            self.sleeping_time = get_time()
            self.current_time = get_time()
            self.teleport_atk =False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move_charge(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = player.RUN_SPEED_PPS * game_framework.frame_time*3
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def third_pattern_charge(self):

        if self.x-self.min_x > self.max_x - self.x: self.tx, self.ty = self.min_x, self.y
        else: self.tx, self.ty = self.max_x, self.y

        self.action = 3
        self.move_charge(self.tx, self.ty)
        self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time) %14
        if get_time() - self.sleeping_time > 0.2:
            if math.cos(self.dir) <= 0:
                monsteratk = attack.MonsterATKPlayer(self.x - 25, self.y, self.skill_atk_size_x,self.skill_atk_size_y)
            else:
                monsteratk = attack.MonsterATKPlayer(self.x + 25, self.y, self.skill_atk_size_x,self.skill_atk_size_y)
            game_world.add_obj(monsteratk, 1)
            game_world.add_collision_pair('monsterATK:player', monsteratk, None)
            self.skill.play()
            self.sleeping_time = get_time()
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 1):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def check_1(self):
        if self.select_pattern != 0: return BehaviorTree.FAIL
        else: return BehaviorTree.SUCCESS
    def check_2(self):
        if self.select_pattern != 1: return BehaviorTree.FAIL
        else: return BehaviorTree.SUCCESS
    def check_3(self):
        if self.select_pattern != 2: return BehaviorTree.FAIL
        else: return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # a1 = Action('Set target lacation', self.set_target_location(), 1000,1000)
        # root = self.move_to_target_location = Sequence('Move to target location', a1, a2)

        a1 = Action('Move to', self.move_to)
        a2 = Action('Set random location', self.set_random_location)
        root = wander = Sequence('Wander', a2, a1)

        a3 = Action('다음 패턴까지 수면', self.sleeping_to_action)


        # c2 = Condition('플레이어가 근처에 있는가?', self.is_player_nearby, 7)
        a4 = [Action('Heal', self.first_pattern_heal),
              Action('teleport and Attack', self.second_pattern_teleport_attack),
              Action('charge attack', self.third_pattern_charge)]

        c1 = Condition('1번째 패턴인가?', self.check_1)
        c2 = Condition('2번째 패턴인가?', self.check_2)
        c3 = Condition('3번째 패턴인가?', self.check_3)

        first_pattern = Sequence('첫번째 패턴 실행', c1, a4[0])
        second_pattern = Sequence('두번째 패턴 실행', c2, a4[1])
        third_pattern = Sequence('세번째 패턴 실행', c3, a4[2])


        pattern_action = Selector('3가지 패턴 중 하나 실행', first_pattern, second_pattern, third_pattern)

        # move_and_attack = Selector('공격할건지 안할건지 선택', attack_player, a1)

        root = Sequence('이동하고 공격', a3, pattern_action,wander)
        # root = attack_or_flee = Selector('공격 또는 무작위 이동', wander, attack_player)

        self.bt = BehaviorTree(root)

class LordOfPotion(Monster):
    def __init__(self, frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x):
        super().__init__(frame_x, action_y, width, height, frame_count, position_x, position_y, size_x, size_y, max_x,min_x)
        self.image = load_image('Resource\\Lord of the Poisons spritesheet 145x47 with glow.png')
        self.run_action = 6
        self.basic_atk_action= 5
        self.skill_atk_action = 3
        self.basic_atk_size_x, self.basic_atk_size_y = 160, 100
        self.skill_atk_size_x, self.skill_atk_size_y = 180, 100
        self.fall_action = 1
        self.idle_action = 7
        self.currenthp =1
        self.maxhp = 7
        self.png = 'Resource\\Lord of the Flames spritesheet 145x47 with glow.png'
        self.basic_atk = load_wav('Resource\\fire_sound.mp3')
        self.basic_atk.set_volume(90)
        self.skill = load_wav('Resource\\fire_charge.mp3')
        self.skill.set_volume(50)
        self.hit_sound = [load_wav('Resource\\bear.mp3'), load_wav('Resource\\bear_hit_2.mp3')]
        self.hit_sound[0].set_volume(50)
        self.hit_sound[1].set_volume(50)
        self.sleeping_time = get_time()
        self.teleport_atk = False

    def update(self):
        self.action = self.idle_action
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
            if int(self.frame) ==8:
                game_framework.change_mode(ending_mode)

        elif self.state == 'heal':
            pass



    def draw(self):
        super().draw()
        for i in range(self.currenthp):
            self.hp_png.draw(self.x-40 + i*20, self.y+20, 20, 30)

    def handle_collision(self, group, other):
        if group == 'playerATK:monster':
            self.currenthp -=1
            if self.currenthp <=0 and self.state != 'Die':
                self.state = 'Die'
                self.dir = 0
                play_mode.portal2 = background.Portal(500, 130)
                game_world.add_obj(play_mode.portal2, 1)
                game_world.add_collision_pair('player:portal2', None, play_mode.portal2)
        if group == 'playerFarATK:monster':
            if self.currenthp <= 0 and self.state != 'Die':
                self.state = 'Die'
                self.dir = 0
                play_mode.portal2 = background.Portal(500, 130)
                game_world.add_obj(play_mode.portal2, 1)
                game_world.add_collision_pair('player:portal2', None, play_mode.portal2)

    def move_to(self, r=1.5):
        if self.state != 'Die':
            self.move_slightly_to(self.tx, self.ty)
            if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
                self.sleeping_time = get_time()
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.RUNNING

    def sleeping_to_action(self):
        self.action = self.idle_action
        if get_time() - self.sleeping_time > 1.5:
            self.current_time = get_time()
            self.sleeping_time = get_time()
            self.player_x, self.player_y =  play_mode.player.x, play_mode.player.y
            self.old_x, self.old_y = self.x, self.y
            self.select_pattern = randint(0,3)
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def first_pattern_heal(self):
        if self.select_pattern != 0:
            return BehaviorTree.FAIL
        self.state = 'heal'
        self.action = 1
        self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time)
        if self.frame >= 20:
            self.frame =0
            self.action = self.idle_action
            self.currenthp += 5
            self.state = 'Walk'
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING


    def second_pattern_teleport_attack(self):
        if self.select_pattern != 1:
            return BehaviorTree.FAIL
        if play_mode.player.x <= 300 or play_mode.player.x >= 700:
            self.player_x -= play_mode.player.dir* player.RUN_SPEED_PPS * game_framework.frame_time

        self.x, self.y = self.player_x, self.player_y


        if get_time() - self.current_time > 0.5 and not self.teleport_atk:
            if math.cos(self.dir) <= 0:
                monsteratk = attack.MonsterATKPlayer(self.x - 25, self.y, self.basic_atk_size_x,
                                                     self.basic_atk_size_y)
            else:
                monsteratk = attack.MonsterATKPlayer(self.x + 25, self.y, self.basic_atk_size_x,
                                                     self.basic_atk_size_y)
            game_world.add_obj(monsteratk, 1)
            game_world.add_collision_pair('monsterATK:player', monsteratk, None)
            self.frame = 0
            self.state = 'Basic_Attack'
            self.current_time = get_time()
            self.basic_atk.play()
            self.teleport_atk = True

        if get_time() - self.current_time >1 and self.teleport_atk:
            self.x, self.y = self.old_x, self.old_y
            self.sleeping_time = get_time()
            self.current_time = get_time()
            self.teleport_atk =False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move_charge(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = player.RUN_SPEED_PPS * game_framework.frame_time*3
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def set_charge(self):
        if self.x - self.min_x > self.max_x - self.x:
            self.tx, self.ty = self.min_x, self.y
        else:
            self.tx, self.ty = self.max_x, self.y

    def third_pattern_charge(self):
        self.action = 3
        self.move_charge(self.tx, self.ty)
        self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time) % 14
        if get_time() - self.sleeping_time > 0.15:
            if math.cos(self.dir) <= 0:
                monsteratk = attack.MonsterATKPlayer(self.x - 25, self.y, self.skill_atk_size_x, self.skill_atk_size_y)
            else:
                monsteratk = attack.MonsterATKPlayer(self.x + 25, self.y, self.skill_atk_size_x, self.skill_atk_size_y)
            game_world.add_obj(monsteratk, 1)
            game_world.add_collision_pair('monsterATK:player', monsteratk, None)
            self.skill.play()
            self.sleeping_time = get_time()
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, 1):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def four_pattern_bomb(self):
        self.action = 4
        self.frame = (self.frame + player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * game_framework.frame_time)
        if get_time() - self.current_time > 0.5:
            for o in range(13):
                monsteratk = attack.BossFarATKPlayer(randint(-500, 1000),randint(100, 500), 120,120)
                game_world.add_obj(monsteratk, 1)
                game_world.add_collision_pair('monsterFarATK:player', monsteratk, None)
            self.sleeping_time = get_time()
            self.current_time = get_time()
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING


    def check_1(self):
        if self.select_pattern != 0: return BehaviorTree.FAIL
        else: return BehaviorTree.SUCCESS
    def check_2(self):
        if self.select_pattern != 1: return BehaviorTree.FAIL
        else: return BehaviorTree.SUCCESS
    def check_3(self):
        if self.select_pattern != 2: return BehaviorTree.FAIL
        else: return BehaviorTree.SUCCESS
    def check_4(self):
        if self.select_pattern != 3: return BehaviorTree.FAIL
        else: return BehaviorTree.SUCCESS
    def check_5(self):
        if self.select_pattern != 4: return BehaviorTree.FAIL
        else: return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # a1 = Action('Set target lacation', self.set_target_location(), 1000,1000)
        # root = self.move_to_target_location = Sequence('Move to target location', a1, a2)

        a1 = Action('Move to', self.move_to)

        a3 = Action('다음 패턴까지 수면', self.sleeping_to_action)


        # c2 = Condition('플레이어가 근처에 있는가?', self.is_player_nearby, 7)
        a4 = [Action('Heal', self.first_pattern_heal),
              Action('teleport and Attack', self.second_pattern_teleport_attack),
              Action('charge attack', self.third_pattern_charge),
              Action('teleport and Attack', self.four_pattern_bomb)
              ]

        a10 = Action('돌진 위치 정하기', self.set_charge)

        c1 = Condition('1번째 패턴인가?', self.check_1)
        c2 = Condition('2번째 패턴인가?', self.check_2)
        c3 = Condition('3번째 패턴인가?', self.check_3)
        c4 = Condition('4번째 패턴인가?', self.check_4)
        c5 = Condition('5번째 패턴인가?', self.check_5)

        first_pattern = Sequence('첫번째 패턴 실행', c1, a4[0])
        second_pattern = Sequence('두번째 패턴 실행', c2, a4[1])
        third_pattern = Sequence('세번째 패턴 실행', c3, a10, a4[2])
        four_pattern = Sequence('네번째 패턴 실행', c4, a4[3])
        # five_pattern = Sequence('세번째 패턴 실행', c5, a4[4])


        pattern_action = Selector('4가지 패턴 중 하나 실행',  first_pattern,  second_pattern, third_pattern, four_pattern)

        # move_and_attack = Selector('공격할건지 안할건지 선택', attack_player, a1)

        root = Sequence('이동하고 공격', a3, pattern_action)
        # root = attack_or_flee = Selector('공격 또는 무작위 이동', wander, attack_player)

        self.bt = BehaviorTree(root)