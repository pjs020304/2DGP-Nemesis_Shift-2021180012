from random import randint

from pico2d import *
from pygame.draw_py import clip_line

import play_mode
import game_framework
import attack
import game_world
import death_mode


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

class CharInfo:
    def __init__(self, width=0, height=0, size_x=0, size_y=0, run_action=0, basic_atk_action=0, fall_action=0, idle_action=0, png='Resource\\UI_quit.png', basic_atk_size_x=0, basic_atk_size_y=0, skill_atk_action=0, skill_atk_size_x=0, skill_atk_size_y=0, maxhp=0, basic_atk=0, skill=0, hit_sound=0):
        self.size_x, self.size_y = size_x, size_y
        self.png = png
        self.image = load_image(self.png)
        self.width, self.height = width, height
        self.basic_atk_size_x, self.basic_atk_size_y =  basic_atk_size_x, basic_atk_size_y
        self.run_action = run_action
        self.basic_atk_action= basic_atk_action
        self.fall_action = fall_action
        self.idle_action = idle_action
        self.skill_atk_action = skill_atk_action
        self.skill_atk_size_x = skill_atk_size_x
        self.skill_atk_size_y = skill_atk_size_y
        self.hp = maxhp
        self.basic_atk = basic_atk
        self.skill = skill
        self.hit_sound = hit_sound

