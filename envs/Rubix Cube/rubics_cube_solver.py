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
		0 -> wall
		1 -> empty cell (empty path)
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
							 [0,0,0,0,0,1,1,1,1,1]] , dtype='int32')

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
		self.start = (9, 9)
		self.end = (0, 0)
		self.pos = self.start				# pos is tester
		self.dir_dict = {-1: [0, 0],		# stay
						 0: [-1, 0],		# up
						 1: [0, -1],		# left
						 2: [1, 0],			# down
						 3: [0, 1]}			# right
		self.direction = random.randrange(4)

		self.has_collided = False
		self.reached = False
		self.has_moved = False
		self.no_action = False
		self.cell_width = SCREEN_WIDTH//GRID_SIZE
		self.cell_height = SCREEN_HEIGHT//GRID_SIZE

		self.wall_img = pygame.image.load("./maze_assets/wall.png")
		self.path_img = pygame.image.load("./maze_assets/path.png")
		self.start_img = pygame.image.load("./maze_assets/start.png")
		self.end_img = pygame.image.load("./maze_assets/end.png")
		self.player_img = pygame.image.load("./maze_assets/player.png")
		self.wall_img = pygame.transform.scale(self.wall_img, (self.cell_width, self.cell_height))
		self.path_img = pygame.transform.scale(self.path_img, (self.cell_width, self.cell_height))
		self.start_img = pygame.transform.scale(self.start_img, (self.cell_width, self.cell_height))
		self.end_img = pygame.transform.scale(self.end_img, (self.cell_width, self.cell_height))
		self.player_img = pygame.transform.scale(self.player_img, (self.cell_width, self.cell_height))

		self.grid[self.start] = 3
		self.grid[self.end] = 4
		self.grid[self.pos] = 2

	# def hash(self, n):
	# 	x, y = n
	# 	return x*self.grid.shape[1] + y

	# def inv_hash(self, n):
	# 	cols = self.grid.shape[1]
	# 	return (n//cols, n%cols)

	# def find_empty_cells(self):
	# 	flat_map = self.grid.flatten()
	# 	flat_map = (flat_map == 0)
	# 	empty_cells = np.arange(GRID_SIZE*GRID_SIZE)[flat_map]
	# 	empty_cells = np.random.choice(list(empty_cells), k, replace=False)
	# 	empty_cells = [self.inv_hash(h) for h in empty_cells]
	# 	return empty_cells
		
	def check_collision(self, trainer):
		'''check if tester has collided with wall or outside of map'''
		self.has_collided = False
		x, y = trainer
		if x >= GRID_SIZE or x < 0:
			self.has_collided = True
		elif y >= GRID_SIZE or y < 0:
			self.has_collided = True
		elif self.grid[x, y]==0:		# wall
			self.has_collided = True
		if self.no_action:
			self.has_collided = False

		self.reached = False
		if trainer == self.end and not self.no_action:
			self.reached = True

	def update(self):
		# print("1", self.has_collided)
		if not (self.reached):
			x, y = self.pos
			dirn = self.dir_dict[self.direction]
			new_head = (x + dirn[0], 
						y + dirn[1])

			self.check_collision(new_head)

			if not (self.has_collided or self.no_action):
				if self.pos == self.start:
					self.grid[self.pos] = 3
				else:
					self.grid[self.pos] = 1 	# old position
				self.pos = new_head
				self.grid[self.pos] = 2 	# new position
				self.has_moved = True

		if (self.reached or self.has_collided or self.no_action):
			self.has_moved = False

		# print("2", self.has_collided)

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
