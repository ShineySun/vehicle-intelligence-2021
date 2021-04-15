# Week 2 - Markov Localization

---
### Motion Model
* Calculate the probability for all possible prior positions
* Calculate the motion model probability using the belief prior state
* Return total probability

### Observation Model
* Exception Check : check a pseudo range vector existence using observations
* Calculate the observation model probability using helper.norm_pdf function
* Return total probability

### My Result Graph
[//]: # (Image References)
[plot]: .result_graph/result.gif

## Assignment

You will complete the implementation of a simple Markov localizer by writing the following two functions in `markov_localizer.py`:

* `motion_model()`: For each possible prior positions, calculate the probability that the vehicle will move to the position specified by `position` given as input.
* `observation_model()`: Given the `observations`, calculate the probability of this measurement being observed using `pseudo_ranges`.

The algorithm is presented and explained in class.

All the other source files (`main.py` and `helper.py`) should be left as they are.

If you correctly implement the above functions, you expect to see a plot similar to the following:

![Expected Result of Markov Localization][plot]

If you run the program (`main.py`) without any modification to the code, it will generate only the frame of the above plot because all probabilities returned by `motion_model()` are zero by default.