class Player:
    def __init__(self):
        self.x, self.y = 400,90
        self.font = load_font('Resource\\ENCR10B.TTF', 20)
        self.frame = 0
        self.dir = 0
        self.state = 'Idle'
        self.action = 0
        self.corpse = False
        self.panel = load_image("Resource\\buttonSquare_blue.png")
        self.cliked_e = False
        self.png = 'Resource\\Sci-fi hero 64x65.png'
        self.skill_count = get_time()
        self.hp_png = load_image('Resource\\health_bar.png')
        self.near_portal = False
        self.jump_sound = load_wav('Resource\\jump_sound.mp3')
        self.jump_sound.set_volume(30)




        # 변신할 때 바껴야 할 것들, 바뀌지 않는 게 있다면 여기서 찾아라 제발
        self.hp = 3
        self.charinfoexist = [False, False]
        self.charinfo = [CharInfo(), CharInfo()]
        self.size_x, self.size_y = 120, 120
        self.image = load_image(self.png)
        self.width, self.height = 64, 65
        self.basic_atk_size_x, self.basic_atk_size_y = 100, 50
        self.skill_atk_size_x, self.skill_atk_size_y = 100, 100
        self.run_action = 11
        self.basic_atk_action= 8
        self.skill_atk_action = 2
        self.fall_action = 9
        self.idle_action = 18
        self.basic_atk = load_wav('Resource\\sword-sound-1.mp3')
        self.basic_atk.set_volume(50)
        self.skill = load_wav('Resource\\sword-sound-2.mp3')
        self.skill.set_volume(50)
        self.skill = load_wav('Resource\\sword-sound-2.mp3')
        self.basic_cooldown = get_time()
        self.hit_sound = [load_wav('Resource\\hit_sound_1.mp3'), load_wav('Resource\\hit_sound_2.mp3')]
        self.hit_sound[0].set_volume(50)
        self.hit_sound[1].set_volume(70)

        # 떨어짐 체크
        self.vertical = 0
        self.fall = False
        self.min_x, self.max_x = 0, 1000
        self.mx, self.my = 0,0

    def change_char(self, charnum):
            self.size_x, self.charinfo[charnum].size_x = self.charinfo[charnum].size_x, self.size_x
            self.size_y, self.charinfo[charnum].size_y = self.charinfo[charnum].size_y, self.size_y
            self.png, self.charinfo[charnum].png = self.charinfo[charnum].png, self.png
            self.image = load_image(self.png)
            self.charinfo[charnum].image = load_image(self.charinfo[charnum].png)
            self.width, self.charinfo[charnum].width = self.charinfo[charnum].width, self.width
            self.height, self.charinfo[charnum].height = self.charinfo[charnum].height, self.height
            self.basic_atk_size_x, self.charinfo[charnum].basic_atk_size_x = self.charinfo[
                charnum].basic_atk_size_x, self.basic_atk_size_x
            self.basic_atk_size_y, self.charinfo[charnum].basic_atk_size_y = self.charinfo[
                charnum].basic_atk_size_y, self.basic_atk_size_y
            self.skill_atk_size_x, self.charinfo[charnum].skill_atk_size_x = self.charinfo[
                charnum].skill_atk_size_x, self.skill_atk_size_x
            self.skill_atk_size_y, self.charinfo[charnum].skill_atk_size_y = self.charinfo[
                charnum].skill_atk_size_y, self.skill_atk_size_y
            self.run_action, self.charinfo[charnum].run_action = self.charinfo[charnum].run_action, self.run_action
            self.basic_atk_action, self.charinfo[charnum].basic_atk_action = self.charinfo[
                charnum].basic_atk_action, self.basic_atk_action
            self.skill_atk_action, self.charinfo[charnum].skill_atk_action = self.charinfo[
                charnum].skill_atk_action, self.skill_atk_action
            self.fall_action, self.charinfo[charnum].fall_action = self.charinfo[charnum].fall_action, self.fall_action
            self.idle_action, self.charinfo[charnum].idle_action = self.charinfo[charnum].idle_action, self.idle_action
            self.hp, self.charinfo[charnum].hp = self.charinfo[charnum].hp, self.hp
            self.basic_atk, self.charinfo[charnum].basic_atk = self.charinfo[charnum].basic_atk, self.basic_atk
            self.skill, self.charinfo[charnum].skill = self.charinfo[charnum].skill, self.skill
            self.hit_sound[0], self.charinfo[charnum].hit_sound[0] = self.charinfo[charnum].hit_sound[0], self.hit_sound[0]
            self.hit_sound[1], self.charinfo[charnum].hit_sound[1] = self.charinfo[charnum].hit_sound[1], self.hit_sound[1]


    def update(self):

        if self.dir == -1:
            if self.x >= 300:
                self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.min_x += RUN_SPEED_PPS * game_framework.frame_time
                self.max_x += RUN_SPEED_PPS * game_framework.frame_time
            if self.state == 'Idle':
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
            self.action = self.run_action

        elif self.dir == 1:
            if self.x <= 700:
                self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.min_x -= RUN_SPEED_PPS * game_framework.frame_time
                self.max_x -= RUN_SPEED_PPS * game_framework.frame_time
            if self.state == 'Idle':
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
            self.action = self.run_action
        else:
            self.action =self.idle_action
            if self.state == 'Idle':
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12

        # 중력 적용
        if self.fall:
            self.y += self.vertical
            self.vertical -= (play_mode.gravity* RUN_SPEED_PPS * game_framework.frame_time)//2
            self.action = self.fall_action
            if self.state == 'Idle':
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if self.state == 'Basic_Attack':
            self.action = self.basic_atk_action
            self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if self.frame >=4:
                self.frame = 0
                self.action = self.idle_action
                self.state = 'Idle'

        if self.state == 'Skill_Attack':
            self.action = self.skill_atk_action
            self.frame = self.frame + FRAMES_PER_ACTION/2 * ACTION_PER_TIME * game_framework.frame_time
            if self.png == 'Resource\\Lord of the Frames spritesheet 145x47 with glow.png':
                if self.x >=300 and self.x <=700:
                    self.x += self.dir*RUN_SPEED_PPS * game_framework.frame_time*5
                else:
                    self.min_x += self.dir*RUN_SPEED_PPS * game_framework.frame_time*5
                    self.max_x += self.dir*RUN_SPEED_PPS * game_framework.frame_time*5
                if get_time() - self.basic_cooldown > 0.1:
                    if self.x < self.mx:
                        playeratk = attack.PlayerATKMonster(self.x + 25, self.y, self.skill_atk_size_y,self.skill_atk_size_y)
                    else:
                        playeratk = attack.PlayerATKMonster(self.x - 25, self.y, self.skill_atk_size_y,self.skill_atk_size_y)
                    game_world.add_obj(playeratk, 1)
                    game_world.add_collision_pair('playerATK:monster', None, playeratk)
                    self.basic_cooldown = get_time()
            if self.frame >=8:
                self.state = 'Idle'
                self.frame = 0
                self.action = self.idle_action
                self.skill_count = get_time()

        # 땅과의 충돌 체크
        if self.y <= 90:
            self.y = 90
            self.vertical = 0
            self.fall = False

        if self.x <self.min_x or self.x > self.max_x:
            self.fall = True
            self.min_x, self.max_x = 0, 1000

        if self.charinfo[0].hp<=0:self.charinfoexist[0] = False
        if self.charinfo[1].hp<=0:self.charinfoexist[1] = False

        if self.hp <=0:
            if self.charinfoexist[0]:
                self.change_char(0)
            elif self.charinfoexist[1]:
                self.change_char(1)
            else:
                play_mode.game_over = True
                pass



    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.dir -=1
            if event.key == SDLK_d:
                self.dir +=1
            if event.key == SDLK_e:
                self.cliked_e = True
            if event.key == SDLK_1 and self.charinfoexist[0]:
                self.change_char(0)
            if event.key == SDLK_2 and self.charinfoexist[1]:
                self.change_char(1)

            if event.key == SDLK_SPACE and self.fall == False:
                self.fall = True
                self.vertical = 16
                self.jump_sound.play()
            if event.key == SDLK_t:
                play_mode.collider_trig = not play_mode.collider_trig
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.dir +=1
            if event.key == SDLK_d:
                self.dir -=1
            if event.key == SDLK_e:
                self.cliked_e = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT and self.state == 'Idle':
                if self.png != 'Resource\\Dust Jumper Sprite Sheet 42x91.png' and get_time() - self.basic_cooldown > 0.5:
                    self.frame = 0
                    self.action = self.basic_atk_action
                    self.state = 'Basic_Attack'
                    if self.x < self.mx:
                        playeratk = attack.PlayerATKMonster(self.x + 25, self.y, self.basic_atk_size_x, self.basic_atk_size_y)
                    else:
                        playeratk = attack.PlayerATKMonster(self.x - 25, self.y,self.basic_atk_size_x, self.basic_atk_size_y)
                    game_world.add_obj(playeratk, 1)
                    game_world.add_collision_pair('playerATK:monster', None, playeratk)
                    self.basic_atk.play()
                    self.basic_cooldown = get_time()



                elif self.png == 'Resource\\Dust Jumper Sprite Sheet 42x91.png' and get_time() - self.basic_cooldown > 1.7:
                    self.frame = 0
                    self.action = self.basic_atk_action
                    self.state = 'Basic_Attack'
                    playeratk = attack.PlayerFarATKMonster(self.mx, self.my, self.basic_atk_size_x,self.basic_atk_size_y)
                    game_world.add_obj(playeratk, 1)
                    game_world.add_collision_pair('playerFarATK:monster', None, playeratk)
                    self.basic_cooldown = get_time()
            if event.button == SDL_BUTTON_RIGHT and self.state == 'Idle'and get_time()- self.skill_count > 5 and self.png != 'Resource\\Dust Jumper Sprite Sheet 42x91.png':
                self.frame = 0
                self.action = self.skill_atk_action
                self.state = 'Skill_Attack'
                if self.x < self.mx:
                    playeratk = attack.PlayerATKMonster(self.x + 25, self.y, self.skill_atk_size_x, self.skill_atk_size_y)
                else:
                    playeratk = attack.PlayerATKMonster(self.x - 25, self.y,self.skill_atk_size_x, self.skill_atk_size_y)
                game_world.add_obj(playeratk, 1)
                game_world.add_collision_pair('playerATK:monster', None, playeratk)
                self.skill.play()
        elif event.type == SDL_MOUSEMOTION:
            self.mx, self.my = event.x , play_mode.DK_height - 1 - event.y
    def draw(self):
        if dir != 0:
            if self.x < self.mx:
                self.image.clip_draw(int(self.frame) * self.width, self.action * self.height, self.width, self.height, self.x, self.y, self.size_x, self.size_y)
            elif self.x >= self.mx:
                self.image.clip_composite_draw(int(self.frame) * self.width, self.action * self.height, self.width, self.height,0,'h', self.x, self.y, self.size_x, self.size_y)
        else:
            self.image.clip_draw(int(self.frame)* self.width, self.action * self.height, self.width, self.height, self.x, self.y, self.size_x, self.size_y)

        if play_mode.collider_trig:
            draw_rectangle(*self.get_bb())
        self.panel.draw(100, 600, 180, 180)
        self.panel.draw(280, 600, 180, 180)
        if self.charinfoexist[0]:
            self.charinfo[0].image.clip_draw(0* self.charinfo[0].width, 0 * self.charinfo[0].height, self.charinfo[0].width, self.charinfo[0].height, 100, 600, 180, 180)
        if self.charinfoexist[1]:
            self.charinfo[1].image.clip_draw(0* self.charinfo[1].width, 0 * self.charinfo[1].height, self.charinfo[1].width, self.charinfo[1].height, 280, 600, 180, 180)
        if self.corpse:
            self.font.draw(self.x, self.y + self.size_y // 4, '[E]', (255, 255, 0))

        if get_time()- self.skill_count > 5:
            self.font.draw(self.x-50, self.y +self.size_y//4+ 25, 'Skill Ready', (0, 191, 255))
        else:
            self.font.draw(self.x-50, self.y +self.size_y//4+ 25, f'(Cooldown: {5-get_time()+self.skill_count:.2f})', (0, 191, 255))
        for i in range(self.hp):
            self.hp_png.draw(300 + i*100, 50, 100, 50)
        if self.near_portal:
            self.font.draw(self.x, self.y + self.size_y // 4, '[E]', (255, 255, 0))
        self.near_portal = False




    def get_bb(self):
        return self.x-self.size_x//6, self.y-self.size_y//4, self.x+self.size_x//6, self.y+self.size_y//6

    def handle_collision(self, group, other):
        if group == 'player:block' and self.vertical < 0:
            if self.png == 'Resource\\Sci-fi hero 64x65.png':
                self.y = other.y + (other.size_y // 4) + 15  # 블록 위에 위치
            else:
                self.y = other.y + (other.size_y // 2) + 15
            self.vertical = 0
            self.fall = False
            self.min_x, self.max_x = other.x - (other.size_x // 2), other.x + (other.size_x // 2)

        if group == 'player:monster' and other.state == 'Die':
            self.corpse = True
            if self.cliked_e:
                if  not self.charinfoexist[0]:
                    self.charinfoexist[0] = True
                    self.charinfo[0] = CharInfo(other.width, other.height, other.size_x, other.size_y, other.run_action, other.basic_atk_action, other.fall_action,other.idle_action, other.png, other.basic_atk_size_x, other.basic_atk_size_y, other.skill_atk_action, other.skill_atk_size_x, other.skill_atk_size_y, other.maxhp, other.basic_atk, other.skill,other.hit_sound)
                    game_world.remove_object(other)

                elif not self.charinfoexist[1]:
                    self.charinfoexist[1] = True
                    self.charinfo[1] = CharInfo(other.width, other.height, other.size_x, other.size_y, other.run_action, other.basic_atk_action, other.fall_action,other.idle_action, other.png, other.basic_atk_size_x, other.basic_atk_size_y, other.skill_atk_action, other.skill_atk_size_x, other.skill_atk_size_y, other.maxhp, other.basic_atk, other.skill,other.hit_sound)
                    game_world.remove_object(other)
                else:
                    temp = CharInfo(other.width, other.height, other.size_x, other.size_y, other.run_action, other.basic_atk_action, other.fall_action,other.idle_action, other.png, other.basic_atk_size_x, other.basic_atk_size_y, other.skill_atk_action, other.skill_atk_size_x, other.skill_atk_size_y, other.maxhp, other.hit_sound)
                    game_world.remove_object(other)
                    self.size_x, temp.size_x = temp.size_x, self.size_x
                    self.size_y, temp.size_y = temp.size_y, self.size_y
                    self.png, temp.png = temp.png, self.png
                    self.image = load_image(self.png)
                    temp.image = load_image(temp.png)
                    self.width, temp.width = temp.width, self.width
                    self.height, temp.height = temp.height, self.height
                    self.basic_atk_size_x, temp.basic_atk_size_x = temp.basic_atk_size_x, self.basic_atk_size_x
                    self.basic_atk_size_y, temp.basic_atk_size_y = temp.basic_atk_size_y, self.basic_atk_size_y
                    self.skill_atk_size_x, temp.skill_atk_size_x = temp.skill_atk_size_x, self.skill_atk_size_x
                    self.skill_atk_size_y, temp.skill_atk_size_y = temp.skill_atk_size_y, self.skill_atk_size_y
                    self.run_action, temp.run_action = temp.run_action, self.run_action
                    self.basic_atk_action, temp.basic_atk_action = temp.basic_atk_action, self.basic_atk_action
                    self.skill_atk_action, temp.skill_atk_action = temp.skill_atk_action, self.skill_atk_action
                    self.fall_action, temp.fall_action = temp.fall_action, self.fall_action
                    self.idle_action, temp.idle_action = temp.idle_action, self.idle_action
                    self.hp, temp.hp = temp.hp, self.hp
                    self.basic_atk, temp.basic_atk = temp.basic_atk, self.basic_atk
                    self.skill, temp.skill = temp.skill, self.skill
                    self.hit_sound[0], other.hit_sound[0] = other.hit_sound[0], self.hit_sound[0]
                    self.hit_sound[1],other.hit_sound[1] = other.hit_sound[1], self.hit_sound[1]

        else:
            self.corpse = False
        if group == 'player:portal':
            self.near_portal = True
            if self.cliked_e:
                self.cliked_e = False
                play_mode.game_change_1_2 = True





        if group == 'monsterATK:player':
            self.hp -=1
            self.y +=20
            self.vertical += 5
            self.fall = True
            self.hit_sound[randint(0,1)].play()






