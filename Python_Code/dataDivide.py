import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
def read_data():
    d=pd.read_csv("iris.csv")
    array=d.values
    return array
def train():
    array=read_data()

    x = array[:, 0:4]
    y = array[:, 4]

    X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, shuffle=True)

    X_train=X_train.T
    X_train=np.vstack((X_train,Y_train))
    np.savetxt('train.csv', X_train.T, delimiter=',')
    np.savetxt('test.csv', X_test, delimiter=',')
    np.savetxt('verify.csv', Y_test, delimiter='/n')
if __name__ == '__main__':
    train()
