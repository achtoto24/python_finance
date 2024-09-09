import numpy as np

A = np.array([[1, 2], [3, 4]])  #Array function that makes a list into an array
print(A)
print(type(A))
print(A.ndim)
print(A.shape)
print(A.dtype)
print("max : {},".format(A.max()), "mean : {}, ".format(A.mean()), "min : {},".format(A.min()), "sum : {}".format(A.sum()))
print()
print(A[0]); print(A[1]); print(A[0][0], A[0][1]); print(A[1][0], A[1][1])
print(A[0, 0], A[0, 1]); print(A[1, 0], A[1, 1])    #same as the upper raw
print(A[A>1])

'''======================================================================='''
print(A.T)  #same as 'A.transpose()'
print(A.flatten())

'''======================================================================='''
A = np.array([[1, 2], [3, 4]])
B = np.array([10, 100])
print(A * B)    #multipling is possible beacause of B's broadcasting
#internal computation of the array
B.dot(B)    # One-dimensional array internal computation is possible in numpy; same as 'np.dot(B, B)'
A.dot(B)







