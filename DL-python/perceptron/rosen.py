#!/packages/envs/scicomp/bin/python
# From:
# https://towardsdatascience.com/rosenblatts-perceptron-the-very-first-neural-network-37a3ec09038a
# --> Import standard Python libraries.
import numpy as np

# --> Import sklearn utility functions to create derived-class objects.
from sklearn.base import BaseEstimator, ClassifierMixin

# --> Redefine the Heaviside function.
H = lambda x: np.heaviside(x, 1).astype(int)

class Rosenblatt(BaseEstimator, ClassifierMixin):
    """
    Implementation of Rosenblatt's Perceptron using sklearn BaseEstimator and
    ClassifierMixin.
    """

    def __init__(self):
        return

    def predict(self, X):
        return H( X.dot(self.weights) + self.bias )

    def fit(self, X, y, epochs=100):
        
        """
        Implementation of the Perceptron Learning Algorithm.
        
        INPUT
        -----
        
        X : numpy 2D array. Each row corresponds to one training example.
        
        y : numpy 1D array. Label (0 or 1) of each example.
        
        OUTPUT
        ------
        
        self : The trained perceptron model.
        """

        # --> Number of features.
        n = X.shape[1]

        # --> Initialize the weights and bias.
        self.weights = np.zeros((n, ))
        self.bias = 0.0
        errors    = None
        loop_count = 0
        # --> Perceptron algorithm loop.
        while loop_count < epochs and errors != 0:
            # --> Current number of errors.
            errors = 0
            # --> Loop through the examples.
            for xi, y_true in zip(X, y):
                # --> Compute error.
                error = y_true - self.predict(xi)
                if error != 0:
                    # --> Update the weights and bias.
                    self.weights += error * xi
                    self.bias += error
                    # --> Current number of errors.
                    errors += 1
            loop_count += 1
        self.epochs = loop_count
        return self
