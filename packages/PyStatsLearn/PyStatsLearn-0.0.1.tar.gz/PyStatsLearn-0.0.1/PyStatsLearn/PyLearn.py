import numpy as np
from scipy.stats import norm

class Measure:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def mean(self,column_name):
        column_values = self.dataframe[column_name]
        self.count_values = 0
        self.sum_values = 0
        for value in column_values:
            self.count_values += 1
            self.sum_values += value
        if self.count_values > 0:
            mean_value = self.sum_values / self.count_values
        else:
            mean_value = None

        return mean_value

class GaussianNaiveBayesClassifier:
    def __init__(self):
        self.classes_ = None
        self.class_priors_ = None
        self.feature_params_ = None

    def train(self, X, y):

        self.classes_ = np.unique(y)
        self.class_priors_ = self.calculate_priors_(y)
        self.feature_params_ = self.calculate_feature_params_(X, y)

    def calculate_priors_(self, y):
        class_counts = np.bincount(y)
        total_samples = len(y)
        class_priors_ = class_counts / total_samples
        return class_priors_

    def calculate_feature_params_(self, X, y):
        num_features = X.shape[1]
        feature_params_ = []
        for c in self.classes_:
            X_class = X[y == c]
            feature_params__class = []
            for i in range(num_features):
                feature_values = X_class[:, i]
                mean = np.mean(feature_values)
                std = np.std(feature_values)
                feature_params__class.append((mean, std))
            feature_params_.append(feature_params__class)
        return feature_params_


    def predict(self, X):

        predictions = []
        for sample in X:
            class_scores = []
            for i, c in enumerate(self.classes_):
                class_score = np.log(self.class_priors_[i])
                for j, feature_value in enumerate(sample):
                    mean, std = self.feature_params_[i][j]
                    feature_probability = norm.pdf(feature_value, mean, std)
                    class_score += np.log(feature_probability)
                class_scores.append(class_score)
            predicted_class = self.classes_[np.argmax(class_scores)]
            predictions.append(predicted_class)
        return predictions
