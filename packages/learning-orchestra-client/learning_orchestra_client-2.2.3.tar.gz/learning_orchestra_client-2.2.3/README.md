<p align="center">
    <img src="./learningOrchestra-python-client.png">
    <img src="https://img.shields.io/badge/build-passing-brightgreen?style=flat-square" href="https://shields.io/" alt="build-passing">
    <img src="https://img.shields.io/github/v/tag/learningOrchestra/learningOrchestra-python-client?style=flat-square" href="https://github.com/riibeirogabriel/learningOrchestra/tags" alt="tag">
    <img src="https://img.shields.io/github/last-commit/learningOrchestra/learningOrchestra-python-client?style=flat-square" href="https://github.com/learningOrchestra/learningOrchestra-python-client/tags" alt="last-commit">
</p>

# pythonClient

Python client for [learningOrchestra](https://github.com/learningOrchestra/learningOrchestra).

# Installation

Requires Python 3.x

```
pip install learning-orchestra-client
```

# Usage

Each interoperable REST API service described in Learning Orchestra is translated 
into Python. Details at [python client docs](https://learningorchestra.github.io/pythonClient/). 
Furthermore, some extra method calls are included into Python client API to simplify 
even more the Machine Learning services. For instance, the REST API is asynchronous, 
except for GET HTTP requests, but the Python client enables also the synchronous API calls. 
The wait API method, useful to receive notifications from ML pipes, is another important 
example to illustrate an extension of the original REST API. 


# Example

* [Here](pipeline/titanic.py) has an example using the [Titanic Dataset](https://www.kaggle.com/c/titanic/overview):
* [Here](pipeline/imdb.py) has an example using the [Sentiment Analysis On IMDb reviews](https://www.kaggle.com/avnika22/imdb-perform-sentiment-analysis-with-scikit-learn):
* [Here](pipeline/mnist_async.py) has an example using the [MNIST Dataset](http://yann.lecun.com/exdb/mnist/):


