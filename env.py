import pygame
import pandas as pd
import random
from pixel import Pixel
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT


class Env(object):

    def __init__(self, x, y, colour_rgb_code=(255, 255, 255), record=False):
        pygame.init()
        self.x = x
        self.y = y
        self.screen = pygame.display.set_mode((self.x, self.y))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(colour_rgb_code)
        self.screen_array = pygame.surfarray.array2d(self.screen)
        self.all_sprites = pygame.sprite.Group()
        self.team_templates = []
        self.teams = {}
        self.record = record


    def choose_start_position(self, position):
        if type(position) == tuple:
            return position
        elif position == "left":
            position = (random.randint(0, (self.x * 0.2)), random.randint(0, self.y))
            return position
        elif position == "right":
            position = (random.randint((self.x * 0.8), self.x), random.randint(0, self.y))
            return position
        else:
            position = (random.randint(0, self.x), random.randint(0, self.y))
            print("Invalid start position (" + str(position) + ")")
            return position

    def add_team(self, team_dict):
        self.team_templates.append(team_dict)

    def spawn_team(self, team_dict):
        team = pygame.sprite.Group()

        for i in range(0, (team_dict['n']-1)):
            new_pixel = Pixel(env=self,
                              team_name=team_dict['team_name'],
                              size=team_dict['size'],
                              colour_rgb_code=team_dict['colour_rgb_code'],
                              start_position=self.choose_start_position(team_dict['start_position']))
            team.add(new_pixel)
            self.all_sprites.add(new_pixel)
        self.teams.update({team_dict['team_name']: team})
        return team

    def update_enemy_groups(self):
        for team in self.teams.values():
            pd.Series(team.sprites()).apply(lambda x: x.update_enemies())

    def check_for_game_end(self):
        for team_name in self.teams.keys():
            if len(self.teams[team_name].sprites()) == 0:
                print(team_name + " has been eliminated")
                return True
        return False

    def check_for_exit_key(self):
        # TODO: currently exit keys not working
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            elif event.type == QUIT:
                pygame.quit()
        return False

    def update_screen(self):
        self.screen.blit(self.background, (0, 0))
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
        self.screen_array = pygame.surfarray.array2d(self.screen)
        pygame.display.flip()

    def is_done(self):
        condition_1 = self.check_for_exit_key()
        condition_2 = self.check_for_game_end()
        if (condition_1) or (condition_2):
            return True
        else:
            return False

    def step(self, agent, action):
        agent.update(action)

        state = self.screen_array
        done = self.is_done()
        reward = 0
        info = []

        return state, reward, done, info

    def record_game_actions(self):
        #TODO: function to combine action records of each Pixel and sav as a file so the game can be replayed
        pass

    def reset(self):
        self.teams = {}
        for team in self.team_templates:
            self.spawn_team(team)
        self.update_enemy_groups()

    def close(self):
        pygame.quit()

if (__name__ == '__main__') | (__name__ == 'builtins'):

    env = Env(400, 400)
    env.add_team({'team_name': "red",
                        'n': 250,
                        'colour_rgb_code': (255, 0, 0),
                        'start_position': "left",
                        'size': 8})

    env.add_team({'team_name': "blue",
                        'n': 250,
                        'colour_rgb_code': (0, 0, 255),
                        'start_position': "right",
                        'size': 8})

    done = False
    env.reset()
    while not done:
        for pixel in env.all_sprites:
            action = pixel.choose_action()
            state, reward, done, info = env.step(pixel, action)
        env.update_screen()
    env.close()

