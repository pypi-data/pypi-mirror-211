
<img width="500" src="doc/logo/transparent_small.png">

**lazy-learn** is a high-level Python interface for automated machine learning (AutoML). While there are many AutoML libraries available each typically solves a niche area of the overall ML pipeline without providing a covering and approachable end-to-end system.

The aim of lazy-learn is exactly that. Given a dataset, lazy-learn will analyse types and distributions of attributes, preprocess, feature-engineer and ultimately train models to be used for further evaluation or inference. 

## Upcoming features

Current stable version is 0.0.3. The upcoming updates will support:
- Abstract construction of model architectures
- XGBoost, LightGBM, Adaboost and Catboost architectures
- Time partitioning of datasets (Added in 0.0.4)
- Automated Hyperparameter Optimisation (HPO) (Added in 0.0.4)
- Text features
- An interface to AutoGluon
- Outlier detection and handling
- Automated suggestions of performance metrics

## Usage

Using lazy-learn revolves around the `LazyLearner` class. You can think of it as a kind of project, and it is the wrapper for any experiment within lazy-learn. You can consider a simple example with the California Housing dataset:

```python
from lazylearn import LazyLearner
from sklearn.datasets import fetch_california_housing


# get some data
data = fetch_california_housing(as_frame=True)
df = data["data"]
df["MedHouseVal"] = data["target"]

# instantiate and run the LazyLearner
learner = LazyLearner()
learner.create_project(data=df, target="MedHouseVal")
learner.run_autopilot()

# evaluate results
print(learner.leaderboard())

```

## Installation

### Dependencies

lazy-learn requires:

- pandas
- scikit-learn
- xgboost

### User Installation 
```
pip install lazy-learn
```

## Help and Support
### Documentation

### Citation
