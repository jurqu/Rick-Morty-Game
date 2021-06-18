import pygame

from gameObject import GameObject
from player import Player
from enemy import Enemy

class Game:

    def __init__(self):
        self.width = 950
        self.height = 950
        self.game_colour = (85, 96, 153)
        self.game_window = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()

        ## self.background = GameObject(0, 0, self.width, self.height, 'assets/b1.png')
        self.treasure = GameObject(450, 50, 50, 50, 'assets/portal.png')

        self.level = 1.0 
        self.reset_map()
    pygame.init()
    start_sound = pygame.mixer.Sound('assets/start.wav')
    died = pygame.mixer.Sound('assets/die.wav')
    next_level = pygame.mixer.Sound('assets/next_level.wav')
    reset_level = pygame.mixer.Sound('assets/you_ok.wav')
    pygame.mixer.music.load('assets/theme_song.mp3')
    pygame.mixer.music.play(-1, 0.0)
    start_sound.play() 


    def reset_map(self):
        speed = 5 + (self.level * 2)
        self.player = Player(450, 850, 50, 50, 'assets/RM.png', speed)
        

        if self.level >= 4.0:
            self.background = GameObject(0, 0, self.width, self.height, 'assets/b3.png')
            self.enemies = [
            Enemy(0, 600, 50, 50, 'assets/enemy.png', speed),
            Enemy(900, 400, 50, 50, 'assets/enemy.png', speed),
            Enemy(0, 200, 50, 50, 'assets/enemy.png', speed),
            ]
        elif self.level >= 2.0:
            self.background = GameObject(0, 0, self.width, self.height, 'assets/b2.png')
            self.enemies = [
            Enemy(0, 600, 50, 50, 'assets/enemy.png', speed),
            Enemy(900, 400, 50, 50, 'assets/enemy.png', speed),
            ]
        else:
            self.background = GameObject(0, 0, self.width, self.height, 'assets/b1.png')
            self.enemies = [
                Enemy(0, 600, 50, 50, 'assets/enemy.png', speed)
            ] 



    def draw_objects(self):
        self.game_window.fill(self.game_colour)
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        self.game_window.blit(self.treasure.image, (self.treasure.x, self.treasure.y))
        self.game_window.blit(self.player.image, (self.player.x, self.player.y))

        for enemy in self.enemies:
            self.game_window.blit(enemy.image, (enemy.x, enemy.y))
        pygame.display.update()


    def move_objects(self, player_direction):
            self.player.move(player_direction, self.height)
            for enemy in self.enemies:
                enemy.move(self.width)

    def check_if_collided(self):
        for enemy in self.enemies:
            if self.detect_collision(self.player, enemy):
                self.level = 1.0
                self.died.play()
                return True
        if self.detect_collision(self.player, self.treasure):
            self.level += 0.5

            return True
        return False


    def detect_collision(self, object_1, object_2):
        if object_1.y > (object_2.y + object_2.height):
            return False
        elif (object_1.y + object_1.height) < object_2.y:
            return False
        
        if object_1.x > (object_2.x + object_2.width):
            return False
        elif (object_1.x + object_1.width) < object_2.x:
            return False
        return True


    def run_game_loop(self):
        player_direction = 0

        while True:
            events = pygame.event.get()
            for event in events: 
                if event.type == pygame.QUIT:
                    return

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_direction = -1
                    elif event.key == pygame.K_DOWN:
                        player_direction = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player_direction = 0


            self.move_objects(player_direction)
            
            # Update Display

            self.draw_objects()
            
            # Detect Collisions
            if self.check_if_collided():
                self.reset_map()

            self.clock.tick(60)