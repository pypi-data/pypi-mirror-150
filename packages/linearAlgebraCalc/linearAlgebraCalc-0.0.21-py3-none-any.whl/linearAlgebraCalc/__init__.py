from linearAlgebraCalc.basicOperations import *
from linearAlgebraCalc.globalFunctions import *
from linearAlgebraCalc.matrixOperations import *
from linearAlgebraCalc.eigan import *

# Delete when publishing 
# from basicOperations import *
# from matrixOperations import *
# from globalFunctions import *
# from eigan import *

def mult(a, b):
    if all(isinstance(x, list) for x in a) and all(isinstance(x, list) for x in b):
        return multiply(a,b)
        #return matrixMultiply(a,b)
    else:
        errorTraceback()
        printError('List of lists not found for matrices A and B')

# Working multiplication
#print(mult([[1,2]], [[3,4], [5,6]]))
# Intential Error:
#print(mult([1,2], [[3,4]]))

def add(a, b):
    if all(isinstance(x, list) for x in a) and all(isinstance(x, list) for x in b):
        return matrixAdd(a,b)
    else:
        errorTraceback()
        printError('List of lists not found for matrices A and B')

def sub(a, b):
    if all(isinstance(x, list) for x in a) and all(isinstance(x, list) for x in b):
        return matrixSub(a,b)
    else:
        errorTraceback()
        printError('List of lists not found for matrices A and B')

# Working addition
#print(add([[1,2], [7,8]], [[3,4], [5,6]]))
# Intential Error:
#print(sub([[1,2] , [1,1]], [[3,4] , [5,6]]))

def scalarMultiply(a, k):
    if all(isinstance(x, list) for x in a):
        return scalarMatrixMultiply(a, k)
    else:
        errorTraceback()
        printError('List of lists not found for the matrix')

# Working
#print(scalarMultiply([[1,2], [7,8]] , 3))

def determinent(a):
    if all(isinstance(x, list) for x in a):
        return matrixDeterminent(a)
    else:
        errorTraceback()
        printError('List of lists not found for the matrix')

# Working 
#print(determinent([[1,2] , [3,4]]))
# Failure
#print(determinent([[1,2]]))

def transpose(a):
    if all(isinstance(x, list) for x in a):
        return transposeMatrix(a)
    else:
        errorTraceback()
        printError('List of lists not found for the matrix')

# Working 
# print(transpose([[1,2,6,7] , [3,4,5,5], [5,6,3,2]]))

def inverse(a):
    if all(isinstance(x, list) for x in a):
        return inverseMatrix(a)
    else:
        errorTraceback()
        printError('List of lists not found for the matrix') 

# Working 
#print(inverse([[1,2,3] , [3,4,6], [3,4,5]]))

def solve(a,b):
    if all(isinstance(x, list) for x in a) and isinstance(b, list):
        return systemEquations(a,b)
    else:
        errorTraceback()
        printError('List of lists not found for the matrix') 

# Working
#print(solve([[1, 1, 1], [0, 2, 5], [2, 5, -1]] , [6, -4, 27]))
#print(solve([[1,2,1,-1] , [1.5,1,2,2] , [4,4,3,4] , [2/5, 0, 1/5, 1]] , [5,8,22,3]))

m1 = eiganMatrix([[2,3],[2,3]])
print(m1.eiganValues)