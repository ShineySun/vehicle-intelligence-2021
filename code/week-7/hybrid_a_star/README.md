# Week 7 - Hybrid A* Algorithm & Trajectory Generation

---
### Week 7
#### Hybrid A* Algorithm
---
```python
def expand(self, current, goal):
    g = current['g']
    x, y, theta = current['x'], current['y'], current['t']

    # The g value of a newly expanded cell increases by 1 from the
    # previously expanded cell.
    g2 = g + 1
    next_states = []

    # Consider a discrete selection of steering angles.
    # M2021077 Sunpil Kim
    for delta_t in range(self.omega_min, self.omega_max+1, self.omega_step):
        # TODO: implement the trajectory generation based on
        # a simple bicycle model.
        # Let theta2 be the vehicle's heading (in radian)
        # between 0 and 2 * PI.
        # Check validity and then add to the next_states list.

        delta = np.pi / 180.0 * delta_t
        # Bicycle Model
        omega = self.speed / self.length * np.tan(delta)
        # Vehicle's Heading
        theta2 = theta + omega
        # theta2 [0 ~ 2*PI]
        if theta2 < 0:
            theta2 += 2*np.pi
        elif theta2 > 2*np.pi:
            theta2 -= 2*np.pi

        # Get Post position
        post_x = x + self.speed*np.cos(theta)
        post_y = y + self.speed*np.sin(theta)

        # CHECK VALIDITY
        if 0 <= self.idx(post_x) and self.idx(post_x) < self.dim[1] and 0 <= self.idx(post_y) and self.idx(post_y) < self.dim[2]:
            post_f = g2 + self.heuristic(post_x, post_y, goal)
            # Add to the next states list
            post_state = {
                'f': post_f,
                'g': g2,
                'x': post_x,
                'y': post_y,
                't': theta2,
            }
            next_states.append(post_state)

    return next_states
```
---
1. `expand()` 는 현재 상태에서 가능한 다음 state set을 반환한다.
2. `Bicycle Model`을 사용하며, [-35,35, step] 의 각도를 이용하여 탐색 범위를 지정하며, 다음 state의 position과 heading(yaw)를 계산한다.
---
```python
def search(self, grid, start, goal):
    # Initial heading of the vehicle is given in the
    # last component of the tuple start.
    theta = start[-1]
    # Determine the cell to contain the initial state, as well as
    # the state itself.
    stack = self.theta_to_stack_num(theta)
    g = 0
    s = {
        'f': self.heuristic(start[0], start[1], goal),
        'g': g,
        'x': start[0],
        'y': start[1],
        't': theta,
    }
    self.final = s
    # Close the initial cell and record the starting state for
    # the sake of path reconstruction.
    self.closed[stack][self.idx(s['x'])][self.idx(s['y'])] = 1
    self.came_from[stack][self.idx(s['x'])][self.idx(s['y'])] = s
    total_closed = 1
    opened = [s]
    # Examine the open list, according to the order dictated by
    # the heuristic function.
    while len(opened) > 0:
        # TODO: implement prioritized breadth-first search
        # for the hybrid A* algorithm.
        opened.sort(key=lambda s : s['f'], reverse=True)
        curr = opened.pop()
        x, y = curr['x'], curr['y']
        if (self.idx(x), self.idx(y)) == goal:
            self.final = curr
            found = True
            break

        # Compute reachable new states and process each of them.
        next_states = self.expand(curr, goal)
        for n in next_states:
            idx_x, idx_y = self.idx(n['x']), self.idx(n['y'])
            stack2 = self.theta_to_stack_num(n['t'])

            if grid[idx_x][idx_y] == 0:
                # Distance from Obstacle
                dist_x = abs(self.idx(x) - idx_x)
                dist_y = abs(self.idx(y)- idx_y)
                # Min Distance
                min_x = min(self.idx(x), idx_x)
                min_y = min(self.idx(y), idx_y)

                flag = True

                for d_x in range(dist_x+1):
                    for d_y in range(dist_y+1):
                        if grid[min_x + d_x][min_y + d_y] != 0:
                            flag = False

                if flag and self.closed[stack2][idx_x][idx_y] == 0:
                    self.closed[stack2][idx_x][idx_y] = 1
                    total_closed += 1
                    self.came_from[stack2][idx_x][idx_y] = curr
                    opened.append(n)

    else:
        # We weren't able to find a valid path; this does not necessarily
        # mean there is no feasible trajectory to reach the goal.
        # In other words, the hybrid A* algorithm is not complete.
        found = False

    return found, total_closed
```
---
1. `search()` 는 `BFS` 를 이용한 다음 경로를 추적한다.
2. `expand()` 를 이용하여 구한 `next_states` 정보를 토대로, `grid map` 상의 갈 수 있는 경로를 확인하여 최적의 경로를 생성한다.
---
```python
def theta_to_stack_num(self, theta):
      # TODO: implement a function that calculate the stack number
      # given theta represented in radian. Note that the calculation
      # should partition 360 degrees (2 * PI rad) into different
      # cells whose number is given by NUM_THETA_CELLS.

      # Radian to Degree
      deg = theta * 180 / np.pi
      interval = 360 / self.NUM_THETA_CELLS
      stack_num = deg // interval
      # Exception Occur
      if stack_num == self.NUM_THETA_CELLS:
          stack_num = 0

      return int(stack_num)
```
---
1. `theta_to_stack_num()` 는 파라미터 `theta` 의 해당 stack을 반환한다. 이때 theta 는 `expand()` 에서 계산된 radian 값이 입력으로 들어오므로 degree 변환을 해줘야 에러 없이 동작한다.
---
```python
def heuristic(self, x, y, goal):
      # TODO: implement a heuristic function.
      # L2 DISTANCE
      l2_dist = np.sqrt((goal[0]-x)*(goal[0]-x) + (goal[1]-y)*(goal[1]-y))
      return l2_dist
```
---
1. `heuristic()` 은 `L2 Distance`를 이용하여 설계하였다.
---

