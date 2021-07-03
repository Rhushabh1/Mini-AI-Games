import pygame
import random
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
red = (255, 0, 0)
orange = (255, 153, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
colors = {'R':red, 'O':orange, 'B':blue, 'G':green, 'W':white, 'Y':yellow}


class Cube:
	def __init__(self, level=200):
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
			# clockwise (F, B, U, D, L, R)
			0: ['F'], 1: ['B'], 2: ['U'], 3: ['D'], 4: ['L'], 5: ['R'],
			# double (F2, B2, U2, D2, L2, R2)
			6: ['F']*2, 7: ['B']*2, 8: ['U']*2, 9: ['D']*2, 10: ['L']*2, 11: ['R']*2, 
			# anti-clockwise (F', B', U', D', L', R')
			12: ['F']*3, 13: ['B']*3, 14: ['U']*3, 15: ['D']*3, 16: ['L']*3, 17: ['R']*3,
			# slice rotations (M, E, S)
			18: ['R','L','L','L'], 19: ['U','D','D','D'], 20: ['B','F','F','F'],
			# reverse slice rotations (M', E', S')
			21: ['L','R','R','R'], 22: ['D','U','U','U'], 23: ['F','B','B','B'],
		}

		self.good_corners = [0, 2, 5, 7]				# good -> (R/O)(B/G)(W/Y), bad -> (R/O)(W/Y)(B/G)
		self.even_corners = np.array([0, 1, 0, 1])	
		'''
		0---1
			|
		1---0
		'''	

		self.level = level
		self.is_solved = True
		self.action_called = False
		self.has_moved = False
		self.side = int( min(SCREEN_WIDTH, SCREEN_HEIGHT) / (3*3) )

		self.scramble_cube()


	def scramble_cube(self):
		# scramble the cube for the player to solve
		seq = []
		# max(5, 8) = 8
		# choice([0, 1, 2, ,,,,23], 8, replace=True) -> moves = [5, 2, 9, 19, 6, 5, 3, 1] => [R, U, D, D, U, D, D, D, ] = SEQ
		moves = np.random.choice(24, max(5, random.randrange(self.level)), replace=True)
		for move in moves:
			seq.extend(self.moves[move])
		self.move(seq)
		print("Scramble: {}".format(seq))
		self.is_solved = False

	def move(self, action_list):
		# [R, U, D, D, U, D, D, D, ] 
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
					# [0, 1, 2]
					# [3, 4, 5]
					pygame.draw.rect(screen, 
									colors[ face[i][j] ], 
									(3*self.side*x + self.side*j, 3*self.side*y + self.side*i, self.side, self.side))


class Pygame2D:
	def __init__(self, mode='bot', level=200):
		'''Initialise pygame and display attributes'''
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
		self.rubiks = Cube(level)
		self.game_speed = 10
		if self.mode == 'human':
			self.game_speed = 60

		self.finish_reward = 1000
		self.move_penalty = -1

		self.description = "\
			\n========KEY-MAP=========\
			\nF 		: move F\
			\nB 		: move B\
			\nU 		: move U\
			\nD 		: move D\
			\nL 		: move L\
			\nR 		: move R\
			\nCtrl + F 	: move F2\
			\nCtrl + B 	: move B2\
			\nCtrl + U 	: move U2\
			\nCtrl + D 	: move D2\
			\nCtrl + L 	: move L2\
			\nCtrl + R 	: move R2\
			\nShift + F 	: move F\'\
			\nShift + B 	: move B\'\
			\nShift + U 	: move U\'\
			\nShift + D 	: move D\'\
			\nShift + L 	: move L\'\
			\nShift + R 	: move R\'\
			\nM 		: move M\
			\nE 		: move E\
			\nS 		: move S\
			\nShift + M 	: move M\'\
			\nShift + E 	: move E\'\
			\nShift + S 	: move S\'\
			\n========================"

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
		state = self.rubiks.cube.flatten()
		state[state=='R'] = 0
		state[state=='O'] = 1
		state[state=='B'] = 2
		state[state=='G'] = 3
		state[state=='W'] = 4
		state[state=='Y'] = 5
		return state.astype(int)

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
		'''
		clockwise -> F
		double 	-> CTRL + F
		anti-clockwise	-> SHIFT + F
		slice rotations	-> M
		reverse slice rotations	-> SHIFT + M
		'''

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
					self.done = True
				if self.mode == 'human':

					mods = pygame.key.get_mods()

					if event.key == pygame.K_RETURN:
						self.done = True

					elif event.key == pygame.K_f:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 12
						elif mods & pygame.KMOD_CTRL:
							self.human_action = 6
						else:
							self.human_action = 0

					elif event.key == pygame.K_b:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 13
						elif mods & pygame.KMOD_CTRL:
							self.human_action = 7
						else:
							self.human_action = 1

					elif event.key == pygame.K_u:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 14
						elif mods & pygame.KMOD_CTRL:
							self.human_action = 8
						else:
							self.human_action = 2

					elif event.key == pygame.K_d:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 15
						elif mods & pygame.KMOD_CTRL:
							self.human_action = 9
						else:
							self.human_action = 3

					elif event.key == pygame.K_l:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 16
						elif mods & pygame.KMOD_CTRL:
							self.human_action = 10
						else:
							self.human_action = 4

					elif event.key == pygame.K_r:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 17
						elif mods & pygame.KMOD_CTRL:
							self.human_action = 11
						else:
							self.human_action = 5

					elif event.key == pygame.K_m:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 21
						else:
							self.human_action = 18

					elif event.key == pygame.K_e:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 22
						else:
							self.human_action = 19

					elif event.key == pygame.K_s:
						if mods & pygame.KMOD_SHIFT:
							self.human_action = 23
						else:
							self.human_action = 20

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
