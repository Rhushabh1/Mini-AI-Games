import pygame
import random
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 20
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Snake:
	def __init__(self):
		'''Initialise the snake, food and grid attributes
		0 -> empty cell
		1 -> snake body
		2 -> food'''
		self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype='int32')

		tmp = self.find_empty_cells(k=2)
		self.pos = [tmp[0]]		# pos[0] is head
		self.food = tmp[1]
		self.dir_dict = {0: [-1, 0],		# up
						1: [0, -1],			# left
						2: [1, 0],			# down
						3: [0, 1]}			# right
		self.direction = random.randrange(4)

		self.length = len(self.pos)
		self.is_alive = True
		self.length_limit = GRID_SIZE*GRID_SIZE
		self.ate_food = False
		self.cell_width = SCREEN_WIDTH//GRID_SIZE
		self.cell_height = SCREEN_HEIGHT//GRID_SIZE

		self.grid[self.food] = 2
		for p in self.pos:
			self.grid[p] = 1

	def hash(self, n):
		x, y = n
		return x*self.grid.shape[1] + y

	def inv_hash(self, n):
		cols = self.grid.shape[1]
		return (n//cols, n%cols)

	def find_empty_cells(self, k=1):
		flat_map = self.grid.flatten()
		flat_map = (flat_map == 0)
		empty_cells = np.arange(GRID_SIZE*GRID_SIZE)[flat_map]
		empty_cells = np.random.choice(list(empty_cells), k, replace=False)
		empty_cells = [self.inv_hash(h) for h in empty_cells]
		return empty_cells

	def check_food(self):
		'''check if food is eaten by the snake
		If eaten, create new food'''
		if self.pos[0] == self.food:
			self.ate_food = True
			self.food = self.find_empty_cells()[0]
			self.grid[self.food] = 2
		
	def check_collision(self, new_head):
		'''check if snake has collided with itself or the wall'''
		self.is_alive = True
		x, y = new_head
		if new_head in self.pos[1:]:
			self.is_alive = False
		elif x >= GRID_SIZE or x < 0:
			self.is_alive = False
		elif y >= GRID_SIZE or y < 0:
			self.is_alive = False

	def update(self):
		'''update the body of the snake and check for collision'''
		if self.is_alive:
			head = self.pos[0]
			dirn = self.dir_dict[self.direction]
			new_head = (head[0] + dirn[0],
					head[1] + dirn[1])
			
			self.check_collision(new_head)

			if self.is_alive:
				self.pos = [new_head] + self.pos
				self.grid[new_head] = 1
				if not self.ate_food:
					tail = self.pos.pop()
					self.grid[tail] = 0
				else:
					self.ate_food = False
				self.length = len(self.pos)

	def draw(self, screen):
		'''draw the snake and food on the screen'''
		screen.fill((0, 0, 0))
		x, y = self.food
		pygame.draw.rect(screen, red, (y*self.cell_width,
										x*self.cell_height,
										self.cell_width, 
										self.cell_height))
		for x, y in self.pos[1:]:
			pygame.draw.rect(screen, green, (y*self.cell_width,
											x*self.cell_height,
											self.cell_width, 
											self.cell_height))
		x, y = self.pos[0]
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
		pygame.display.set_caption("Snake 2D")
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('Arial', 30)
		self.snake = Snake()
		self.game_speed = 60
		if self.mode == 'human':
			self.game_speed = 10

		self.dead_penalty = -1000
		self.food_reward = 10
		self.move_penalty = -1

	def get_human_action(self):
		assert self.mode == 'human', "return_action() not usable without 'human' mode for gym env."
		action = self.human_action
		self.human_action = self.no_op_action
		return action

	def action(self, action):
		'''update state by taking action
		check for collisions and food
		0 -> left	1 -> straight	2 -> right'''
		if action == 0:
			self.snake.direction = (self.snake.direction + 1)%4
		elif action == 2:
			self.snake.direction = (self.snake.direction - 1)%4
		# if action == 1:	# do nothing
		self.snake.update()
		self.snake.check_food()

	def evaluate(self):
		'''compute reward of the snake'''
		reward = self.move_penalty
		if not self.snake.is_alive:
			reward += self.dead_penalty
		if self.snake.ate_food:
			reward += self.food_reward
		return reward

	def is_done(self):
		'''check for terminal condition or crash'''
		if not self.snake.is_alive or self.snake.length >= self.snake.length_limit or self.done:
			self.done = False
			return True
		return False

	def observe(self):
		'''return next state upon taking action'''
		return self.snake.grid.flatten()

	def view(self):
		'''render the state of the game on the screen'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.done = True

		self.snake.draw(self.screen)

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

		self.snake.draw(self.screen)
		pygame.display.flip()
		self.clock.tick(self.game_speed)

		return reward, done

	def close(self):
		pygame.display.quit()
		pygame.quit()