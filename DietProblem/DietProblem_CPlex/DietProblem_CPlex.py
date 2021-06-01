#
# DietProblem_CPlex.py
#
# Script to solve the Stigler diet, that is it selects a set of foods that
# satisfy a set of nutritional requirements (defined by both min and max 
# values) that have a minimal cost.
#
# Note: This is the CPlex version
#
# > python DietProblem_CPlex.py
#



from docplex.mp.model import Model
from docplex.util.environment import get_environment
import ReadCSVFiles



# 
# Build the model
# 
def buildDietModel (foods, foodNames, categoryNames, nutrientData, dietaryReqs, name='diet', **kwargs):

    # solve variables as integers or floats...
    ints = kwargs.pop ('ints', False)

    # Make the model
    print ('** Making model')
    model = Model (name=name, **kwargs)

    #
    # Decision variables, limited to a range (0 to max)
    #
    print ('   -> adding decision variables ')
    amountToBuy = {}
    for food in foods:
        amountToBuy [food] = model.continuous_var (lb=foods[food]['minQuantity'], ub=foods[food]['maxQuantity'], name=(food))

    print ('   -> adding constraints ')
    for category in categoryNames:
        categoryAmount = model.sum ( amountToBuy [food] * nutrientData [food][category] for food in foods )
        model.add_range ( dietaryReqs[category]['min'], categoryAmount, dietaryReqs[category]['max'] );

    print ('   -> adding objective function ')
    objectiveFunction = model.sum ( amountToBuy [food] * foods [food]['unitCost'] for food in foods )
    model.minimize (objectiveFunction)

    return model


# 
# Solve the model and display the result
# 
if __name__ == '__main__':

    # 
    # Load the data...
    # 
    foods = ReadCSVFiles.readCostCSVFile ('Foods.csv')
    foodNames, categoryNames, nutrientData = ReadCSVFiles.readFoodCSVFile ('FoodData.csv')
    dietaryReqs = ReadCSVFiles.readDietaryReqCSVFile ('DietaryReqs.csv')

    #
    # Making the model...
    #
    model = buildDietModel (foods, foodNames, categoryNames, nutrientData, dietaryReqs,\
                            ints=False, log_output=True, float_precision=6)
    model.print_information ()

    solution = model.solve ()
    print ()

    if solution:

        model.print_solution ()
        print ()

        totalCost = 0
        print (f"{'Food':22}   Amount  Cost")
        for food in foods:
            decVar = model.get_var_by_name (food)
            cost = foods [food]['unitCost'] * decVar.solution_value
            totalCost += cost
            print (f'{food:22}  {decVar.solution_value:6.3f}   {cost:.2f}')

        print ()
        print (f'Total Cost: {totalCost:.2f}')
        print ()

        print ('Daily Requirement Categories')
        for category in categoryNames:
            categoryAmount = 0
            for food in foods:
                decVar = model.get_var_by_name (food)
                categoryAmount += ( decVar.solution_value * nutrientData [food][category] )

            print (f'{category:15}  {categoryAmount:7.2f}')



