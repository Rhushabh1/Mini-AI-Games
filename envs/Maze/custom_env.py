import gym
from gym import spaces
import numpy as np
from maze_test import Pygame2D

class CustomEnv(gym.Env):
	def __init__(self, grid_size=10, mode='bot'):
		'''Set the action and observation spaces
		Initialise the pygame object'''
		super().__init__()
		self.mode = mode
		self.grid_size = grid_size
		self.pygame = Pygame2D(self.grid_size, mode=self.mode)
		self.action_space = spaces.Discrete(4)		# 0-->front, 1-->left, 2-->back, 3-->right
		self.observation_space = spaces.MultiDiscrete([5 for _ in range(self.grid_size*self.grid_size)])

	def reset(self):
		'''Re-initialise the pygame object
		Return -> starting state of env'''
		del self.pygame 
		self.pygame = Pygame2D(self.grid_size, mode=self.mode)
		obs = self.pygame.observe()
		return obs

	def get_action(self):
		return self.pygame.get_human_action()

	def step(self, action):
		'''Take the action & update the env
		Return -> next_state, reward, done, info'''
		self.pygame.action(action)
		obs = self.pygame.observe()
		reward = self.pygame.evaluate()
		done = self.pygame.is_done()
		return obs, reward, done, {}

	def render(self, mode='bot', close=False):
		'''Render the env on the screen'''
		self.pygame.view()

	def play(self, max_try):
		'''Simulate 1 episode of Single player game'''
		score = 0
		self.reset()
		for t in range(max_try):
			reward, done = self.pygame.run_game_loop()
			score += reward
			if done:
				break
		self.reset()
		return score, done, {'time':t}

	def close(self):
		self.pygame.close()
		del self.pygame
