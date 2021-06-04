#
# DietProblemSolver_Gurobi.py
#
# Gurobi version of the diet solver.
#

from DietProblemSolver import DietProblemSolver

import gurobipy as gp
from gurobipy import GRB

import subprocess


class DietProblemSolver_Gurobi (DietProblemSolver):

    #
    # GetSolverName... returns the name and version of the solver instance
    #
    def GetSolverName (self): 

        # this isn't the nicest way of doing this but it works for now...
        versionOutput = subprocess.check_output ('/usr/local/bin/gurobi_cl --version', shell=True)
        versionOutput = versionOutput.decode ('utf-8')
        version = versionOutput.split ('\n')

        return (version[0])


    #
    # BuildModel... build a gurobi model 
    #
    def BuildModel (self):

        # print ('DietProblemSolver_Gurobi buildModel')

        # make the model
        self._model = gp.Model ('DietProblem')

        # Create the decision variables... one by one
        self._amountsToBuy = {}
        for food in self._foodNames:
            self._amountsToBuy [food] = self._model.addVar (name=food)

        # make and assign the objective function
        expression = gp.LinExpr ()
        for food in self._foodNames:
            # note addTerms parameters are in the form of value then variable
            expression.addTerms (self._foodCosts [food]['unitCost'], self._amountsToBuy [food])

        self._model.setObjective (expression, GRB.MINIMIZE)

        # Add constraints...
        for category in self._nutrientNames:
            expression = gp.LinExpr ()
            for food in self._foodNames:
                expression.addTerms (self._nutrientData[food][category], self._amountsToBuy[food])

            self._model.addRange (expression, \
                                  self._dietaryReqs[category]['min'], \
                                  self._dietaryReqs[category]['max'], \
                                  category) 


    #
    # SolveModel... optimize the model.  Note that Gurobi likes outputting a lot of text to the screen
    #
    def SolveModel (self):

        #print ('DietProblemSolver_Gurobi solvemodel')

        if self._model != None:
            # note that optimize does not return a value
            self._model.optimize ()


    #
    # PrintResults
    #
    def PrintResults (self):

        #print ('DietProblemSolver_Gurobi printresults')

        if self._model.status == GRB.OPTIMAL:

            print ()

            modelVars = self._model.getVars ()

            # Display the amounts to purchase of each food.
            print ('Foods to Buy: ')
            totalCost = 0
            for var in modelVars:
                if var.varName in self._foodNames and var.x > 0.0001:
                    totalCost += var.x * self._foodCosts [var.varName]["unitCost"]
                    print (f'{var.varName:25} --> {var.x:8.3f} units/servings   $ {(var.x * self._foodCosts [var.varName]["unitCost"]):.3f}')

            print ()
            print (f'Objective function results: {self._model.objVal}')
            print (f'Total daily cost: {totalCost:.2f}')
            print ()

            print ('Nutrient amounts... ')
            for nutrient in self._nutrientNames:
                total = 0
                for var in modelVars:
                    if var.varName in self._foodNames and var.x > 0.0001:
                        total += var.x * self._nutrientData [var.varName][nutrient]

                print (f'   {nutrient:15}  {total:7.2f}')

        else:  

            print ('No solution')


