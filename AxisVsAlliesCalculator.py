import tkinter as tk
from numpy import random
from numpy import mean
from math import floor

import numpy as np
import seaborn as sns
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot

class Player:
    
    # Class wide variables giving the attacking value in order of increasing 
    # unit cost [infantry, artillery, tank, sub, destroyer, fighter, bomber,
    # cruiser, aircraft carrier, battleship]
    attackingVals = [1, 2, 3, 3, 4, 2, 2, 3, 1, 4]
    defendingVals = [2, 2, 3, 4, 1, 1, 2, 3, 2, 4]
    costVals = [3, 4, 6, 6, 8, 10, 12, 12, 14, 20]
    
    def __init__(self, parent: tk.Frame, allyTeam: bool):
        
        self.team = "ALLIES" if allyTeam else "AXIS"
        
        self.imageFolder = r"C:\\Users\\TheMainframe\\Documents\\Code\\Personal\\AxisVsAlliesCalculator\\Images\\" + self.team + "\\"
        
        # Unit type counts
        self.infantry = 0
        self.artillery = 0
        self.tank = 0
        self.sub = 0
        self.destroyer = 0
        self.fighter = 0
        self.bomber = 0
        self.cruiser = 0
        self.carrier = 0
        self.battleship = 0
        
        # Tracks number of battleship hits to allow for them to take two hits
        self.battleshipHits = 0
        
        # Class holder frame and placement in root
        frame = tk.Frame(parent)
        frame.grid(row = 1, column = 1 if allyTeam else 3, sticky = "nsew")
        
        # Add/Subtract buttons of each unit type (left click / right click)
        self.infantryBtn = UnitButtonAndCounter(frame, self.imageFolder + "Infantry.png", 1, self, 'infantry', allyTeam)
        self.artilleryBtn = UnitButtonAndCounter(frame, self.imageFolder + "Artillery.png", 2, self, 'artillery', allyTeam)
        self.tankBtn = UnitButtonAndCounter(frame, self.imageFolder + "Tank.png", 3, self, 'tank', allyTeam)
        self.fighterBtn = UnitButtonAndCounter(frame, self.imageFolder + "Fighter.png", 4, self, 'fighter', allyTeam)
        self.bomberBtn = UnitButtonAndCounter(frame, self.imageFolder + "Bomber.png", 5, self, 'bomber', allyTeam)
        self.subBtn = UnitButtonAndCounter(frame, self.imageFolder + "Submarine.png", 6, self, 'sub', allyTeam)
        self.destroyerBtn = UnitButtonAndCounter(frame, self.imageFolder + "Destroyer.png", 7, self, 'destroyer', allyTeam)
        self.cruiserBtn = UnitButtonAndCounter(frame, self.imageFolder + "Cruiser.png", 8, self, 'cruiser', allyTeam)
        self.carrierBtn = UnitButtonAndCounter(frame, self.imageFolder + "Carrier.png", 9, self, 'carrier', allyTeam)
        self.battleshipBtn = UnitButtonAndCounter(frame, self.imageFolder + "Battleship.png", 10, self, 'battleship', allyTeam)
        #---------------------------------------------------------------------#
        
    def getUnitArray(self) -> [int]:
        
        # Returns list of unit amounts in order of unit cost
        return [self.infantry, self.artillery, self.tank, self.sub, \
                self.destroyer, self.fighter, self.bomber,  self.cruiser, \
                self.carrier, self.battleship]
            
    def setUnitArray(self, newUnitNums):
        
        # Sets unit amounts given array of new amounts in order of unit cost
        self.infantry = newUnitNums[0]
        self.artillery = newUnitNums[1]
        self.tank = newUnitNums[2]
        self.sub = newUnitNums[3]
        self.destroyer = newUnitNums[4]
        self.fighter = newUnitNums[5]
        self.bomber = newUnitNums[6]
        self.cruiser = newUnitNums[7]
        self.carrier = newUnitNums[8]
        self.battleship = newUnitNums[9]
    
    def numUnits(self) -> int:
        
        return sum(self.getUnitArray())
            
    def getUnitHitArray(self, attacking: bool) -> [tuple]:
        
        unitArray = self.getUnitArray()
        
    def getCostOfUnits(self) -> int:
        
        return sum([numUnit * unitCost for numUnit, unitCost in zip(self.getUnitArray(), Player.costVals)])
        
    def getHits(self, attacking: bool) -> int:
        
        hitValues = Player.attackingVals if attacking else Player.defendingVals
        
        unitArray = self.getUnitArray()
                
        return sum([sum([1 if i else 0 for i in random.randint(1,7,size=numUnit) <= hitVal]) for numUnit, hitVal in zip(unitArray, hitValues)])
                    
        
    def handleHits(self, numHits: int):        
        # Battleships can take two hits, if one hasn't been hit yet. Use that one
        while (self.battleshipHits < self.battleship):
            
            numHits -= 1
            
            self.battleshipHits += 1
            
        unitArray = self.getUnitArray()

        for i, unitNum in enumerate(unitArray):
            
            if (unitNum > 0):
                
                diff = unitNum if numHits >= unitNum else numHits
                
                numHits -= diff
                
                unitArray[i] -= diff
            
            if (numHits == 0):
                
                break
        
        self.setUnitArray(unitArray)
            
        
