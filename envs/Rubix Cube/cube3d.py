import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

color_map = {
	'R': 'r',
	'O': 'orange',
	'B': 'b',
	'G': 'g',
	'W': 'w',
	'Y': 'y',
}

faces = np.array([ [[0,3,3],[3,3,3],[0,0,3],[3,0,3]],		#top
				   [[0,0,0],[3,0,0],[0,3,0],[3,3,0]],		#bottom
				   [[0,3,3],[0,0,3],[0,3,0],[0,0,0]],		#left
				   [[3,0,3],[3,3,3],[3,0,0],[3,3,0]],		#right
				   [[0,0,3],[3,0,3],[0,0,0],[3,0,0]],		#front
				   [[3,3,3],[0,3,3],[3,3,0],[0,3,0]] ])	    #back

def plotting(xyz,color, ax):
	
	X, Y, Z = xyz
	
	X = X.reshape((2,2))
	Y = Y.reshape((2,2))
	Z = Z.reshape((2,2))

	ax.plot_surface(X,Y,Z,color=color_map[color],shade=False)

def divide(face,colors, ax):

	face_t = face.T

	offset = np.array([[0,0],[0,1],[1,0],[1,1]])

	tmp = np.unique(face_t[0])
	# print(tmp)
	if (np.unique(face_t[0]).size == 1):		#left and right
		X = face_t[0]
		y = np.linspace(face[0][1],face[1][1],4)
		z = np.linspace(face[0][2],face[2][2],4)
		# y = z = np.arange(0,3,1)
		Y, Z = np.meshgrid(y,z)
		X = np.ones((2,2)) * np.unique(X)

		# print('yz', Y, Z)
		for i in range(3):
			for j in range(3):
				pts = offset+np.array([i, j])
				piece_y =  np.array([Y[pt[0], pt[1]] for pt in pts]).reshape((2, 2))
				piece_z =  np.array([Z[pt[0], pt[1]] for pt in pts]).reshape((2, 2))

				# print(i, j, X, piece_y, piece_z)
				# print(pts)
				plotting((X, piece_y, piece_z), colors[i][j], ax)

	elif (np.unique(face_t[1]).size == 1):		#front back
		Y = face_t[1]
		x = np.linspace(face[0][0],face[1][0],4)
		z = np.linspace(face[0][2],face[2][2],4)
		# y = z = np.arange(0,3,1)
		X, Z = np.meshgrid(x,z)
		Y = np.ones((2,2)) * np.unique(Y)

		# print('yz', X, Z)
		for i in range(3):
			for j in range(3):
				pts = offset+np.array([i, j])
				piece_x =  np.array([X[pt[0], pt[1]] for pt in pts]).reshape((2, 2))
				piece_z =  np.array([Z[pt[0], pt[1]] for pt in pts]).reshape((2, 2))

				# print(i, j, Y, piece_x, piece_z)
				# print(pts)
				plotting((piece_x, Y, piece_z), colors[i][j], ax)

	elif (np.unique(face_t[2]).size == 1):		#top bottom
		Z = face_t[2]
		x = np.linspace(face[0][0],face[1][0],4)
		y = np.linspace(face[0][1],face[2][1],4)
		# y = z = np.arange(0,3,1)
		X, Y = np.meshgrid(x, y)
		Z = np.ones((2,2)) * np.unique(Z)

		# print('yz', Y, Z)
		for i in range(3):
			for j in range(3):
				pts = offset+np.array([i, j])
				piece_x =  np.array([X[pt[0], pt[1]] for pt in pts]).reshape((2, 2))
				piece_y =  np.array([Y[pt[0], pt[1]] for pt in pts]).reshape((2, 2))

				# print(i, j, X, piece_y, piece_z)
				# print(pts)
				plotting((piece_x, piece_y, Z), colors[i][j], ax)

def cube_3d(colors):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	for i in range(faces.shape[0]):
		divide(faces[i], colors[i], ax)

	plt.show()


if __name__ == "__main__":
					   
	colors = np.tile(np.array(['R', 'O', 'B', 'G', 'W', 'Y']).reshape(-1, 1, 1), [1, 3, 3])

	cube_3d(colors)