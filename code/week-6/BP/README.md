# Week 6 - Prediction & Behaviour Planning

---
### Week 6
#### Behaviour Planning
```python
def choose_next_state(self, predictions):
	# M2021077 Sunpil Kim
			# Get possible successor states
			states = self.successor_states()

			# Init best cost
			best_cost = 9999
			best_trajectory = None

			for idx in range(len(states)):
					trajectory = self.generate_trajectory(states[idx], predictions)
					cost = calculate_cost(self, trajectory, predictions)

					if cost < best_cost:
							best_cost = cost
							best_trajectory = trajectory

			# Note that the return value is a trajectory, where a trajectory
			# is a list of Vehicle objects with two elements.
			return best_trajectory
```
---
1. `choose_next_state` 는 `predictions` 와 `states` 를 이용하여 후보 `trajectory`를 생성한뒤, 최적의 `cost`를 구한다.
2. 이때 `states`는 `successor_states()`를 이용하여 다음 상태 `states`를 구하게 된다.
---

```python
def goal_distance_cost(vehicle, trajectory, predictions, data):
    '''
    Cost increases based on distance of intended lane (for planning a
    lane change) and final lane of a trajectory.
    Cost of being out of goal lane also becomes larger as vehicle approaches
    the goal distance.
    '''

    # M2021077 Sunpil Kim
    dist = abs(data.end_distance_to_goal)

    if dist > 0:
        delta_d = 2.0*vehicle.goal_lane - data.intended_lane - data.final_lane

        cost = 1 - 2*exp(-(abs(delta_d)/dist))
    else:
        cost = 1

    return cost
```
---
1. `goal_distance_cost()` 는 차량이 목표거리에 가까워 질수록 목표하는 차선을 벗어날 시 생기는 비용이 커지는 특성을 가지는 function 으로 설계하였다.
---

```python
def inefficiency_cost(vehicle, trajectory, predictions, data):
    '''
    Cost becomes higher for trajectories with intended lane and final lane
    that have slower traffic.
    '''
    # M2021077 Sunpil Kim
    vel_intended = velocity(predictions, data.intended_lane)

    # Find None exception
    if vel_intended is None : vel_intended = vehicle.target_speed

    vel_final = velocity(predictions, data.final_lane)
    # Find None exception
    if vel_final is None : vel_final = vehicle.target_speed

    cost = (2.0*vehicle.target_speed - vel_intended - vel_final) / vehicle.target_speed

    return cost
```
---
1. `inefficiency_cost()` 는 intended lane 과 속도가 느린 target lane에 있는 경우 cost가 증가하게 설계되었다.
---

---
### Result
---
1. Case 1 : Success
```python
REACH_GOAL = 0.9
EFFICIENCY = 0.1
```
```
+Meters ======================+ step: 33
      |     |     | 013 |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     | 014 |     |
      |     |     |     |     |
      |     |     |     |     |
300 - | -G- |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     | 015 |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      | *** |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     | 016 |
      |     |     |     |     |
      |     |     |     | 017 |
      |     |     |     |     |
      |     |     |     | 018 |
320 - |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     | 019 |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |

You got to the goal in 33 seconds!
```
---
2. Case 2 : Success
```python
REACH_GOAL = 0.8
EFFICIENCY = 0.2
```
```
+Meters ======================+ step: 34
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     | 013 |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
300 - | -G- |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     | 014 |     |
      |     |     |     |     |
      | *** |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     | 015 |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
320 - |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     | 016 |
      |     |     |     |     |
      |     |     |     | 017 |

You got to the goal in 34 seconds!
```
---
3. Case 3 : Fail
```python
REACH_GOAL = 0.7
EFFICIENCY = 0.3
```
```
+Meters ======================+ step: 34
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     | 013 |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
300 - | -G- |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     | *** |     |     |
      |     |     |     |     |
      |     |     | 014 |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     | 015 |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |
320 - |     |     |     |     |
      |     |     |     |     |
      |     |     |     |     |

You missed the goal. You are in lane 1 instead of 0.
```
---
## Assignment #2

Under the directory [./BP](./BP), you are given four Python modules:

* `simulate_behavior.py`: the main module you run. It instantiates a simple text-based simulation environment and runs it using the configuration specified in the same module.
* `road.py`: `class Road` is implemented here. It captures the state of the simulated road with a number of vehicles (including the ego) running on it, and visualizes it using terminal output.
* `vehicle.py`: `class Vehicle` implements the states of a vehicle and its transition, along with the vehicle's dynamics based on a simple kinematic assumption. Note that a vehicle's trajectory is represented by two instances of object of this class, where the first one gives the current state and the second one predicts the state that the vehicle is going to be in after one timestep.
* `cost_functions.py`: implementation of cost functions governing the state transition of the ego vehicle. The main job required for your assignment is to provide an adequate combination of cost functions by implementing them in this module.

### Task 1

Implement the method `choose_next_state()` in `vehicle.py`. It should

* determine which state transitions are possible from the current state (`successor_states()` function in the same module will be helpful),
* calculate cost for each state transition using the trajectory generated for each behaviour, and
* select the minimum cost trajectory and return it.

Note that you must return a planned trajectory (as described above) instead of the state that the vehicle is going to be in.

### Task 2

In `cost_functions.py`, templates for two different cost functions (`goal_distance_cost()` and `inefficiency_cost()`) are given. They are intended to capture the cost of the trajectory in terms of

* the lateral distance of the vehicle's lane selection from the goal position, and
* the time expected to be taken to reach the goal (because of different lane speeds),

respectively.

Note that the range of cost functions should be carefully defined so that they can be combined by a weighted sum, which is done in the function `calculate_cost()` (to be used in `choose_next_state()` as described above). In computing the weighted sum, a set of weights are used. For example, `REACH_GOAL` and `EFFICIENCY` are already defined (but initialized to zero values). You are going to find out a good combination of weights by an empirical manner.

You are highly encouraged to experiment with your own additional cost functions. In implementing cost functions, a trajectory's summary (defined in `TrajectoryData` and given by `get_helper_data()`) can be useful.

You are also invited to experiment with a number of different simulation settings, especially in terms of

* number of lanes
* lane speed settings (all non-ego vehicles follow these)
* traffic density (governing the number of non-ego vehicles)

and so on.

Remember that our state machine should be geared towards reaching the goal in an *efficient* manner. Try to compare a behaviour that switches to the goal lane as soon as possible (note that the goal position is in the slowest lane in the given setting) and one that follows a faster lane and move to the goal lane as the remaining distance decreases. Observe different behaviour taken by the ego vehicle when different weights are given to different cost functions, and also when other cost metrics (additional cost functions) are used.
