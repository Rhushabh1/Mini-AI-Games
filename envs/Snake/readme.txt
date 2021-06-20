=======================Title=======================

Snake game Custom environment in Python using OpenAI Gym

=================Short Description=================

Snake-gym is a custom environment of the classic snake game using OpenAI Gym. It is meant to test different Reinforcement Learning Agents. It has a "human" mode to serve as a Single Player game.

=================Long Description==================

Installation:
$> pip install -r requirements.txt

How to run:
$> python3 main.py [--mode <mode>] [--episodes <num_episodes>]

where mode = "bot" / "human" [default = "bot"],
num_episodes = number of games to simulate [default = 30]

Controller Functions:	
reset(): reset env to start state
step(action): return next-state and reward based on action
render(): render env on screen
play(max_moves): simulate a game with maximum moves = max_moves
close(): quit the env

Rewards and Penalties:
-1000 if snake dies
+10 if snake ate food
-1 if snake moves 1 block

Game Details:
A sample Agent class is defined to demonstrate the Agent-Env interaction.

Average Scores of all the games played is displayed at the end.

The grid dimensions are 20x20.

Snake is allowed to move in 3 directions w.r.t. its body orientation:
LEFT (left arrow key), STRAIGHT (up arrow key), RIGHT (right arrow key)

The state of the env is modelled as a complete 20x20 grid with the following notation:
0 -> empty cell
1 -> snake head + body
2 -> food

Game terminates when the snake hits his head on the wall or tries to eat itself.