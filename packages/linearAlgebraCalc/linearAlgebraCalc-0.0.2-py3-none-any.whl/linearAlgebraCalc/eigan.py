from linearAlgebraCalc.basicOperations import *
from linearAlgebraCalc.globalFunctions import *
from linearAlgebraCalc.matrixOperations import *

#from basicOperations import *
#from matrixOperations import *
#from globalFunctions import *

def eiganValuesCalc(a):

    return 5

class eiganMatrix:

    def __init__(self, a):
        
        dim = arrDim(a)

        if all(isinstance(x, list) for x in a) and dim[0] == dim[1]:
            self.eiganValues = eiganValuesCalc(a)
        else:
            errorTraceback()
            printError('List of lists not found for matrix A')

