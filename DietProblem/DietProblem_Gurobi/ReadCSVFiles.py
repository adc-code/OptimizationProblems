import csv


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
                nutrientNames.remove ('food')
                firstRow = False

            else:
           
                foodNames.append ( row[0] ) 
                nutrientData [ row[0] ] = { 'calories': float (row[1]),
                                            'protein':  float (row[2]),
                                            'fat':      float (row[3]),
                                            'sodium':   float (row[4]) }

        return (foodNames, nutrientNames, nutrientData)


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





#foodNames, nutrientNames, nutrientData = readCSVFile ('Foods.csv')
#print (nutrientNames, nutrientData)

#totalFat = 0;
#for food in foodNames:
#    totalFat += nutrientData[food]['fat']

#print (totalFat)

