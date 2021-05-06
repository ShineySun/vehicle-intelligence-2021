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
## Assignment #1

Under the directory [./GNB](./GNB), you are given two Python modules:

* `prediction.py`: the main module you run. The `main()` function does two things: (1) read an input file ([`train.json`](./GNB/train.json)) and train the GNB (Gaussian Naive Bayes) classifier using the data stored in it, and (2) read another input file ([`test.json`](./GNB/test.json)) and make predictions for a number of data points. The accuracy measure is taken and displayed.
* `classifier.py`: main implementation of the GNB classifier. You shall implement two methods (`train()` and `precict()`), which are used to train the classifier and make predictions, respectively.

Both input files ([`train.json`](./GNB/train.json) and [`test.json`](./GNB/test.json)) have the same format, which is a JSON-encoded representation of training data set and test data set, respectively. The format is shown below:

```
{
	"states": [[s_1, d_1, s_dot_1, d_dot_1],
	           [s_2, d_2, s_dot_2, d_dot_2],
	           ...
	           [s_n, d_n, s_dot_n, d_dot_n]
	          ],
	"labels": [L_1, L_2, ..., L_n]
}
```

The array `"states"` have a total of `n` items, each of which gives a (hypothetically) measured state of a vehicle, where `s_i` and `d_i` denote its position in the Frenet coordinate system. In addition, `s_dot_i` and `d_dot_i` give their first derivates, respectively. For each measured state, a label is associated (given in the `"labels"` array) that represents the vehicle's behaviour. The label is one of `"keep"`, `"left"`, and `"right"`, which denote keeping the current lane, making a left turn, and making a right turn, respectively.

The training set has a total of 750 data points, whereas the test set contains 250 data points with the ground truth contained in `"labels"`.

The GNB classifier is trained by computing the mean and variance of each component in the state variable for each observed behaviour. Later it is used to predict the behaviour by computing the Gaussian probability of an observed state for each behaviour and taking the maximum. You are going to implement that functionality. For convcenience, a separate function `gaussian_prob()` is already given in the module `classifier.py`.


---
