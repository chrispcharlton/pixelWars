import pygame
import pandas as pd
import random
from pygame.locals import *
from pixel import Pixel


class Env(object):

    def __init__(self, x, y, colour_rgb_code=(255, 255, 255), record=False):
        pygame.init()
        self.x = x
        self.y = y
        self.screen = pygame.display.set_mode((self.x, self.y))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(colour_rgb_code)
        self.all_sprites = pygame.sprite.Group()
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

    def spawn_team(self, name="", colour_rgb_code=(0, 0, 0), n=500, position="left", size=4):
        team = pygame.sprite.Group()
        for i in range(0, (n-1)):
            new_pixel = Pixel(env=self,
                              team_name=name,
                              size=size,
                              colour_rgb_code=colour_rgb_code,
                              start_position=self.choose_start_position(position))
            team.add(new_pixel)
            self.all_sprites.add(new_pixel)
        self.teams.update({name: team})
        return team

    def update_enemy_groups(self):
        for team in self.teams.values():
            pd.Series(team.sprites()).apply(lambda x: x.update_enemies())

    def check_for_game_end(self):
        for team_name in self.teams.keys():
            if len(self.teams[team_name].sprites()) == 0:
                running = False
                print(team_name + " has been eliminated")
                return running
        running = True
        return running

    def check_for_exit_key(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
            elif event.type == QUIT:
                return False
        return True

    def update_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.update()
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
        pygame.display.flip()

    def game_loop(self):
        running = self.check_for_exit_key()
        if not running:
            return running
        running = self.check_for_game_end()
        if not running:
            return running
        self.update_screen()
        return running

    def record_game_actions(self):
        #TODO: function to combine action records of each Pixel and sav as a file so the game can be replayed
        pass

    def run(self):
        self.update_enemy_groups()
        running = True
        while running:
            running = self.game_loop()
        pygame.quit()
        if self.record:
            self.record_game_actions()

if (__name__ == '__main__') | (__name__ == 'builtins'):

    env = Env(400, 400)

    red = env.spawn_team("red", (255, 0, 0), position="left", n=250, size=8)
    blue = env.spawn_team("blue", (0, 0, 255), position="right", n=250, size=8)

    env.run()
