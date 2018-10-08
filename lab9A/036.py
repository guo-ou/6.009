import numpy as np

B = np.array([[1,10], [1,10], [10,1] ,[1,10],[10,1]])
Z = np.array([[1],[1],[5],[1],[5]])
a = np.array([[10],[1]])

print(np.dot(np.dot(np.dot(np.linalg.inv(np.dot(B.T, B) + np.identity(2)), B.T), Z).T,a).tolist())
