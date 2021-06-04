#
# DietProblemSolver_CPlex.py
# 
# CPlex version for the diet problem solver
#


from DietProblemSolver import DietProblemSolver

from docplex.mp.model import Model
from docplex.util.environment import get_environment
import cplex


class DietProblemSolver_CPlex (DietProblemSolver):

    #
    # GetSolverName... returns the name and version of the solver instance
    #
    def GetSolverName (self): 

        return 'CPlex ' + cplex.Cplex().get_version()


    #
    # BuildModel... build a CPlex based model
    #
    def BuildModel (self):

        #print ('DietProblemSolver_CPlex buildModel')

        # Make the model
        self._Model = Model (name='DietProblem')

        # Decision variables, limited to a range 
        self._amountToBuy = {}
        for food in self._foodNames:
            self._amountToBuy [food] = self._Model.continuous_var (lb = self._foodCosts[food]['minQuantity'], \
                                                                   ub = self._foodCosts[food]['maxQuantity'], \
                                                                   name = (food))

        # adding constraints 
        for nutrient in self._nutrientNames:
            categoryAmount = self._Model.sum ( self._amountToBuy [food] * self._nutrientData [food][nutrient] for food in self._foodNames )

            self._Model.add_range ( self._dietaryReqs[nutrient]['min'], \
                                    categoryAmount, 
                                    self._dietaryReqs[nutrient]['max'] )

        # adding objective function 
        objectiveFunction = self._Model.sum ( self._amountToBuy [food] * self._foodCosts [food]['unitCost'] for food in self._foodNames )
        self._Model.minimize (objectiveFunction)


    #
    # SolveModel
    #
    def SolveModel (self):

        #print ('DietProblemSolver_CPlex solvemodel')

        if self._Model != None:
            self._Model.solve ()
            self._solveStatus = self._Model.solve_details.status_code


    #
    # PrintResults
    #
    def PrintResults (self):

        # print ('DietProblemSolver_CPlex printresults')

        # uncomment for debugging
        #self._Model.print_information ()
        #self._Model.print_solution ()

        if self._solveStatus == True:

            totalCost = 0
            print (f"{'Food':22}   Amount  Cost")
            for food in self._foodNames:
                decVar = self._Model.get_var_by_name (food)
                cost = self._foodCosts [food]['unitCost'] * decVar.solution_value
                totalCost += cost
                if decVar.solution_value > 0.001:
                    print (f'{food:22}  {decVar.solution_value:6.3f}   {cost:.2f}')

            print ()
            print (f'Total Cost: {totalCost:.2f}')
            print ()

            print ('Daily Requirement Categories')
            for nutrient in self._nutrientNames:
                categoryAmount = 0
                for food in self._foodNames:
                    decVar = self._Model.get_var_by_name (food)
                    categoryAmount += ( decVar.solution_value * self._nutrientData [food][nutrient] )

                print (f'{nutrient:15}  {categoryAmount:7.2f}')

        else:  
         
            # should add more to this...
            print ('no solution')



