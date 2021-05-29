import gym
env = gym.make("CartPole-v0")

class Agent:
	def __init__(self):
		pass
	def get_action(self, obs):
		if obs

env.reset()
for i_episode in range(10):
	obs = env.reset()
	for t in range(100):
		env.render()
		print(obs)
		action = env.action_space.sample()
		obs, reward, done, info = env.step(action)
		# if done:
		# 	print("Episode finished after {} timesteps".format(t+1))
		# 	break

env.close()