# Week 6 - Prediction & Behaviour Planning

---
### Week 6
#### Gaussian Naive Bayes
```python
def train(self, X, Y):
			'''
			Collect the data and calculate mean and standard variation
			for each class. Record them for later use in prediction.
			'''
			# TODO: implement code.
			# M2021077 Sunpil Kim


			### Collect the data ###
			values_by_label = dict()

			# INPUT FORMAT [ s, d, s_dot, d_dot ]
			# for x,y in zip(X,Y):
			#     print(x)
			#     print(y)

			for c in self.classes:
					values_by_label[c] = np.empty((4,0))
			# Collect the data
			# Dict ==> { class : [s : ], [d%4 : ], [s_dot : ], [d_dot : ]}
			for x,y in zip(X,Y):
					# item [s, d%4, s_dot, d_dot]
					item = np.array([[x[0]], [(x[1] % 4)], [x[2]], [x[3]]])
					# concat the array for get mean, stddevs
					values_by_label[y] = np.append(values_by_label[y], item, axis=1)

			#print(values_by_label)

			### Caculate mean and stddevs for each classes ###
			means = dict()
			stddevs = dict()

			for c in self.classes:
					class_array = np.array(values_by_label[c])
					# get mean
					means[c] = np.mean(class_array, axis=1)
					# get stddevs
					stddevs[c] = np.std(class_array, axis=1)

			self.means = means
			self.stddevs = stddevs

```
---
1. train 함수는 `self.classes` 의 각 class에 포함되는 데이터의 평균과 분산을 구하는 역할을 한다.
2. `np.append()` 함수를 사용하여 class에 맞는 데이터를 한 배열에 저장함으로써 평균과 분산을 쉽게 구할 수 있게 작업하였다.
---

```python
def predict(self, observation):
			'''
			Calculate Gaussian probability for each variable based on the
			mean and standard deviation calculated in the training process.
			Multiply all the probabilities for variables, and then
			normalize them to get conditional probabilities.
			Return the label for the highest conditional probability.
			'''
			# TODO: implement code.
			# M2021077 Sunpil Kim

			# Calculate Gaussian probability for each variable
			probs = dict()

			for c in self.classes:
					cur_prob = 1.00
					# Multiply all the probabilities for variables
					for idx in range(len(observation)):
							cur_prob *= gaussian_prob(observation[idx], self.means[c][idx], self.stddevs[c][idx])

					probs[c] = cur_prob

			# Get hightest conditinal probability & label
			highest_prob = 0
			highest_class = "keep"

			for c in self.classes:
					if probs[c] > highest_prob:
							highest_prob = probs[c]
							highest_class = c

			return highest_class

```
---
1. prediction 함수는 각 `self.classes`에 해당하는 observation의 확률을 `gaussian_prob()` 함수를 이용하여 계산한다.
2. `probs` 에 있는 값 중 가장 큰 class 를 추출하여 prediction을 진행한다.
---

---
### Result
---
```
You got 83.60 percent correct
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
