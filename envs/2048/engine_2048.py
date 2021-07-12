import pygame
import random
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
GRID_SIZE = 20

# fontcolor, bgcolor
white = '#ffffff'
BgColor = '#cccccc'
colors = {
	1: 		['#b3adad', '#b3adad'],
	2: 		['#776e64', '#eee4da'],
	4: 		['#776e64', '#ede0c8'],
	8: 		['#f9f6f2', '#f2b179'],
	16: 	['#f9f6f2', '#f59563'],
	32: 	['#f9f6f2', '#f67c5f'],
	64: 	['#f9f6f2', '#f65e3b'],
	128: 	['#f9f6f2', '#edcf72'],
	256: 	['#f9f6f2', '#edcc61'],
	512: 	['#f9f6f2', '#edc850'],
	1024: 	['#f9f6f2', '#edc53f'],
	2048: 	['#f9f6f2', '#edc22e'],
}


class Engine_2048:
	def __init__(self):
		'''using powers as nos.
		Convert powers (x) to (2^x) in draw function'''
		self.grid = np.zeros((GRID_SIZE, GRID_SIZE)).astype('int32')
		
		self.dir_dict = {0: [1, 1],			# up 		(1, 1), 	(-1, 0)
						 1: [0, 1],			# left 		(0, 1), 	(0, -1)
						 2: [1, -1],		# down 		(1, -1), 	(1, 0)
						 3: [0, -1]}		# right 	(0, -1), 	(0, 1)

		self.header = SCREEN_HEIGHT - SCREEN_WIDTH
		self.cell_width = SCREEN_WIDTH//GRID_SIZE
		self.cell_height = (SCREEN_HEIGHT-self.header)//GRID_SIZE
		self.margin = min(self.cell_width, self.cell_height)//25
		self.font = pygame.font.SysFont('Arial', min(self.cell_width, self.cell_height)//2)
		self.header_font = pygame.font.SysFont('Arial', self.header//2)

		self.has_moved = False
		self.action_called = False
		self.is_stuck = False
		self.reached_goal = False
		self.total_reward = 0
		self.merge_reward = 0
		# self.has_collided = False
		# self.has_merged = False


		self.insert_choice = [1, 2]			# [2, 4, 8]
		self.insert_probs = [0.95, 0.05]
		self.insert_cell()

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
			return True
		else:
			return False

	def insert_cell(self):
		'''place a number from [2, 4, 8] randomly in an empty cell'''
		xs, ys = np.where(self.grid==0)
		if xs.size==0:
			return
		i = random.randrange(xs.size)
		n = np.random.choice(self.insert_choice, p=self.insert_probs)
		self.grid[xs[i], ys[i]] = n

	def shift(self, dirn, test=False):
		'''test=True -> change self.grid
		else -> dont alter self.grid'''

		x, y = dirn
		tmp_grid = self.grid.copy()
		if x:
			tmp_grid = tmp_grid.T
		tmp_grid = tmp_grid[::1, ::y]

		if not test:
			self.merge_reward = 0
		# default = RIGHT 
		for i in range(self.grid.shape[0]):
			row = tmp_grid[i]
			# shift
			# [3, 0, 1, 0]
			tmp_list = [j for j in row if j!=0]
			# [3, 1]
			tmp_list.extend( [0]*(row.size - len(tmp_list)) )
			# [3, 1, 0, 0]
			# merge
			# [3, 1, 1, 1, 0]
			for j in range(1, len(tmp_list)):
				if tmp_list[j]==tmp_list[j-1] and tmp_list[j]!=0:
					if not test:
						self.merge_reward += pow(2, tmp_list[j]+1)
					tmp_list[j-1]+=1
					tmp_list[j] = 0
			# shift
			# [3, 2, 0, 1, 0]
			tmp_list = [j for j in tmp_list if j!=0]
			tmp_list.extend( [0]*(row.size - len(tmp_list)) )
			# [3, 2, 1, 0, 0]

			tmp_grid[i, :] = np.array(tmp_list)

		if not test:
			self.total_reward += self.merge_reward

		tmp_grid = tmp_grid[::1, ::y]
		if x:
			tmp_grid = tmp_grid.T
		
		if (self.grid==tmp_grid).all():
			return False
		if not test:
			self.grid = tmp_grid
		return True

		# # shreyas
		# test_grid = self.grid.copy()
		# for i in range(len(self.grid)):
		# 	temp_x = i
		# 	for j in range(len(self.grid)):
		# 		temp_y = j
		# 		# print(i,j)
		# 		if(test_grid[i,j]==0):
		# 			continue
		# 		temp = test_grid[i,j]
		# 		while not (self.has_collided): #or self.has_merged):
		# 			temp_x+=dirn[0]
		# 			temp_y+=dirn[1]

		# 			if not (temp_x >= len(test_grid) or temp_x < 0 or temp_y >= len(test_grid) or temp_y < 0):
		# 				print(1)
						
		# 				if (test_grid[temp_x,temp_y]!=0 and test_grid[temp_x,temp_y]!=test_grid[temp_x-dirn[0],temp_y-dirn[1]]):
		# 					print(2)
		# 					continue
						
		# 				elif (test_grid[temp_x,temp_y]==test_grid[temp_x-dirn[0],temp_y-dirn[1]] and test_grid[temp_x,temp_y]!=0):
		# 					print(3)
		# 					test_grid[temp_x,temp_y]+=1
		# 					test_grid[temp_x-dirn[0],temp_y-dirn[1]]=0
		# 					#self.has_merged = True
		# 				else:
		# 					print(4)
		# 					test_grid[temp_x,temp_y] = temp
		# 					test_grid[temp_x-dirn[0],temp_y-dirn[1]] = 0
		# 					print("grid = \n",test_grid)
		# 					print("temp_x,temp_y = ",temp_x,temp_y)
		# 					print("temp_x-dirn[0],temp_y-dirn[1] = ",temp_x-dirn[0],temp_y-dirn[1])
		# 			else:
		# 				self.has_collided = True

		# 		self.has_collided = False
		# 		#self.has_merged = False

		# if(self.grid==test_grid).all():
		# 	return False
		# if not (test):
		# 	self.grid = test_grid
		# return True

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

	def draw(self, screen):
		'''draw the snake and food on the screen'''
		w, h, m, head = self.cell_width, self.cell_height, self.margin, self.header

		screen.fill(pygame.Color(white))
		pygame.draw.rect(screen, pygame.Color(BgColor), pygame.Rect(0, head, GRID_SIZE*w, GRID_SIZE*h), 0)

		text = self.header_font.render(str(self.total_reward), True, pygame.Color(colors[1][0]), None)
		textRect = text.get_rect()
		textRect.center = ( SCREEN_WIDTH//4, head//2)
		screen.blit(text, textRect)

		for i in range(self.grid.shape[0]):
			for j in range(self.grid.shape[1]):
				val = pow(2, self.grid[i, j])
				
				pygame.draw.rect(screen, pygame.Color(colors[val][1]), pygame.Rect(j*w+m, i*h+m + head, w-2*m, h-2*m), 0)

				text = self.font.render(str(val), True, pygame.Color(colors[val][0]), None)
				textRect = text.get_rect()
				textRect.center = ( j*w+(w//2), i*h+(h//2) + head)
				screen.blit(text, textRect)


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
		# reward += self.engine.merge_reward
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
				if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
					self.done = True

		self.engine.draw(self.screen)

		pygame.display.flip()
		self.clock.tick(self.game_speed)

	def run_game_loop(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
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

		self.engine.draw(self.screen)
		pygame.display.flip()
		self.clock.tick(self.game_speed)

		# if done:
		# 	pygame.time.wait(5*1000)

		return reward, done

	def close(self):
		pygame.display.quit()
		pygame.quit()
