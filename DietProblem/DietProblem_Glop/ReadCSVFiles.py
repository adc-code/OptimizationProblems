import csv


#
# readFoodCSVFile: used to read the food data file.  That is the file that
#                  contains all the nutrients for each food item.
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
                nutrientNames.remove ('Food')
                nutrientNames.remove ('Amount')
                firstRow = False

            else:
           
                foodNames.append ( row[0] ) 
                nutrientData [ row[0] ] = { 'Calories':   float (row[2]),
                                            'Protein':    float (row[3]),
                                            'Calcium':    float (row[4]),
                                            'Iron':       float (row[5]), 
                                            'Vitamin_A':  float (row[6]),
                                            'Vitamin_B1': float (row[7]),
                                            'Vitamin_B2': float (row[8]),
                                            'Niacin':     float (row[9]),  
                                            'Vitamin_C':  float (row[10]) }

        return (foodNames, nutrientNames, nutrientData)


#
# readCostCSVFile: reads the food cost file.  
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
           
                foodCosts [ row[0] ] = float (row[1])

        return foodCosts 


#
# readDietaryReqCSVFile: reads the dietary requirements file
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
           
                dietaryReqs [ row[0] ] = { 'units': row[1],
                                           'min':   float (row[2]) }

        return dietaryReqs


