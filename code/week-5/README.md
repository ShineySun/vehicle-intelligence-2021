# Week 5 - Path Planning & the A* Algorithm

### Week 5
#### A* Algorithm
```python
def optimum_policy_2D(grid, init, goal, cost):
		# Initialize the value function with (infeasibly) high costs.
		value = np.full((4, ) + grid.shape, 999, dtype=np.int32)
		# Initialize the policy function with negative (unused) values.
		policy = np.full((4,) + grid.shape, -1, dtype=np.int32)
		# Final path policy will be in 2D, instead of 3D.
		policy2D = np.full(grid.shape, ' ')

		# Apply dynamic programming with the flag change.
		change = True
		while change:
				change = False
				# This will provide a useful iterator for the state space.
				p = itertools.product(
						range(grid.shape[0]),
						range(grid.shape[1]),
						range(len(forward))
				)
				# Compute the value function for each state and
				# update policy function accordingly.
				for y, x, t in p:
						#print(y, ' ', x, ' ', t)
						# Mark the final state with a special value that we will
						# use in generating the final path policy.
						if (y, x) == goal and value[(t, y, x)] > 0:
								# TODO: implement code.
								# M2021077 Sunpil Kim
								value[(t,y,x)] = 0
								# Final Marker --> -444
								policy[(t,y,x)] = -444
								change = True
						# Try to use simple arithmetic to capture state transitions.
						elif grid[(y, x)] == 0:
								# TODO: implement code.
								# M2021077 Sunpil Kim
								for f_idx in range(len(forward)):
										# get post position
										x_tmp = x + forward[f_idx][1]
										y_tmp = y + forward[f_idx][0]

										# boundary check
										# Be Careful -> len_x < len(grid[0])    --> 1 hour source bug ㅡㅡ
										if x_tmp >= 0 and x_tmp < len(grid[0]) and y_tmp >= 0 and y_tmp < len(grid) and grid[y_tmp][x_tmp] == 0:
												post_tmp = value[(f_idx, y_tmp, x_tmp)]
												#print(post_tmp)

												for act_idx in range(len(action)):
														if (t + action[act_idx]) % len(forward) == f_idx:
																v_tmp = post_tmp + cost[act_idx]

																# cost coparison & change
																if v_tmp < value[(t,y,x)]:
																		value[(t,y,x)] = v_tmp
																		policy[(t,y,x)] = action[act_idx]
																		change = True

		# Now navigate through the policy table to generate a
		# sequence of actions to take to follow the optimal path.
		# TODO: implement code.

		# M2021077 Sunpil Kim

		# init position & orientation
		y = init[0]
		x = init[1]
		f = init[2]

		if policy[(f,y,x)] == -1:
				policy2D[(y,x)] = action_name[0]
		elif policy[(f,y,x)] == 0:
				policy2D[(y,x)] = action_name[1]
		elif policy[(f,y,x)] == 1:
				policy2D[(y,x)] = action_name[2]
		else:
				policy2D[(y,x)] = "*"

		# visualization
		while policy[(f,y,x)] != -444:
				if policy[(f,y,x)] == -1:
						f = (f - 1)%4
				elif policy[(f,y,x)] == 1:
						f = (f + 1)%4

				x += forward[f][1]
				y += forward[f][0]

				if policy[(f,y,x)] == -1:
						policy2D[(y,x)] = action_name[0]
				elif policy[(f,y,x)] == 0:
						policy2D[(y,x)] = action_name[1]
				elif policy[(f,y,x)] == 1:
						policy2D[(y,x)] = action_name[2]
				else:
						# final state is visualized as "*" star marker
						policy2D[(y,x)] = "*"

		# Return the optimum policy generated above.
		return policy2D
```
---

## Examples

We have four small working examples for demonstration of basic path planning algorithms:

* `search.py`: simple shortest path search algorithm based on BFS (breadth first search) - only calculating the cost.
* `path.py`: built on top of the above, generating an optimum (in terms of action steps) path plan.
* `astar.py`: basic implementation of the A* algorithm that employs a heuristic function in expanding the search.
* `policy.py`: computation of the shortest path based on a dynamic programming technique.

These sample source can be run as they are. Explanation and test results are given in the lecture notes.

## Assignment

You will complete the implementation of a simple path planning algorithm based on the dynamic programming technique demonstrated in `policy.py`. A template code is given by `assignment.py`.

The assignmemt extends `policy.py` in two aspects:

* State space: since we now consider not only the position of the vehicle but also its orientation, the state is now represented in 3D instead of 2D.
* Cost function: we define different cost for different actions. They are:
	- Turn right and move forward
	- Move forward
	- Turn left and move forward

This example is intended to illustrate the algorithm's capability of generating an alternative (detouring) path when left turns are penalized by a higher cost than the other two possible actions. When run with the settings defined in `assignment.py` without modification, a successful implementation shall generate the following output,

```
[[' ', ' ', ' ', 'R', '#', 'R'],
 [' ', ' ', ' ', '#', ' ', '#'],
 ['*', '#', '#', '#', '#', 'R'],
 [' ', ' ', ' ', '#', ' ', ' '],
 [' ', ' ', ' ', '#', ' ', ' ']]
```

because of the prohibitively high cost associated with a left turn.

You are highly encouraged to experiment with different (more complex) maps and different cost settings for each type of action.
