# PyStatsLearn

This is a python module which is made for education purpose. The aim is to implement machine learning algorithms and publish it. Currenlty this package has 2 functionalities
1. Calculating mean by taking a dataframe as an input. (Mean Calculates is not done by using any library. The code is developed from scratch)
2. Implemeted Gaussian Naive Bayes Classifier which is build upon numpy

# Installation

```
pip install PyStatsLearn
```

# Usage

```
import pandas as pd
from PyStatsLearn import Measure, GaussianNaiveBayesClassifier
from sklearn.model_selection import train_test_split

df = pd.read_excel('data.xlsx')

a = Measure(df)
print(a.mean('Insulin'))

b = GaussianNaiveBayesClassifier()

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

X = X.to_numpy()
y = y.to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25)

nb_classifier = GaussianNaiveBayesClassifier()

nb_classifier.train(X_train, y_train)

predictions = nb_classifier.predict(X_test)
print(predictions)
```
