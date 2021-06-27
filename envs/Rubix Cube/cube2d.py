import pygame
import random
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 20
red = (255, 0, 0)
orange = (255, 153, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
colors = {'R':red, 'O':orange, 'B':blue, 'G':green, 'W':white, 'Y':yellow}


class Cube:
	def __init__(self):
		'''Initialise the Rubik's cube
		Has 6 faces
		0 -> red
		1 -> orange
		2 -> blue
		3 -> green
		4 -> white
		5 -> yellow
		'''
		self.corner_color = ['RBW', 'RBY', 'RGY', 'RGW', 
							'OBW', 'OBY', 'OGY', 'OGW']
		self.edge_color = ['RW', 'RB', 'RY', 'RG', 
						   'BW', 'BY', 'GY', 'GW', 
						   'OW', 'OB', 'OY', 'OG']

		# [id(corner/edge), orient_offset]
		'''
		CORNERS: offset is wrt good corners, (-ve) for bad corners
		EDGES: offset if wrt 0 orient edges, flip for 1 orient edges
		'''
		self.array_to_cube = [#		||			||		cases for U/D edge faces
			[ [[1,0],[2,0],[2,0]], [[1,0],[],[3 ,0]], [[0,0],[0 ,0],[3,0]] ],		# red
			[ [[4,0],[8,0],[7,0]], [[9,0],[],[11,0]], [[5,0],[10,0],[6,0]] ],		# orange
			[ [[1,2],[1,1],[0,1]], [[5,1],[],[4 ,1]], [[5,1],[9 ,1],[4,2]] ],		# blue
			[ [[3,2],[3,1],[2,1]], [[7,1],[],[6 ,1]], [[7,1],[11,1],[6,2]] ],		# green
			[ [[0,2],[0,1],[3,1]], [[4,0],[],[7 ,0]], [[4,1],[8 ,1],[7,2]] ],		# white
			[ [[2,2],[2,1],[1,1]], [[6,0],[],[5 ,0]], [[6,1],[10,1],[5,2]] ],		# yellow
		]

		self.cube = np.tile(np.array(['R', 'O', 'B', 'G', 'W', 'Y']).reshape(-1, 1, 1), [1, 3, 3])
		self.corners = np.arange(8)
		self.edges = np.arange(12)
		self.corners_orient = np.zeros(8).astype(int)
		self.edges_orient = np.zeros(12).astype(int)

		self.corner_face_dict = {
			'F': [0, 3, 7, 4], 
			'B': [2, 1, 5, 6],
			'U': [1, 2, 3, 0],
			'D': [4, 7, 6, 5],
			'L': [1, 0, 4, 5],
			'R': [3, 2, 6, 7],
		}
		self.edge_face_dict = {
			'F': [0, 7, 8, 4], 
			'B': [2, 5, 10, 6],
			'U': [2, 3, 0, 1],
			'D': [8, 11, 10, 9],
			'L': [1, 4, 9, 5],
			'R': [3, 6, 11, 7],
		}

		self.moves = {
			0: ['F'], 6: ['F']*2, 12: ['F']*3,
			1: ['B'], 7: ['B']*2, 13: ['B']*3,
			2: ['U'], 8: ['U']*2, 14: ['U']*3,
			3: ['D'], 9: ['D']*2, 15: ['D']*3,
			4: ['L'], 10: ['L']*2, 16: ['L']*3,
			5: ['R'], 11: ['R']*2, 17: ['R']*3,
		}

		self.good_corners = [0, 2, 5, 7]				# R/O, B/G, W/Y
		self.even_corners = np.array([0, 1, 0, 1])		# R/O, W/Y, B/G

		self.is_solved = True
		self.action_called = False
		self.has_moved = False
		self.side = int( min(SCREEN_WIDTH, SCREEN_HEIGHT) / (3*3) )

		self.scramble_cube()


	def scramble_cube(self):
		# scramble the cube for the player to solve
		self.is_solved = False

	def corners_edges_to_cube(self):
		# print(self.corners, self.corners_orient, self.edges, self.edges_orient)
		for idx, face in enumerate(self.array_to_cube):
			for i in range(len(face)):
				for j in range(len(face[0])):
					if (i in [0, 2]) and (j in [0, 2]):
						# its a corner
						pos, offset = face[i][j]
						corner_id = self.corners[pos]
						orient = self.corners_orient[pos]
						color = self.corner_color[corner_id]
						if corner_id in self.good_corners:
							self.cube[idx, i, j] = color[(orient+offset)%3]
						else:
							self.cube[idx, i, j] = color[(orient-offset)%3]

					elif i==1 and j==1:
						# its a center (do nothing)
						continue
					else:
						# its an edge
						pos, face_offset = face[i][j]
						edge_id = self.edges[pos]
						orient = self.edges_orient[pos]
						color = self.edge_color[edge_id]
						if ('B' in color) or ('G' in color):
							try:
								bad_i = color.index('B')
							except:
								bad_i = color.index('G')
						else:
							try:
								bad_i = color.index('W')
							except:
								bad_i = color.index('Y')
							# bad_i = (bad_i + (idx>1 and i==1))%2 		# +1 if F/B face

						self.cube[idx, i, j] = color[(bad_i+(1-orient)+face_offset)%2]


	def move(self, action_list):
		'''move faces according the action
		Corners:
			(C) clockwise = 0->1->2->...
			(A) anit-clockwise = 2->1->0->...
			(G) good corners 		= 	[0, 0, 1, 1]
			(E) even pos or corners = 	[0, 1, 0, 1] constant for a face
			Clock or Anti?			=	[A, C, C, A] XOR op

		Edges:
			flip only when F/B
			else don't flip
		'''
		self.action_called = True
		for action in action_list:
			corner_list = self.corner_face_dict[action]
			edge_list = self.edge_face_dict[action]

			# orientation update
			if action not in ['U', 'D']:
				good = np.array([c in self.good_corners for c in self.corners[corner_list]])
				clock = np.bitwise_xor(good, self.even_corners)
				self.corners_orient[corner_list] = ( self.corners_orient[corner_list] + (clock) + (-1)*(1 - clock) )%3

			if action in ['F', 'B']:
				self.edges_orient[edge_list] = 1 - self.edges_orient[edge_list]

			# position update
			self.corners[corner_list] = np.roll(self.corners[corner_list], 1)
			self.corners_orient[corner_list] = np.roll(self.corners_orient[corner_list], 1)
			self.edges[edge_list] = np.roll(self.edges[edge_list], 1)
			self.edges_orient[edge_list] = np.roll(self.edges_orient[edge_list], 1)

	def update(self):
		# do something
		if self.action_called:
			self.corners_edges_to_cube()
			self.is_solved = self.check_solve()
		self.has_moved = self.action_called
		self.action_called = False

	def check_solve(self):
		for face in self.cube:
			if np.unique(face).size > 1:
				return False
		return True

	def draw(self, screen):
		'''draw the Rubik's Cube on the screen'''
		screen.fill((0, 0, 0))

		for idx, face in enumerate(self.cube):
			for i in range(face.shape[0]):
				for j in range(face.shape[1]):
					x, y = idx%3, idx//3
					pygame.draw.rect(screen, 
									colors[ face[i][j] ], 
									(3*self.side*x + self.side*j, 3*self.side*y + self.side*i, self.side, self.side))


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
		pygame.display.set_caption("Rubiks Cube")
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('Arial', 30)
		self.rubiks = Cube()
		self.game_speed = 10
		if self.mode == 'human':
			self.game_speed = 60

		self.finish_reward = 1000
		self.move_penalty = -1

	def get_human_action(self):
		assert self.mode == 'human', "return_action() not usable without 'human' mode for gym env."
		action = self.human_action
		self.human_action = self.no_op_action 		# no input action
		return action

	def action(self, action):
		'''update state by taking action
		-1 -> stop at position (do nothing)
		0 -> ...
		'''
		if action != -1:
			action_list = self.rubiks.moves[action]
			self.rubiks.move(action_list)
		self.rubiks.update()		

	def evaluate(self):
		'''compute reward of the player'''
		reward = 0
		if self.rubiks.has_moved:
			reward += self.move_penalty
		if self.rubiks.is_solved:
			reward += self.finish_reward
		return reward

	def is_done(self):
		'''check for terminal condition (is_solved)'''
		if self.rubiks.is_solved or self.done:
			self.done = False
			return True
		return False

	def observe(self):
		'''return next state upon taking action'''
		return self.rubiks.cube.flatten()

	def view(self):
		'''render the state of the game on the screen'''
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.done = True

		self.rubiks.draw(self.screen)

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
					elif event.key == pygame.K_f:
						self.human_action = 0
					elif event.key == pygame.K_b:
						self.human_action = 1
					elif event.key == pygame.K_u:
						self.human_action = 2
					elif event.key == pygame.K_d:
						self.human_action = 3
					elif event.key == pygame.K_l:
						self.human_action = 4
					elif event.key == pygame.K_r:
						self.human_action = 5

		action = self.get_human_action()
		self.action(action)
		reward = self.evaluate()
		done = self.is_done()

		self.rubiks.draw(self.screen)
		pygame.display.flip()
		self.clock.tick(self.game_speed)

		return reward, done

	def close(self):
		pygame.display.quit()
		pygame.quit()
