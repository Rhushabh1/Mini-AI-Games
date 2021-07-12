import pygame
import random
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 20
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Engine_2048:
	def __init__(self):
		'''using powers as nos.
		Convert powers (x) to (2^x) in draw function'''
		self.grid = np.zeros((GRID_SIZE, GRID_SIZE)).astype('int32')
		
		self.dir_dict = {0: [-1, 0],		# up
						 1: [0, -1],		# left
						 2: [1, 0],			# down
						 3: [0, 1]}			# right

		self.cell_width = SCREEN_WIDTH//GRID_SIZE
		self.cell_height = SCREEN_HEIGHT//GRID_SIZE

		self.has_moved = False
		self.action_called = False
		self.is_stuck = False
		self.reached_goal = False
		self.has_collided = False
		self.has_merged = False

		self.insert_choice = [1, 2, 3]			# [2, 4, 8]
		self.insert_probs = [0.7, 0.2, 0.1]
		self.insert_cell()

	def find_empty_cells(self):
		'''returns an empty cell coordinates'''
		xs, ys = np.where(self.grid==0)
		i = random.randrange(xs.size)
		return (xs[i], ys[i])

	def check_stuck(self):
		'''stuck when the there are no possible moves left'''
		xs, ys = np.where(self.grid==0)
		if xs.size>0:
			return False
		for i in range(4):
			dirn = self.dir_dict[i]
			success = self.shift(dirn, test=True)
			if success:
				return False
		return True

	def check_goal(self):
		'''check if 2048 is reached'''
		xs, ys = np.where(self.grid==11)
		if xs.size>0:
			self.reached_goal = True
		else:
			self.reached_goal = False

	def insert_cell(self):
		'''place a number from [2, 4, 8] randomly in an empty cell'''
		x, y = self.find_empty_cells()
		n = np.random.choice(self.insert_choice, p=self.insert_probs)
		self.grid[x, y] = n

	def shift(self, dirn, test=False):
		'''test=True -> change self.grid
		else -> dont alter self.grid'''
		test_grid = self.grid.copy()
		for i in range(self.grid.shape[0]):
			temp_x = i
			for j in range(self.grid.shape[0]):
				temp_y = j
				# print(i,j)
				if(test_grid[i,j]==0):
					continue
				temp = test_grid[i,j]
				while not (self.has_collided): #or self.has_merged):
					temp_x+=dirn[0]
					temp_y+=dirn[1]

					if not (temp_x >= len(test_grid) or temp_x < 0 or temp_y >= len(test_grid) or temp_y < 0):
						print(1)
						
						if (test_grid[temp_x,temp_y]!=0 and test_grid[temp_x,temp_y]!=test_grid[temp_x-dirn[0],temp_y-dirn[1]]):
							print(2)
							continue
						
						elif (test_grid[temp_x,temp_y]==test_grid[temp_x-dirn[0],temp_y-dirn[1]] and test_grid[temp_x,temp_y]!=0):
							print(3)
							test_grid[temp_x,temp_y]+=1
							test_grid[temp_x-dirn[0],temp_y-dirn[1]]=0
							#self.has_merged = True
						else:
							print(4)
							test_grid[temp_x,temp_y] = temp
							test_grid[temp_x-dirn[0],temp_y-dirn[1]] = 0
							print("grid = \n",test_grid)
							print("temp_x,temp_y = ",temp_x,temp_y)
							print("temp_x-dirn[0],temp_y-dirn[1] = ",temp_x-dirn[0],temp_y-dirn[1])
					else:
						self.has_collided = True

				self.has_collided = False
				#self.has_merged = False

		if(self.grid==test_grid).all():
			return False
		if not (test):
			self.grid = test_grid
		return True


		# return merge successful bool

	def move(self, action):
		'''shift the cells using input action'''
		dirn = self.dir_dict[action]
		self.action_called = self.shift(dirn)
		if self.action_called:
			self.insert_cell()

	def update(self):
		if self.action_called:
			self.is_stuck = self.check_stuck()
			self.reached_goal = self.check_goal()
		self.has_moved = self.action_called
		self.action_called = False


		# dirn = self.dir_dict[self.direction]
		# for x in range(len(self.grid)):
		# 	temp_x = x
		# 	for y in range(len(self.grid)):
		# 		temp_y = y

		# 		while not (self.has_collided):
		# 			self.check_full(self.grid,x,y)
		# 			if not (self.is_full):

		# 				temp_value = self.grid[temp_x,temp_y]
		# 				temp_x+=dirn[0]
		# 				temp_y+=dirn[1]
		# 				if temp_x >= len(self.grid) or temp_x < 0:
		# 					self.has_collided = True
		# 				elif temp_y >= len(self.grid) or temp_y < 0:
		# 					self.has_collided = True
		# 				else:
		# 					if self.grid[x,y] == 0 or self.grid[temp_x,temp_y] != 0:
		# 						continue
		# 					else:
		# 						self.merge(self.grid,dirn)
		# 						self.grid[temp_x,temp_y] = temp_value

		# 		self.has_collided = False

		# self.placed(self.grid)

	def draw(self, screen, font):
		'''draw the snake and food on the screen'''
		screen.fill((0, 0, 0))
		# screen.blit(self.path_img, (y*self.cell_width, x*self.cell_height))
		print(self.grid)