class UnitButtonAndCounter:
    
    def __init__(self, parent: tk.Frame, photoPath: str, row: int, player, unitName, allyTeam: bool):
        
        frame = tk.Frame(parent)
        frame.grid(row = row, column = 1)#, sticky = "ew")
                        
        self.buttonPhoto = tk.PhotoImage(file=photoPath)
        
        self.unitCount = tk.Label(frame, text = "0", font = "TkFixedFont 42")
        
        self.unitCount.pack(side = tk.RIGHT if allyTeam else tk.LEFT)
        
        self.button = tk.Button(frame, image = self.buttonPhoto)#.pack()
                
        self.button.pack(side = tk.LEFT if allyTeam else tk.RIGHT)#pack(side=tk.TOP)
        
        def incrementUnit(e):
            
            numUnit = getattr(player, unitName) + 1
            setattr(player,unitName, numUnit)
            self.unitCount.config(text = str(numUnit))
        
        def decrementUnit(e):
            
            self.button.config(relief = tk.SUNKEN)
            numUnit = getattr(player, unitName)
            numUnit = 0 if numUnit <= 1 else numUnit - 1
            setattr(player,unitName, numUnit)          
            self.button.after(120, lambda: self.button.config(relief=tk.RAISED))
            self.unitCount.config(text = str(numUnit))
            
                              
        self.button.bind('<Button-1>', incrementUnit)
        
        self.button.bind('<Button-3>', decrementUnit)
        
