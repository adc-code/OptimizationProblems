#
# ReadCSVFiles.py
#
# Note that this code is simply used to import data from CSV files to python lists
# and dictionaries.  No validity checking or anything else is being done.
#


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
                firstRow = False

            else:
           
                foodNames.append ( row[0] ) 

                rowIndex = 1
                nutrientData [ row[0] ] = {}
                for nutrient in nutrientNames:
                    nutrientData [row[0]][nutrient] = float (row[rowIndex])
                    rowIndex += 1

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
           
                foodCosts [ row[0] ] = { 'unitCost':    float (row[1]),
                                         'minQuantity': float (row[2]),
                                         'maxQuantity': float (row[3])  }

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
          
                maxValue = 9e9;
                if row[2] != 'INF': 
                    maxValue = float (row[2])

                dietaryReqs [ row[0] ] = { 'min':  float (row[1]), 
                                           'max':  maxValue  }

        return dietaryReqs


