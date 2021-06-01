#
# 
#


import csv


#
# readFoodCSVFile: read the FOOD file... that is the file containing the nutrition
#                  data for each food
#
def readFoodCSVFile (fileName):

    with open (fileName, newline='') as csvfile:

        csvReader = csv.reader (csvfile, delimiter=',')

        foodNames     = [] 
        nutrientNames = []
        nutrientData  = {}

        firstRow = True
        for row in csvReader:

            if firstRow:
  
                nutrientNames = row;
                nutrientNames.remove ('FoodName')
                firstRow = False

            else:
           
                foodNames.append ( row[0] ) 
                nutrientData [ row[0] ] = { 'Calories':      float (row[1]),
                                            'Calcium':       float (row[2]),
                                            'Iron':          float (row[3]),
                                            'Vitamin_A':     float (row[4]),
                                            'Dietary_Fiber': float (row[5]),
                                            'Carbohydrates': float (row[6]),
                                            'Protein':       float (row[7]) }

        return (foodNames, nutrientNames, nutrientData)


#
# readCostCSVFile: read the COST file... that is the file containing the costs
#                  for each food.  Note that it could be part of the Food file,
#                  but this way different versions can exist for different stores
#
def readCostCSVFile (fileName):

    with open (fileName, newline='') as csvfile:

        csvReader = csv.reader (csvfile, delimiter=',')

        foodCosts = {}

        firstRow = True
        for row in csvReader:

            if firstRow:
  
                firstRow = False
                continue

            else:
           
                foodCosts [ row[0] ] = { 'unitCost':    float (row[1]),
                                         'minQuantity': float (row[2]),
                                         'maxQuantity': float (row[3])  }

        return foodCosts 


#
# readDietaryReqCSVFile: read the DIETARY REQUIREMENTS file.  This is the file
#                        containing the min and max values for each nutrient
#
def readDietaryReqCSVFile (fileName):

    with open (fileName, newline='') as csvfile:

        csvReader = csv.reader (csvfile, delimiter=',')

        dietaryReqs = {}

        firstRow = True
        for row in csvReader:

            if firstRow:
  
                firstRow = False
                continue

            else:
           
                dietaryReqs [ row[0] ] = { 'min': float (row[1]),
                                           'max': float (row[2]) }

        return dietaryReqs


