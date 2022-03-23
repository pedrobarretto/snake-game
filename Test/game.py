import pygame
from network import Network
import time
import random
# print(pygame.font.get_fonts())

pygame.init()

class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.window_x = 720
        self.window_y = 480
        self.width = w
        self.height = h
        # self.player = Player(50, 50)
        # self.player2 = Player(100,100)
        self.canvas = Canvas(self.width, self.height, "Testing...")
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.yellow = pygame.Color(252, 207, 3)
        self.snake_position = [100, 50]
        self.snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]
        self.snake_position2 = [100, 50]
        self.snake_body2 = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]
        self.speed = 15
        self.direction = 'RIGHT'
        self.direction2 = 'LEFT'
        self.change_to = self.direction
        self.change_to2 = self.direction2
        self.score = 0
        self.score2 = 0

        self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
			random.randrange(1, (self.window_y//10)) * 10]

    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)

        score_surface = score_font.render('Score : ' + str(self.score), True, color)

        score_rect = score_surface.get_rect()

        self.canvas.get_canvas().blit(score_surface, score_rect)

    def game_over(self):
        my_font = pygame.font.SysFont('notosans', 50)

        game_over_surface = my_font.render(
            'Your Score is : ' + str(self.score), True, self.red)
 
        game_over_rect = game_over_surface.get_rect()
        
        game_over_rect.midtop = (self.window_x/2, self.window_y/4)
        
        self.canvas.get_canvas().blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        
        time.sleep(2)
        
        pygame.quit()
        
        quit()

    def run(self):
        clock = pygame.time.Clock()
        run = True

        self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
			random.randrange(1, (self.window_y//10)) * 10]
        fruit_spawn = True

        while run:
            clock.tick(self.speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'

            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            if self.direction == 'UP':
                self.snake_position[1] -= 10
            if self.direction == 'DOWN':
                self.snake_position[1] += 10
            if self.direction == 'LEFT':
                self.snake_position[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_position[0] += 10

            self.snake_body.insert(0, list(self.snake_position))
            if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
                self.score += 10
                fruit_spawn = False
            else:
                self.snake_body.pop()
                
            if not fruit_spawn:
                self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
                                random.randrange(1, (self.window_y//10)) * 10]
                
            fruit_spawn = True
            self.canvas.draw_background()
            
            for pos in self.snake_body:
                pygame.draw.rect(self.canvas.get_canvas(), self.blue,
                                pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(self.canvas.get_canvas(), self.white, pygame.Rect(
                self.fruit_position[0], self.fruit_position[1], 10, 10))

            if self.snake_position[0] < 0 or self.snake_position[0] > self.window_x-10:
                game_over()
            if self.snake_position[1] < 0 or self.snake_position[1] > self.window_y-10:
                game_over()

            for block in self.snake_body[1:]:
                if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                    game_over()

            self.show_score(1, self.white, 'notosans', 20)

            # self.player2.x, self.player2.y = self.parse_data(self.send_data())
            self.snake_body, self.snake_body2, self.snake_position, self.snake_position2, self.fruit_position, self.score, self.score2 = self.parse_data(self.send_data())

            # self.canvas.draw_background()
            # self.player.draw(self.canvas.get_canvas())
            # self.player2.draw(self.canvas.get_canvas())
            # self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        # data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        data = {
            'id': str(self.net.id),
            'snake_body': self.snake_body,
            'snake_body2': self.snake_body2,
            'snake_position': self.snake_position,
            'snake_position2': self.snake_position2,
            'fruit_position': self.fruit_position,
            'score': self.score,
            'score2': self.score2
        }
        print('send_data data >> ', data)
        reply = self.net.send(data)
        print('reply: ', reply)

        if ('gameover' in reply):
            pygame.quit()

        return reply

    @staticmethod
    def parse_data(data):
        try:
            # d = data.split(":")[1].split(",")
            # return int(d[0]), int(d[1])
            print('data: ', data)
            res = [
                #data.id
                data.snake_body, 
                data.snake_body2, 
                data.snake_position, 
                data.snake_position2, 
                data.fruit_position, 
                data.score,
                data.score2
            ]
            print('retornando res: ', res)
            return res or data
        except:
            print('retorno de array vazio')
            return [
                [[100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
                ],
                [[100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
                ],
                [100, 50],
                [100, 50],
                [10, 10],
                0,
                0
            ]


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
