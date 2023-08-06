import unittest
import numpy
import sys

sys.path.append('..')
from simple_linear_regr import SimpleLinearRegression
from simple_linear_regr_utils import generate_data, evaluate


class SimpleLinearRegressionTest(unittest.TestCase):
    def test_predict(self):
        X_train, y_train, X_test, y_test = generate_data()
        model = SimpleLinearRegression(iterations=1, lr=0.001)
        model.fit(X_train, y_train)
        pred = model.predict([[1], [2], [3], [4]])

        self.assertEqual(pred.shape, (4, 1))  # add assertion here


if __name__ == '__main__':
    unittest.main()