---
### Result
---
1. Case 1 - Success
```python
NUM_THETA_CELLS = 360
speed = 1.0
length = 0.5
```
![Result Case 1][result_case_1]
---
2. Case 2 - Semi Success
```python
NUM_THETA_CELLS = 180
speed = 1.0
length = 0.5
```
![Result Case 2][result_case_2]
---
3. Case 1 - Fail
```python
NUM_THETA_CELLS = 360
speed = 0.5
length = 0.5
```
![Result Case 3][result_case_3]
---
[//]: # (Image References)
[has-example]: ./has_example.png
[result_case_1]: ./result_case_1.png
[result_case_2]: ./result_case_2.png
[result_case_3]: ./result_case_3.png

## Assignment: Hybrid A* Algorithm

In directory [`./hybrid_a_star`](./hybrid_a_star), a simple test program for the hybrid A* algorithm is provided. Run the following command to test:

```
$ python main.py
```

The program consists of three modules:

* `main.py` defines the map, start configuration and end configuration. It instantiates a `HybridAStar` object and calls the search method to generate a motion plan.
* `hybrid_astar.py` implements the algorithm.
* `plot.py` provides an OpenCV-based visualization for the purpose of result monitoring.

You have to implement the following sections of code for the assignment:

* Trajectory generation: in the method `HybridAStar.expand()`, a simple one-point trajectory shall be generated based on a basic bicycle model. This is going to be used in expanding 3-D grid cells in the algorithm's search operation.
* Hybrid A* search algorithm: in the method `HybridAStar.search()`, after expanding the states reachable from the current configuration, the algorithm must process each state (i.e., determine the grid cell, check its validity, close the visited cell, and record the path. You will have to write code in the `for n in next_states:` loop.
* Discretization of heading: in the method `HybridAStar.theta_to_stack_num()`, you will write code to map the vehicle's orientation (theta) to a finite set of stack indices.
* Heuristic function: in the method `HybridAStar.heuristic()`, you define a heuristic function that will be used in determining the priority of grid cells to be expanded. For instance, the distance to the goal is a reasonable estimate of each cell's cost.

You are invited to tweak various parameters including the number of stacks (heading discretization granularity) and the vehicle's velocity. It will also be interesting to adjust the grid granularity of the map. The following figure illustrates an example output of the program with the default map given in `main.py` and `NUM_THETA_CELLS = 360` while the vehicle speed is set to 0.5.

![Example Output of the Hybrid A* Test Program][has-example]

---
