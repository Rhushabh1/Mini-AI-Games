import gym
from custom_env import CustomEnv
import random
import argparse

def play_agent(env, max_episodes, max_try):
	total_scores = []

	for i_episode in range(max_episodes):
		state = env.reset()
		score = 0
		for t in range(max_try):
			action = env.action_space.sample()
			next_state, reward, done, info = env.step(action)
			score += reward
			env.render()
			if done:
				break

		total_scores.append(score)
		print("Episode:{}\tReward:{}".format(i_episode+1, score))
	return total_scores

def play_human(env, max_episodes, max_try):
	total_scores = []

	for i_episode in range(max_episodes):
		env.reset()
		score, done, info = env.play(max_try)
		total_scores.append(score)
		print("Episode:{}\tReward:{}".format(i_episode+1, score))
	return total_scores

if __name__ == "__main__":
	MAX_EPISODES = 30
	MAX_TRY = 10000

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--mode', metavar='M', type=str, default='bot', help='Enter Game mode ["bot", "human"]')
	args = parser.parse_args()
	print(args.mode)

	env = CustomEnv(args.mode)
	if args.mode == 'human':
		total_scores = play_human(env, MAX_EPISODES, MAX_TRY)
	else:
		total_scores = play_agent(env, MAX_EPISODES, MAX_TRY)
	avg_score = sum(total_scores)/len(total_scores)
	print("Average Scores:{:.2f}".format(avg_score))
	env.close()
