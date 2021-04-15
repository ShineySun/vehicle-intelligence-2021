# Week 4 - Motion Model & Particle Filters

---

[//]: # (Image References)
[empty-update]: ./empty-update.gif
[example]: ./example.gif
[My-result]: ./result_graph/result.gif
### Update Weights
* Select the set of landmarks that are in sensor range
* Transform landmark's coordinates from particle's to map's coordinates
* Get list of associated landmarks
* Calculate probability using gaussian_distribution(implemented in helper.py)
* Update Weight

### Resampling
* According to particle's weight, Generate random index list
* Resample new particles & Replace

### My Result
![My Particle Filter with Proper Update & Resample][My-result]

## Assignment

You will complete the implementation of a simple particle filter by writing the following two methods of `class ParticleFilter` defined in `particle_filter.py`:

* `update_weights()`: For each particle in the sample set, calculate the probability of the set of observations based on a multi-variate Gaussian distribution.
* `resample()`: Reconstruct the set of particles that capture the posterior belief distribution by drawing samples according to the weights.

To run the program (which generates a 2D plot), execute the following command:

```
$ python run.py
```

Without any modification to the code, you will see a resulting plot like the one below:

![Particle Filter without Proper Update & Resample][empty-update]

while a reasonable implementation of the above mentioned methods (assignments) will give you something like

![Particle Filter Example][example]

Carefully read comments in the two method bodies and write Python code that does the job.
