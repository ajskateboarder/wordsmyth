import numpy as np

def mse(actual, predicted):
    return np.square(np.subtract(np.array(actual), np.array(predicted))).mean()

print(mse(1, 1.2))