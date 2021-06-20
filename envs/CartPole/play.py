import gym
env_name = "CartPole-v0"
env_name = "Ant-v2"
env = gym.make(env_name)

class Agent:
	def __init__(self, env):
		self.action_space = env.action_space
	def get_action(self, obs):
		return self.action_space.sample()

env.reset()
agent = Agent(env)

for i_episode in range(10):
	state = env.reset()
	for t in range(100):
		env.render()
		action = agent.get_action(state)
		next_state, reward, done, info = env.step(action)
		if done:
			print("Episode finished after {} timesteps".format(t+1))
			break

env.close()