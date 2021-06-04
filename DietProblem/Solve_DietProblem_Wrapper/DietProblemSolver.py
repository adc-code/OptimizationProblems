#
# DietProblemSolver
# 
# Base class for various 'Diet Problem' solvers.  Since python is somewhat limited in object
# oriented functionality such as with C++, it should be noted that one should not derive objects
# from this class.  Rather, one needs to use one of the derived classes for the specific type of
# solved (Gurobi, Glop, or Cplex).
#

class DietProblemSolver ():

    #
    # Constructor... just assign and initialize some variables
    #
    def __init__ (self, foodNames, nutrientNames, nutrientData, foodCosts, dietaryReqs):

        self._foodNames     = foodNames
        self._nutrientNames = nutrientNames
        self._nutrientData  = nutrientData
        self._foodCosts     = foodCosts
        self._dietaryReqs   = dietaryReqs

        self._model         = None
        self._solveStatus   = -1

    #
    # GetSolverName... returns the name and version of the solver instance
    #
    def GetSolverName (self): 
        pass

    #
    # BuildModel... should do everything to setup a model; that is create decision variables,
    #               set constraints, and specify the objective function
    #
    def BuildModel (self):
        pass

    #
    # SolveModel... solves the model; that is calls the appropriate function which will solve
    #               the model depending on the type of solver specified
    # 
    def SolveModel (self):
        pass

    #
    # PrintResults... if the model was built and solved, this function will output the results
    #
    def PrintResults (self):
        pass


