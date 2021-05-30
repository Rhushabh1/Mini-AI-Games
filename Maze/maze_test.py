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
		'''Initialise the snake, food and grid attributes
		0 -> empty cell (empty path)
		1 -> wall
		2 -> tester
		3 -> start of maze
		4 -> end of maze'''
		self.grid = np.array([[1,1,1,1,0,0,1,1,1,0],
                     		 [0,0,1,0,0,1,1,0,1,0],
                     		 [0,0,1,1,1,1,0,0,1,0],
                     		 [1,1,0,0,0,0,0,1,1,0],
                     		 [1,0,1,1,1,1,1,1,0,0],
                     		 [1,0,1,0,0,0,0,0,1,1],
                     		 [1,1,1,0,1,1,1,1,1,0],
                     		 [0,1,0,1,1,0,0,0,1,0],
                     		 [0,1,1,1,0,1,0,0,1,0],
                     		 [0,0,0,0,0,1,1,1,1,1]])

		'''
                  y-> 0 1 2 3 4
		x = 0[0 0 1 0 1]
		x = 1[1 0 1 0 0]
		x = 2[1 0 0 0 1]
		x = 3[0 1 1 0 1]
		x = 4[0 0 0 0 0]
		   0
		   |
		1-----3
		   |
		   2
		'''
		start=[9,9]
		end=[0,0]
		self.pos = start		                # pos is tester
		self.dir_dict = {0: [-1, 0],		        # up
				 1: [0, -1],			# left
				 2: [1, 0],			# down
				 3: [0, 1]}			# right
		self.direction = random.randrange(4)

		self.is_alive = True
		self.cell_width = SCREEN_WIDTH//GRID_SIZE
		self.cell_height = SCREEN_HEIGHT//GRID_SIZE

		self.grid[self.pos[0],[self.pos[1]]] = 2

	def hash(self, n):
		x, y = n
		return x*self.grid.shape[1] + y

	def inv_hash(self, n):
		cols = self.grid.shape[1]
		return (n//cols, n%cols)

	def find_empty_cells(self):
		flat_map = self.grid.flatten()
		flat_map = (flat_map == 0)
		empty_cells = np.arange(GRID_SIZE*GRID_SIZE)[flat_map]
		empty_cells = np.random.choice(list(empty_cells), k, replace=False)
		empty_cells = [self.inv_hash(h) for h in empty_cells]
		return empty_cells
		
	def check_collision(self, trainer):
		'''check if tester has collided with wall or outside of map'''
		self.is_alive = True
		x, y = trainer
		if grid[x][y]==1:
			self.is_alive = False
		elif x >= GRID_SIZE or x < 0:
			self.is_alive = False
		elif y >= GRID_SIZE or y < 0:
			self.is_alive = False

	def update(self):
		if self.is_alive:
			x,y = trainer
			if x==0 and y==0:
				return True

	def draw(self, screen):
		'''draw the snake and food on the screen'''
		screen.fill((0, 0, 0))

		x_arr,y_arr=np.where(self.grid==False)
		for i in range(len(x_arr)):
			x,y=x_arr[i],y_arr[i]
			pygame.draw.rect(screen, red, (y*self.cell_width,
										x*self.cell_height,
										self.cell_width, 
										self.cell_height))



		x, y = self.pos
		pygame.draw.rect(screen, blue, (y*self.cell_width,
										x*self.cell_height,
										self.cell_width, 
										self.cell_height))


class Pygame2D:
	def __init__(self, grid_size=20, mode='bot'):
		'''Initialise pygame and display attributes'''
		global GRID_SIZE
		GRID_SIZE = grid_size
		allowed_modes = ['bot', 'human']
		assert mode in allowed_modes, "Wrong mode for gym env. Should be from ['bot', 'human']"

		self.mode = mode
		self.done = False
		self.no_op_action = 1 		# action which does nothing
		self.human_action = self.no_op_action

		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Maze")
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('Arial', 30)
		self.tester = Tester()
		self.game_speed = 60
		if self.mode == 'human':
			self.game_speed = 10

		self.dead_penalty = -1000
		self.finish_reward = 1000
		self.move_penalty = -1

	def get_human_action(self):
		assert self.mode == 'human', "return_action() not usable without 'human' mode for gym env."
		action = self.human_action
		self.human_action = self.no_op_action
		return action

	def action(self, action):
		'''update state by taking action
		check for collisions and food
		0 -> left	1 -> straight   2 -> right   3 -> backward'''
		if action == 0:
			self.tester.direction = (self.tester.direction + 1)%4
		elif action == 2:
			self.tester.direction = (self.tester.direction - 1)%4
		elif action == 3:
			self.tester.direction = (self.tester.direction + 2)%4
		# if action == 1:	# do nothing

	def evaluate(self):
		'''compute reward of the tester'''
		reward = self.move_penalty
		if not self.tester.is_alive:
			reward += self.dead_penalty
		if self.tester.update:
                        reward += self.finish_reward
		return reward

	def is_done(self):
		'''check for terminal condition or crash'''
		if not self.tester.is_alive or self.done:
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
					elif event.key == pygame.K_LEFT:
						self.human_action = 0
					elif event.key == pygame.K_UP:
						self.human_action = 1
					elif event.key == pygame.K_RIGHT:
						self.human_action = 2

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
