#
# DietProblem_Glop.py
#
# Script used to solve the diet problem using Google's Glop.  This version is a bit different than
# the example from the project's website where data is supplied as CSV files.  In the future, this
# will be hopefully changed so that values will be taken from a database.
#
# Usage:
# > python DietProblem_Glop.py
#
# The datafile are organized as follows:
# - DietaryReqs.csv: minimum dietary requirements for each nutrient
# - FoodCosts.csv: contains the costs of various foods
# - FoodData.csv: contains the nutrient amounts for each food 
#

from ortools.linear_solver import pywraplp


import ReadCSVFiles


#
# SolveDietProblem: solves and prints the results for the diet problem
#
def SolveDietProblem (foodNames, nutrientNames, nutrientData, foodCosts, dietaryReqs):

    # make the model
    model = pywraplp.Solver ('DietProblem', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # make an empty objective function to be filled later
    objective = model.Objective()

    # make decision variables and complete the objective function
    amountToBuy = {}
    for food in foodNames:
        amountToBuy [food] = model.NumVar (0.0, model.infinity(), food)

        # sets the coefficient for the objective function
        objective.SetCoefficient (amountToBuy[food], 1)

    objective.SetMinimization()

    # make the constraints
    constraints = {}

    for nutrient in nutrientNames:
        # Make a constraint for each nutrient... min is defined, max is infinity
        constraints [nutrient] = model.Constraint (dietaryReqs[nutrient]['min'], model.infinity(), nutrient)

        # for each food item
        for food in foodNames:
            constraints [nutrient].SetCoefficient (amountToBuy[food], nutrientData[food][nutrient])

    # solve the model
    status = model.Solve()

    if status == model.OPTIMAL:

        # Display the amounts (in dollars) to purchase of each food.
        cost = 0
        for food in foodNames:
            cost += amountToBuy[food].solution_value()

            if amountToBuy[food].solution_value() > 0:
                print (f'{food:25} --> {amountToBuy[food].solution_value():.5f}')

        totalNutrients = {}
        for nutrient in nutrientNames:
            totalNutrients [nutrient] = 0
            for food in foodNames:
                totalNutrients [nutrient] += amountToBuy[food].solution_value() * nutrientData[food][nutrient]

        print ()
        print (f'Optimal daily cost (in 1939 money):  {cost:.2f}')
        print (f'Optimal annual cost (in 1939 money): {(365 * cost):.2f}')
        print ()

        for totalNut in totalNutrients:
            print (f'{totalNut:11} -->  {totalNutrients[totalNut]:6.2f} {dietaryReqs[totalNut]["units"]}')

    else:  

        # No optimal solution was found.
        if status == model.FEASIBLE:
            print('A potentially suboptimal solution was found.')
        else:
            print('The solver could not solve the problem.')



if __name__ == '__main__':

    dietaryReqs = ReadCSVFiles.readDietaryReqCSVFile ('DietaryReqs.csv')
    foodCosts = ReadCSVFiles.readCostCSVFile ('FoodCosts.csv')
    foodNames, nutrientNames, nutrientData = ReadCSVFiles.readFoodCSVFile ('FoodData.csv')

    SolveDietProblem (foodNames, nutrientNames, nutrientData, foodCosts, dietaryReqs)


