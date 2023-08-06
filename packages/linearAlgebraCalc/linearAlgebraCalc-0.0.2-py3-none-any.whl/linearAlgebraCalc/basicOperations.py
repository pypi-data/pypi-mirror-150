from linearAlgebraCalc.globalFunctions import *

#from globalFunctions import *

def multiply(a,b):

    if len(b) == len(a[0]):

        result = [[0 for z in range(len(b[0]))] for w in range(len(a))]

        for i in range(len(a)):
            for j in range(len(b[0])):
                for k in range(len(b)):
                    result[i][j] += a[i][k] * b[k][j]

        return result
    
    else:
        errorTraceback()
        printError('Columns of first matrix must match rows of second matrix!')

def matrixAdd(a, b):

    if arrDim(a) == arrDim(b):

        result = []
        for i in range(len(a)):
            appendList = []
            for k in range(len(a[0])):
                appendList.append(a[i][k] + b[i][k])
            result.append(appendList)

        return result
    else:
            errorTraceback()
            printError('Both matrices must have the same dimensions!')

def matrixSub(a, b):

    if arrDim(a) == arrDim(b):

        result = []
        for i in range(len(a)):
            appendList = []
            for k in range(len(a[0])):
                appendList.append(a[i][k] - b[i][k])
            result.append(appendList)

        return result
    else:
            errorTraceback()
            printError('Both matrices must have the same dimensions!')

def scalarMatrixMultiply(a, k):

    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = (a[i][j] * k)

    return a 
