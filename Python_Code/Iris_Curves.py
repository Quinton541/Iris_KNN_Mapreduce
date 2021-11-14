import pandas as pd
import matplotlib.pyplot as plt
iris = pd.read_csv("iris.csv")

pd.plotting.andrews_curves(iris,"Species")
plt.show()
pd.plotting.parallel_coordinates(iris, "Species")
plt.show()
pd.plotting.radviz(iris, "Species")
plt.show()