import gym
from gym import spaces
import numpy as np
from cube2d import Pygame2D

class CustomEnv(gym.Env):
	def __init__(self, mode='bot', level=200):
		'''Set the action and observation spaces
		Initialise the pygame object'''
		super().__init__()
		self.mode = mode
		self.level = level
		self.pygame = Pygame2D(mode=self.mode, level=self.level)
		self.description = self.pygame.description
		self.action_space = spaces.Discrete(24)
		self.observation_space = spaces.MultiDiscrete([6 for _ in range(6*3*3)])	# 1 for each of the 6 faces

	def reset(self):
		'''Re-initialise the pygame object
		Return -> starting state of env'''
		del self.pygame 
		self.pygame = Pygame2D(mode=self.mode, level=self.level)
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
