#
# DietProblemSolver_Glop
#
# Glop version of the diet problem solver
#


from DietProblemSolver import DietProblemSolver
from ortools.linear_solver import pywraplp
import ortools


class DietProblemSolver_Glop (DietProblemSolver):

    #
    # GetSolverName... returns the name and version of the solver instance
    #
    def GetSolverName (self):
        return 'GLOP - ORTools ' + ortools.__version__


    #
    # BuildModel... builds a Glop version
    #
    def BuildModel (self):

        #print ('DietProblemSolver_Glop buildModel')

        # make the model
        self._model = pywraplp.Solver ('DietProblem', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING) 

        # make an empty objective function to be filled later
        objective = self._model.Objective()

        # make decision variables and complete the objective function
        self._amountToBuy = {}
        for food in self._foodNames:
            self._amountToBuy [food] = self._model.NumVar (self._foodCosts[food]['minQuantity'], \
                                                           self._foodCosts[food]['maxQuantity'], \
                                                           food)

            # sets the coefficient for the objective function
            objective.SetCoefficient (self._amountToBuy[food], self._foodCosts[food]['unitCost'])

        objective.SetMinimization()

        # make the constraints
        constraints = {}

        for nutrient in self._nutrientNames:
            # Make a constraint for each nutrient... min is defined, max is infinity
            constraints [nutrient] = self._model.Constraint (self._dietaryReqs[nutrient]['min'], \
                                                             self._dietaryReqs[nutrient]['max'], \
                                                             nutrient)

            # for each food item
            for food in self._foodNames:
                constraints [nutrient].SetCoefficient (self._amountToBuy[food], self._nutrientData[food][nutrient])


    #
    # SolveModel
    #
    def SolveModel (self):

        #print ('DietProblemSolver_Glop solvemodel')

        if self._model != None:
            self._solveStatus = self._model.Solve ()


    #
    # PrintResults... outputs any useful results if possible
    #
    def PrintResults (self):

        # print ('DietProblemSolver_Glop printresults')

        if self._solveStatus == self._model.OPTIMAL:

            # Display the amounts (in dollars) to purchase of each food.
            cost = 0
            for food in self._foodNames:
                cost += self._amountToBuy[food].solution_value() * self._foodCosts[food]['unitCost'];

                if self._amountToBuy[food].solution_value() > 0.001:
                    print (f'{food:25} --> {self._amountToBuy[food].solution_value():7.3f} units/servings   {self._amountToBuy[food].solution_value()*self._foodCosts[food]["unitCost"]:.2f}')

            totalNutrients = {}
            for nutrient in self._nutrientNames:
                totalNutrients [nutrient] = 0
                for food in self._foodNames:
                    totalNutrients [nutrient] += self._amountToBuy[food].solution_value() * self._nutrientData[food][nutrient]

            print ()
            print (f'Optimal daily cost:  {cost:7.2f}')
            print (f'Optimal annual cost: {(365 * cost):7.2f}')
            print ()

            for nutrient in totalNutrients:
                print (f'{nutrient:15} -->  {totalNutrients[nutrient]:7.2f}')

        else:  

            # No optimal solution was found.
            if status == model.FEASIBLE:
                print ('A potentially suboptimal solution was found.')
            else:
                print ('The solver could not solve the problem.')



