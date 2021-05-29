#
# DietProblem_Gurobi.py
#
# Usage... > python DietProblem_Gurobi.py
#
# Note that Gurobi must be properly setup with a valid license.
#


import gurobipy as gp
from gurobipy import GRB

import ReadCSVFiles


#
# BuildDietModel: builds a diet model that can be solved and modified.  
#
# Note that the building the model involves:
#    - creating the model
#    - making the decision variables
#    - making the objective function
#    - adding in constraints
#
def BuildDietModel (foodNames, foodCategories, foodData, foodCosts, dietaryReqs):

    # Model
    print ('Creating the model...')
    model = gp.Model ('diet')

    # Create the decision variables... one by one
    print ('Creating decision variables...')
    amountsToBuy = {}
    for food in foodNames:
        amountsToBuy [food] = model.addVar (name=food)

    # make and assign the objective function
    print ('Making objective function...') 
    expression = gp.LinExpr ()
    for food in foodNames:
        # note addTerms parameters are in the form of value then variable
        expression.addTerms (foodCosts [food], amountsToBuy [food])
    model.setObjective (expression, GRB.MINIMIZE)

    # Add constraints...
    print ('Adding in constraints...')
    for category in foodCategories:
        expression = gp.LinExpr ()
        for food in foodNames:
            expression.addTerms (foodData[food][category], amountsToBuy[food])
        model.addRange (expression, dietaryReqs[category]['min'], dietaryReqs[category]['max'], category)

    return model


#
# printSolution: used to dump out key elements from a solved model
#
def printSolution (model, foodNames, foodCategories, foodData):

    if model.status == GRB.OPTIMAL:

        print (f'Optimal Cost: {model.objVal:.2f}')

        modelVars = model.getVars ()

        print ('Foods to Buy: ')
        for var in modelVars:
            if var.varName in foodNames and var.x > 0.0001:
                print (f'{var.varName:11}  {var.x:.2f}')
        print ()

        print ('Amounts... ')
        for category in foodCategories:
            total = 0
            for var in modelVars:
                if var.varName in foodNames and var.x > 0.0001:
                    total += var.x * foodData[var.varName][category]
            print (f'    {category:11}  {total:.2f}')

    else:
        print ('No solution')



#
# Load the data...
#
print ('Loading Food Data...')
foodNames, foodCategories, foodData = ReadCSVFiles.readFoodCSVFile ('Foods.csv')

print ('Loading Cost Data...')
foodCosts = ReadCSVFiles.readCostCSVFile ('Costs.csv')

print ('Loading Dietary Requirements Data...')
dietaryReqs = ReadCSVFiles.readDietaryReqCSVFile ('DietaryRequirements.csv')


#
# Solve... that is build a model, solve it (or optimize it), and print out the results
#
model = BuildDietModel (foodNames, foodCategories, foodData, foodCosts, dietaryReqs)
model.optimize ()

printSolution (model, foodNames, foodCategories, foodData)