class Results:

    def __init__(self, parent, attacker: Player, defender: Player):
        
        # Group frame
        frame = tk.Frame(parent)
        frame.grid(row=1, column=2)
        
        # Holds references to the armies
        self.attacker = attacker
        self.defender = defender
        
        # Initializes the stats holder
        self.resultsDict = {
            'attackerWinProb': 0,
            'defenderWinProb': 0,
            'drawProb': 0,
            'attackSurvivesCost': [],
            'defenseSurvivesCost': [],
            'meanAttackSurvives': 0,
            'meanDefenseSurvives': 0
            }
        
        # Initializes the number of units graph
        initialFigure = self.graphCostResults()
        self.canvas = FigureCanvasTkAgg(initialFigure, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=1, columnspan=3)
        
        # Binds click events in the root widget to click handler (unfortunate
        # but without signalling, probably the best solution)
        parent.bind('<Button-1>', self.handleClick)
        parent.bind('<Button-3>', self.handleClick)
        
        # Win/loss probability display
        resultsTopFrame = tk.Frame(frame)
        # Attacker
        tk.Label(resultsTopFrame, text = "Attacker Win: ", font = "TkFixedFont 22").grid(row=1,column=1)
        self.attackerProbLabel = tk.Label(resultsTopFrame, text = "N/A", font = "TkFixedFont 22")
        self.attackerProbLabel.grid(row=1,column=2)        
        # Defender
        tk.Label(resultsTopFrame, text = "Defender Win: ", font = "TkFixedFont 22").grid(row=2,column=1)
        self.defenderProbLabel = tk.Label(resultsTopFrame, text = "N/A", font = "TkFixedFont 22")
        self.defenderProbLabel.grid(row=2,column=2)
        # Draw
        tk.Label(resultsTopFrame, text = "Draw: ", font = "TkFixedFont 22").grid(row=3,column=1)
        self.drawProbLabel = tk.Label(resultsTopFrame, text = "N/A", font = "TkFixedFont 22")
        self.drawProbLabel.grid(row=3,column=2)
        resultsTopFrame.grid(row=1,column=2)
        # -------------------------------------------------------------------#
        
        
    def handleClick(self, e):
        
        # Calculates and displays new statistics
        self.redrawGraph()
        
        # Updates probability labels        
        self.attackerProbLabel.config(text=str(self.resultsDict['attackerWinProb']) + "%", fg = 'green' if self.resultsDict['attackerWinProb'] > 50 else 'red')
        self.defenderProbLabel.config(text=str(self.resultsDict['defenderWinProb']) + "%", fg = 'green' if self.resultsDict['defenderWinProb'] > 50 else 'red')
        self.drawProbLabel.config(text=str(self.resultsDict['drawProb']) + "%")
                
        
    def graphCostResults(self) -> Figure:#, attackSurvivesCost, defenseSurvivesCost) -> Figure:
        
        # Makes matplotlib figure, plots the two histograms on the axes and returns the figure for canvas display
        figure = Figure()
        ax = figure.subplots()
        sns.distplot(self.resultsDict['attackSurvivesCost'], norm_hist=True, hist=False, kde=True, ax=ax)#kde=False, ax=ax) # # kde=False, ax=ax)
        sns.distplot(self.resultsDict['defenseSurvivesCost'], norm_hist=True, hist=False, kde=True, ax=ax)# kde=False, ax=ax)#hist=False, norm_hist=True, kde=True, ax=ax)
        return figure
    
    def redrawGraph(self):
        
        # Calculates battle statistics for the current unit numbers
        self.resultsDict = self.CalculateBattle()
        
        # Redraws the graph
        self.canvas.figure = self.graphCostResults()
        self.canvas.draw()

    def CalculateBattle(self) -> {}:#, attacker: Player, defender: Player) -> {}:
        
        # Stats to be calculated        
        numAttackerWins = 0        
        numDefenderWins = 0        
        numDraws = 0        
        attackSurvives = []        
        attackSurvivesCost = []        
        defenseSurvives = []        
        defenseSurvivesCost = []

        # Num simulations to run        
        numIterations = 300
        
        # Store the pre-battle troop amounts
        attackerTroops = attacker.getUnitArray().copy()
        defenderTroops = defender.getUnitArray().copy()
        
        # Simulation loop
        for i in range(numIterations):            
            
            # Battle loop
            while (attacker.numUnits() != 0 and defender.numUnits() != 0):
                
                # Attacker attacks
                attAttacks = self.attacker.getHits(True)
                
                # Defender attacks and remove hits from both
                self.attacker.handleHits(self.defender.getHits(False))
                self.defender.handleHits(attAttacks)
                
            if (self.attacker.numUnits() > 0): 
                numAttackerWins += 1
                attackSurvives.append(attacker.getUnitArray())
                attackSurvivesCost.append(attacker.getCostOfUnits())
            
            elif (self.defender.numUnits() > 0): 
                numDefenderWins += 1
                defenseSurvives.append(defender.getUnitArray())
                defenseSurvivesCost.append(defender.getCostOfUnits())
                
            else:
            
                numDraws += 1
                
            # Restore units to what they were pre-battle for next iteration
            self.attacker.setUnitArray(attackerTroops)
            self.defender.setUnitArray(defenderTroops)
        
        # Output is used to overwrite self.resultsDict
        return {
            'attackerWinProb': floor(numAttackerWins * 100 / numIterations),
            'defenderWinProb': floor(numDefenderWins * 100 / numIterations),
            'drawProb': floor(numDraws * 100 / numIterations),
            'attackSurvivesCost': attackSurvivesCost,
            'defenseSurvivesCost': defenseSurvivesCost,
            'meanAttackSurvives': mean(attackSurvives,axis=0),
            'meanDefenseSurvives': mean(defenseSurvives,axis=0)
            }


def displayAverageSurvival():
        
     pass
 

sns.set()  
root = tk.Tk()

attacker = Player(root, True)
defender = Player(root, False)
results = Results(root, attacker, defender)
#calcButton = tk.Button(root, text = "CALCULATE", font = "TkFixedFont 32", command = lambda: CalculateBattle(attacker, defender))
#calcButton.grid(row=1,column=2)

root.mainloop()