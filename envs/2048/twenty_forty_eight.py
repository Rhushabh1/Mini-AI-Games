import pygame
import random
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 20
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Tester:
	def __init__(self):
		self.grid = np.array([[0,0,0,0],
							  [0,0,0,0],
							  [0,0,0,0],
							  [0,0,0,0]] , dtype='int32')

		# self.my_rows, self.my_cols = self.grid.shape
		# self.assign_grid = [[0]*my_cols]*my_rows

		# self.nos = list(range(1,11))

		
		self.dir_dict = {-1: [0, 0],		# stay
						 0: [-1, 0],		# up
						 1: [0, -1],		# left
						 2: [1, 0],			# down
						 3: [0, 1]}			# right


		self.direction = random.randrange(4)

		self.cell_width = SCREEN_WIDTH//GRID_SIZE
		self.cell_height = SCREEN_HEIGHT//GRID_SIZE

		self.row = random.randrange(self.grid.shape[0])
		self.column = random.randrange(self.grid.shape[0])
		self.grid[self.row,self.column] = pow(2,1)

		self.has_collided = False
		self.is_full = False
		# self.is_placed = False


	def placed(self,grid):
		row = random.randrange(self.grid.shape[0])
		column = random.randrange(self.grid.shape[0])

		if not (self.grid[row,column]):
			self.grid[row,column] = pow(2,1)
			# self.is_placed = True
		else:
			# self.is_placed = False
			placed(self.grid)



	def check_full(self,grid,i,j):
		count = 0
		for i in range(len(self.grid)):
			for j in range(len(self.grid)):
				if(self.grid[i,j] != 0):
					count+=1

		if(count == len(self.grid)*len(self.grid)):
			self.is_full == True
		else:
			self.is_full == False



	def merge(self,grid,dirn):
		for i in range(len(self.grid)):
			for j in range(len(self.grid)):
				if(self.grid[i,j]==self.grid[i+dirn[0],j+dirn[1]] and self.grid[i,j]!=0):
					self.grid[i,j]*=2
					self.grid[i+dirn[0],i+dirn[1]]=0
				



	def update(self):
		dirn = self.dir_dict[self.direction]
		for x in range(len(self.grid)):
			temp_x = x
			for y in range(len(self.grid)):
				temp_y = y

				while not (self.has_collided):
					self.check_full(self.grid,x,y)
					if not (self.is_full):

						temp_value = self.grid[temp_x,temp_y]
						temp_x+=dirn[0]
						temp_y+=dirn[1]
						if temp_x >= len(self.grid) or temp_x < 0:
							self.has_collided = True
						elif temp_y >= len(self.grid) or temp_y < 0:
							self.has_collided = True
						else:
							if self.grid[x,y] == 0 or self.grid[temp_x,temp_y] != 0:
								continue
							else:
								self.merge(self.grid,dirn)
								self.grid[temp_x,temp_y] = temp_value

				self.has_collided = False

		self.placed(self.grid)




	def draw(self, screen):
		'''draw the snake and food on the screen'''
		screen.fill((0, 0, 0))

		for x in range(self.grid.shape[0]):
			for y in range(self.grid.shape[1]):
				# pygame.draw.rect(screen, red, (y*self.cell_width,
				# 							x*self.cell_height,
				# 							self.cell_width, 
				# 							self.cell_height))
				screen.blit(self.path_img, (y*self.cell_width, x*self.cell_height))

		x_arr, y_arr = np.where(self.grid==0)
		for i in range(x_arr.shape[0]):
			x, y = x_arr[i],y_arr[i]
			# pygame.draw.rect(screen, red, (y*self.cell_width,
			# 							x*self.cell_height,
			# 							self.cell_width, 
			# 							self.cell_height))
			screen.blit(self.wall_img, (y*self.cell_width, x*self.cell_height))

		x, y = self.end
		# pygame.draw.rect(screen, green, (y*self.cell_width,
		# 								x*self.cell_height,
		# 								self.cell_width, 
		# 								self.cell_height))
		screen.blit(self.end_img, (y*self.cell_width, x*self.cell_height))
		x, y = self.start
		# pygame.draw.rect(screen, green, (y*self.cell_width,
		# 								x*self.cell_height,
		# 								self.cell_width, 
		# 								self.cell_height))
		screen.blit(self.start_img, (y*self.cell_width, x*self.cell_height))
		x, y = self.pos
		# pygame.draw.rect(screen, blue, (y*self.cell_width,
		# 								x*self.cell_height,
		# 								self.cell_width, 
		# 								self.cell_height))
		screen.blit(self.player_img, (y*self.cell_width, x*self.cell_height))


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
		pygame.display.set_caption("Maze")
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('Arial', 30)
		self.tester = Tester()
		self.game_speed = 10
		if self.mode == 'human':
			self.game_speed = 10

		self.crash_penalty = -10
		self.finish_reward = 1000
		self.move_penalty = -1

	def get_human_action(self):
		assert self.mode == 'human', "return_action() not usable without 'human' mode for gym env."
		action = self.human_action
		self.human_action = self.no_op_action 		# no input action
		return action

	def action(self, action):
		'''update state by taking action
		check for collisions and endpoint
		-1 -> stop at position (do nothing)
		0 -> up 	1 -> left   2 -> down   3 -> right'''
		if action != -1:
			self.tester.direction = action
			self.tester.no_action = False
		else:	# action == -1:
			self.tester.no_action = True
		self.tester.update()

	def evaluate(self):
		'''compute reward of the tester'''
		reward = 0
		if self.tester.has_moved:
			reward += self.move_penalty
		if self.tester.has_collided:
			reward += self.crash_penalty
		if self.tester.reached:
			reward += self.finish_reward
		# print(reward)
		return reward

	def is_done(self):
		'''check for terminal condition or crash'''
		if self.tester.reached or self.done:
			self.done = False
			return True
		return False

	def observe(self):
		'''return next state upon taking action'''
		return self.tester.grid.flatten()

	def view(self):
		'''render the state of the game on the screen'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.done = True

		self.tester.draw(self.screen)

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

		self.tester.draw(self.screen)
		pygame.display.flip()
		self.clock.tick(self.game_speed)

		return reward, done

	def close(self):
		pygame.display.quit()
		pygame.quit()
