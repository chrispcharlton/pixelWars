import pygame
import random


class Pixel(pygame.sprite.Sprite):

    def __init__(self, env, team_name, colour_rgb_code=(0, 0, 0), size=4, speed=2, start_position=None):
        # get properties of Sprite class
        super(Pixel, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(colour_rgb_code)
        self.speed = speed
        self.hp = 2
        self.attack_damage = 1
        self.team = team_name
        self.env = env
        self.enemy_team = pygame.sprite.Group()
        self.update_enemies()

        # set position
        self.x_max = self.env.x
        self.y_max = self.env.y
        if start_position is None:
            start_position = (self.x_max / 2,
                              self.y_max / 2)
        self.rect = self.surf.get_rect(center=start_position)
        # start off facing right (arbitrary)
        self.direction = (1, 0)

        self.actions = ["rotateLeft",
                        "rotateRight",
                        "rotateUp",
                        "rotateDown",
                        "move",
                        "attack"]
        self.is_alive = True

        self.record = []

    def update_enemies(self):
        enemies = pygame.sprite.Group()
        for key, value in self.env.teams.items():
            if key != self.team:
                enemies.add(value)
        self.enemy_team = enemies

    def check_boundaries(self):
        if self.rect.right > self.x_max:
            self.rect.right = self.x_max
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 1
        if self.rect.bottom > self.y_max:
            self.rect.bottom = self.y_max

    def check_collision(self, type='all'):
        if type == 'enemy':
            group_to_check = self.enemy_team
        else:
            group_to_check = self.env.all_sprites
        collided_pixel = pygame.sprite.spritecollideany(self, group_to_check, collided=None)
        return collided_pixel

    def handle_movement_collision(self,dx,dy,collided_pixel):
        # If a collision is detected, move so that there is no more collision (edges touching)
        if collided_pixel is not None:
            if dx > 0:
                self.rect.right = collided_pixel.rect.left
            if dx < 0:
                self.rect.left = collided_pixel.rect.right
            if dy > 0:
                self.rect.bottom = collided_pixel.rect.top
            if dy < 0:
                self.rect.top = collided_pixel.rect.bottom

    def move_single_axis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
        collided_pixel = self.check_collision()
        if collided_pixel is not None:
            self.handle_movement_collision(dx, dy, collided_pixel)
        self.check_boundaries()

    def move_forward(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def attack(self):
        # TODO: Currently an attack that does not hit will move the pixel in the direction it faces
        self.move_forward(self.direction[0], self.direction[1])
        collided_pixel = self.check_collision(type='enemy')
        if collided_pixel is not None:
            if collided_pixel.direction != tuple(-1*x for x in self.direction):
                collided_pixel.hp -= (self.attack_damage * 2)
            else:
                collided_pixel.hp -= self.attack_damage
        self.handle_movement_collision(self.direction[0], self.direction[1], collided_pixel)

    def choose_action(self):
        choice = random.randint(0, (len(self.actions)-1))
        choice = self.actions[choice]
        return choice

    def record_action(self,choice):
        self.record.append(choice)

    def do_action(self,choice):
        # maps action names to functions with inputs
        if choice == "rotateLeft":
            self.direction = (-1,0)
        if choice == "rotateRight":
            self.direction = (1, 0)
        if choice == "rotateUp":
            self.direction = (0, -1)
        if choice == "rotateDown":
            self.direction = (0, 1)
        if choice == "move":
            x = self.direction[0] * self.speed
            y = self.direction[1] * self.speed
            self.move_forward(x, y)
        if choice == "attack":
            self.attack()

    def check_death(self):
        if self.hp <= 0:
            print(str(self.team), "pixel has died")
            self.kill()

    def update(self, action):
        self.check_death()
        # action = self.choose_action()
        if self.env.record:
            self.record_action(action)
        self.do_action(action)
        self.check_boundaries()

