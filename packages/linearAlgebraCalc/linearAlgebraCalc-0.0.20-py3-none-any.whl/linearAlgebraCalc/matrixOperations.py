from linearAlgebraCalc.globalFunctions import *
from linearAlgebraCalc.basicOperations import *

# Delete 
#from basicOperations import *
#from globalFunctions import *

def __cofactor(a, i , j):
    return [row[: j] + row[j+1:] for row in (a[: i] + a[i+1:])]

def matrixDeterminent(a):

    dim = arrDim(a)

    if (dim[0] == dim[1]):
        if dim[0] == 2:
            deter = a[0][0] * a[1][1] - a[1][0] * a[0][1]
            return deter
        else: 
            deter = 0 

            for i in range(dim[0]):
                sign = (-1) ** i

                deterInner = matrixDeterminent(__cofactor(a, 0, i))
                deter += (sign * a[0][i] * deterInner)
            
            return deter
    else:
        errorTraceback()
        printError('Matrix is not a square matrix!')

def transposeMatrix(a):

    transposed = [[0 for x in range(len(a))] for y in range(len(a[0]))]

    for i in range(len(a[0])):
        for j in range(len(a)):
            transposed[i][j] = a[j][i]

    return transposed

def inverseMatrix(a):
    dim = arrDim(a)

    if (dim[0] == dim[1]):

        deter = matrixDeterminent(a)
        if (deter != 0):
            inverse = [[0 for x in range(len(a[0]))] for y in range(len(a))]

            if (len(inverse) == 1):
                inverse[0][0] = 1
            else:
                sign = 1

                for i in range(len(a)):
                    for j in range(len(a)):
                        cofacter = [[0 for x in range(len(a[0]))] for y in range(len(a))]
                        cofacter = __cofactor(a, i, j)
                        
                        if (i + j) % 2 == 0:
                            sign = 1
                        else:
                            sign = -1
                        
                        inverse[j][i] = (sign) * (matrixDeterminent(cofacter))
            
            for i in range(len(a)):
                for j in range(len(a)):
                    inverse[i][j] = inverse[i][j] / deter

            return inverse
        else:
            errorTraceback()
            printError('Singular matrix, no inverse!')
    else:
        errorTraceback()
        printError('Matrix is not a square matrix!')
    
def systemEquations(a,b):
    
    dimA = arrDim(a)
    
    if dimA[1] == len(b):
        
        invA = inverseMatrix(a)
        deter = matrixDeterminent(invA)
        tranB = transposeMatrix([b])

        for x in range(len(invA)):
            for y in range(len(invA[x])):
                invA[x][y] = (invA[x][y] / deter)

        S = multiply(invA, tranB)

        for i in range(len(S)):
            for j in range(len(S[0])):
                S[i][j] = round((S[i][j] * deter) , 2)

        return S

    else:
        errorTraceback()
        printError('Dimensions of augmented matrix do not match!')