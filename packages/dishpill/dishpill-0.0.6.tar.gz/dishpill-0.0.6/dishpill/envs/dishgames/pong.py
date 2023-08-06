import time
import random
from typing import Optional

import numpy as np

import dishpill
from dishpill import error, spaces
from dishpill.error import DependencyNotInstalled



WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

ctrl = 0
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2

class Pong(dishpill.Env):
    
    def __init__(self, hardcore: bool = False):
        self.score1 = 0 
        self.score2 = 0
        self.paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
        self.paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
        self.l_score = 0
        self.r_score = 0
        self.paddle1_vel = 0
        self.paddle2_vel = 0
        self.ball_pos = [0, 0]
        self.ball_vel = [0, 0]
        self.screen = None
        self.clock = None
        self.action_space = spaces.Discrete(3)

        if random.randrange(0, 2) == 0:
            self.ball_init(True)
        else:
            self.ball_init(False)

    def ball_init(self,right):
        self.ball_pos = [WIDTH // 2, HEIGHT // 2]
        horz = random.randrange(2, 4)
        vert = random.randrange(1, 3)

        if right == False:
            horz = -horz

        self.ball_vel = [horz, -vert]

    def _destroy(self):
        self.game_over = True

    def reset(self):
        super().reset()
        self.game_over = False
        self._destroy()
        self.ball_init(True)

    def step(self, action):
        if action == 1:
            self.paddle2_vel = -8
        elif action == 2:
            self.paddle2_vel = 8
        else:
            self.paddle2_vel = 0
        if self.paddle1_pos[1] > HALF_PAD_HEIGHT and self.paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            self.paddle1_pos[1] += self.paddle1_vel
        elif self.paddle1_pos[1] == HALF_PAD_HEIGHT and self.paddle1_vel > 0:
            self.paddle1_pos[1] += self.paddle1_vel
        elif self.paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and self.paddle1_vel < 0:
            self.paddle1_pos[1] += self.paddle1_vel

        if self.paddle2_pos[1] > HALF_PAD_HEIGHT and self.paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            self.paddle2_pos[1] += self.paddle2_vel
        elif self.paddle2_pos[1] == HALF_PAD_HEIGHT and self.paddle2_vel > 0:
            self.paddle2_pos[1] += self.paddle2_vel
        elif self.paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and self.paddle2_vel < 0:
            self.paddle2_pos[1] += self.paddle2_vel

        self.ball_pos[0] += int(self.ball_vel[0])
        self.ball_pos[1] += int(self.ball_vel[1])

        if int(self.ball_pos[1]) <= BALL_RADIUS:
            self.ball_vel[1] = -self.ball_vel[1]
        if int(self.ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
            self.ball_vel[1] = -self.ball_vel[1]

        done = False
        if int(self.ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(self.ball_pos[1]) in range(
            self.paddle1_pos[1] - HALF_PAD_HEIGHT, self.paddle1_pos[1] + HALF_PAD_HEIGHT, 1
        ):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= 1.1
            self.ball_vel[1] *= 1.1
        elif int(self.ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
            self.r_score += 1
            done = True
            self.ball_init(True)

        if int(self.ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(
            self.ball_pos[1]
        ) in range(self.paddle2_pos[1] - HALF_PAD_HEIGHT, self.paddle2_pos[1] + HALF_PAD_HEIGHT, 1):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= 1.1
            self.ball_vel[1] *= 1.1
        elif int(self.ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
            self.l_score += 1
            done = True
            self.ball_init(False)

        reward =  self.r_score   
        state = [self.ball_pos[0],self.ball_pos[1], self.paddle1_pos[0],self.paddle1_pos[1],self.paddle2_pos[0],self.paddle2_pos[1]]
        return np.array(state, dtype=np.float32), reward, done, {}

    def render(self, mode: str = "human"):
        global ctrl
        try:
            import pygame
            from pygame import gfxdraw
        except ImportError:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install dishpill[pong]`"
            )

        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT),0,32)
            pygame.display.set_caption("DishPong")
        if self.clock is None:
            self.clock = pygame.time.Clock()

        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
        pygame.draw.line(self.screen, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(
            self.screen, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1
        )
        pygame.draw.circle(self.screen, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)
        pygame.draw.circle(self.screen, ORANGE, self.ball_pos, 20, 0)
        pygame.draw.polygon(
            self.screen,
            GREEN,
            [
                [self.paddle1_pos[0] - HALF_PAD_WIDTH, self.paddle1_pos[1] - HALF_PAD_HEIGHT],
                [self.paddle1_pos[0] - HALF_PAD_WIDTH, self.paddle1_pos[1] + HALF_PAD_HEIGHT],
                [self.paddle1_pos[0] + HALF_PAD_WIDTH, self.paddle1_pos[1] + HALF_PAD_HEIGHT],
                [self.paddle1_pos[0] + HALF_PAD_WIDTH, self.paddle1_pos[1] - HALF_PAD_HEIGHT],
            ],
            0,
        )
        pygame.draw.polygon(
            self.screen,
            GREEN,
            [
                [self.paddle2_pos[0] - HALF_PAD_WIDTH, self.paddle2_pos[1] - HALF_PAD_HEIGHT],
                [self.paddle2_pos[0] - HALF_PAD_WIDTH, self.paddle2_pos[1] + HALF_PAD_HEIGHT],
                [self.paddle2_pos[0] + HALF_PAD_WIDTH, self.paddle2_pos[1] + HALF_PAD_HEIGHT],
                [self.paddle2_pos[0] + HALF_PAD_WIDTH, self.paddle2_pos[1] - HALF_PAD_HEIGHT],
            ],
            0,
        )
        myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
        label1 = myfont1.render("Score " + str(self.l_score), 1, (255, 255, 0))
        self.screen.blit(label1, (50, 20))

        myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
        label2 = myfont2.render("Score " + str(self.r_score), 1, (255, 255, 0))
        self.screen.blit(label2, (470, 20))
        
        pygame.display.update()
        self.clock.tick(60)
        # print(self.ball_pos[0],self.ball_pos[1], self.paddle1_pos[0],self.paddle1_pos[1],self.paddle2_pos[0],self.paddle2_pos[1])
        # ctrl+=1
        # if ctrl > 5:
        #     raise TypeError("Oups!")
        
        

    def close(self):
        if self.screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()
            self.isopen = False



if __name__ == "__main__":
    # Heurisic: suboptimal, have no notion of balance.
    env = Pong()
    env.reset()
    
    steps = 0
    total_reward = 0
    
    for _ in range (0,100):
        
        a = random.randrange(0,2)
        print(a)
        s, r, done, info = env.step(a)
        time.sleep(1)
        print(s,r,done,info)
        env.render()
        # if done:
        #     break
