#
# SolveDietProblem.py
#
# Script that will solve the diet problem with the selected solver.
#
# Usage:
# > python  SolveDietProblem.py <SolverName>  <DataSetDir>
#
# Where:
# - <SolverName> : is either Gurobi, Cplex, or Glop
# - <DataSetDir> : is the directory containing the 3 CSV datafiles (for nutrient, cost, and requirement data)
#


import sys
import os.path
from os import path

import ReadCSVFiles

from DietProblemSolver import DietProblemSolver
from DietProblemSolver_Glop import DietProblemSolver_Glop
from DietProblemSolver_Gurobi import DietProblemSolver_Gurobi
from DietProblemSolver_CPlex import DietProblemSolver_CPlex

DIETARY_REQ_FILENAME = 'DietaryReqs.csv'
FOODCOST_FILENAME    = 'FoodCosts.csv'
FOODDATA_FILENAME    = 'FoodData.csv'


if len (sys.argv) != 3:

    print ('Error: incorrect number of parameters')
    print ()
    print ('Usage:')
    print (f'> python {sys.argv[0]}  <SolverName>  <DataSetDir>')
    print ()
    print ('Where:')
    print ('  <SolverName> : is either Gurobi, Cplex, or Glop')
    print ('  <DataSetDir> : is the directory containing the 3 CSV datafiles (for nutrient, cost, and requirement data)')

    sys.exit ()


#
# check the solver name parameter...
#
solverName = 'Unknown'

if sys.argv [1] == 'Glop' or sys.argv[1] == 'Cplex' or sys.argv[1] == 'Gurobi':
    solverName = sys.argv [1]

if solverName == 'Unknown':
    
    print ('Error: incorrect solver name')
    print ()
    print ('Valid Names: Glop, Cplex, or Gurobi')
    print (f'Given: {sys.argv [1]}')

    sys.exit ()


#
# check the data directory parameter...
# 
dataSetDir = sys.argv [2]

dietaryReqFilePath = dataSetDir + '/' + DIETARY_REQ_FILENAME
foodCostFilePath   = dataSetDir + '/' + FOODCOST_FILENAME
foodDataFilePath   = dataSetDir + '/' + FOODDATA_FILENAME

if path.exists (dietaryReqFilePath) == False or \
   path.exists (foodCostFilePath)   == False or \
   path.exists (foodDataFilePath)   == False:

    print ('Error: dataset file missing')
    print ()
    print (f'Could not either find: {DIETARY_REQ_FILENAME}, {FOODCOST_FILENAME}, or {FOODDATA_FILENAME}')

    sys.exit ()


#
# Read the data...
#
foodNames, nutrientNames, nutrientData = ReadCSVFiles.readFoodCSVFile (foodDataFilePath)
foodCosts                              = ReadCSVFiles.readCostCSVFile (foodCostFilePath)
dietaryReqs                            = ReadCSVFiles.readDietaryReqCSVFile (dietaryReqFilePath)


#
# Build the model...
#
DietProblemSolver = None
if solverName == 'Glop':
    DietProblemSolver = DietProblemSolver_Glop (foodNames, nutrientNames, nutrientData, foodCosts, dietaryReqs)

elif solverName == 'Gurobi':
    DietProblemSolver = DietProblemSolver_Gurobi (foodNames, nutrientNames, nutrientData, foodCosts, dietaryReqs)

elif solverName == 'Cplex':
    DietProblemSolver = DietProblemSolver_CPlex (foodNames, nutrientNames, nutrientData, foodCosts, dietaryReqs)


#
# If a model was built, use it and output the results...
#
if DietProblemSolver:

    print ('#')
    print ('# ' + DietProblemSolver.GetSolverName() )
    print ('#')
    print ()

    # Build the model... make the decision variables, add constraints, and an objective function
    DietProblemSolver.BuildModel ()

    # Attempt to solve the model... let the solver do its magic
    DietProblemSolver.SolveModel ()

    # Output any results if possible... decision variable values, nutrient amounts, objective function results 
    DietProblemSolver.PrintResults ()

else:

    print ('Error: Could not make a solver instance!')