class Pygame2D:
	def __init__(self, grid_size=20, mode='bot'):
		'''Initialise pygame and display attributes'''
		global GRID_SIZE
		GRID_SIZE = grid_size
		allowed_modes = ['bot', 'human']
		assert mode in allowed_modes, "Wrong mode for gym env. Should be from ['bot', 'human']"

		self.mode = mode
		self.done = False
		self.no_op_action = -1 		# action which does nothing
		self.human_action = self.no_op_action

		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("2048")
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('Arial', 30)
		self.engine = Engine_2048()
		self.game_speed = 10
		if self.mode == 'human':
			self.game_speed = 60

		self.stuck_penalty = -100
		self.finish_reward = 1000
		self.move_penalty = -1

		self.description = "========CONTROLS========\
		\nUp arrow\t: move up\
		\nDown arrow\t: move down\
		\nLeft arrow\t: move left\
		\nRight arrow\t: move right\
		\n========================"

	def get_human_action(self):
		assert self.mode == 'human', "return_action() not usable without 'human' mode for gym env."
		action = self.human_action
		self.human_action = self.no_op_action 		# no input action
		return action

	def action(self, action):
		'''update state by taking action
		-1 -> stop at position (do nothing)
		0 -> up 	1 -> left   2 -> down   3 -> right'''
		if action != -1:
			self.engine.move(action)
		self.engine.update()

	def evaluate(self):
		'''compute reward of the engine'''
		reward = 0
		if self.engine.has_moved:
			reward += self.move_penalty
		if self.engine.is_stuck:
			reward += self.stuck_penalty
		if self.engine.reached_goal:
			reward += self.finish_reward
		return reward

	def is_done(self):
		'''check for terminal condition or crash'''
		if self.engine.is_stuck or self.engine.reached_goal or self.done:
			self.done = False
			return True
		return False

	def observe(self):
		'''return next state upon taking action'''
		return self.engine.grid.flatten()

	def view(self):
		'''render the state of the game on the screen'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.done = True

		self.engine.draw(self.screen, self.font)

		pygame.display.flip()
		self.clock.tick(self.game_speed)

	def run_game_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.done = True
				if self.mode == 'human':
					if event.key == pygame.K_RETURN:
						self.done = True
					elif event.key == pygame.K_UP:
						self.human_action = 0
					elif event.key == pygame.K_LEFT:
						self.human_action = 1
					elif event.key == pygame.K_DOWN:
						self.human_action = 2
					elif event.key == pygame.K_RIGHT:
						self.human_action = 3

		action = self.get_human_action()
		self.action(action)
		reward = self.evaluate()
		done = self.is_done()

		self.engine.draw(self.screen,self.font)
		pygame.display.flip()
		self.clock.tick(self.game_speed)

		return reward, done

	def close(self):
		pygame.display.quit()
		pygame.quit()
