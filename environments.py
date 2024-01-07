import random
import sys
from copy import deepcopy

import pygame

from agents import Agent
from constants import WIDTH, HEIGHT, Point, Action, GameState


class GameEnvironment:
    def __init__(self, agent: Agent):
        self.agent = agent
        head = Point(WIDTH//2, HEIGHT//2)
        self._initial_tail = [Point(head.x, head.y-1), head]
        self.state = GameState(head=Point(WIDTH//2, HEIGHT//2), velocity=Point(0, 1), tail=self._initial_tail, food=self._initial_food_position())

    def _play_step(self, action):
        new_head, new_velocity = self._handle_action(action)
        new_food = self.state.food
        new_tail = deepcopy(self.state.tail)

        reward = 0

        if new_head == self.state.food:
            new_food = self._new_food_position()
            reward = 10
        else:
            new_tail.pop(0)

        new_tail.append(new_head)
        new_game_state = GameState(head=new_head, velocity=new_velocity, tail=new_tail, food=new_food)
        if self._will_collide(new_head):
            return -100, new_game_state, 1, len(new_game_state.tail) - 2

        return reward, new_game_state, 0, len(new_game_state.tail) - 2

    def _handle_action(self, action):
        if action == Action.TURN_RIGHT:
            new_velocity = Point(self.state.velocity.y, -self.state.velocity.x)
        elif action == Action.TURN_LEFT:
            new_velocity = Point(-self.state.velocity.y, self.state.velocity.x)
        else:
            new_velocity = Point(self.state.velocity.x, self.state.velocity.y)
        return Point(self.state.head.x + new_velocity.x, self.state.head.y + new_velocity.y), new_velocity

    def _will_collide(self, new_head):
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            return True
        if new_head in self.state.tail:
            return True
        return False

    def _initial_food_position(self):
        while True:
            new_position = Point(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if new_position not in self._initial_tail:
                return new_position

    def _new_food_position(self):
        while True:
            new_position = Point(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if new_position not in self.state.tail and new_position != self.state.food:
                return new_position

    def _iteration(self):
        action = self.agent.get_action(self.state)
        reward, next_state, game_over, score = self._play_step(action)
        self.agent.update_with_reward(self.state, action, reward, next_state, game_over)

        self.state = next_state

        return score, game_over

    def game_loop(self):
        while True:
            score, game_over = self._iteration()

            if game_over:
                break


class VisualGameEnvironment(GameEnvironment):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self._width = 500
        self._height = 500

        pygame.init()
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("snake")

    def game_loop(self):
        clock = pygame.time.Clock()

        self._draw_game(0, 0)
        pygame.display.flip()
        clock.tick(2)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            score, game_over = self._iteration()

            self._draw_game(score, game_over)

            pygame.display.flip()
            clock.tick(2)

            if game_over:
                break

    def _draw_game(self, score, game_over):
        self._screen.fill((255, 255, 255))

        body_width = self._width / WIDTH

        for body_part in self.state.tail:
            pygame.draw.rect(self._screen, (127, 127, 127), ((body_part.x*body_width, (HEIGHT-body_part.y-1) * body_width), (body_width, body_width)))

        pygame.draw.rect(self._screen, (230, 0, 0), ((self.state.food.x*body_width, (HEIGHT-self.state.food.y-1) * body_width), (body_width, body_width)))
        pygame.draw.rect(self._screen, (80, 80, 80), ((self.state.head.x * body_width, (HEIGHT - self.state.head.y - 1) * body_width), (body_width, body_width)))