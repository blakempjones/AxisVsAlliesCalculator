import tkinter as tk
from numpy import random
from numpy import mean
from math import floor

import numpy as np
import seaborn as sns
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rc
from matplotlib.figure import Figure
from matplotlib import pyplot
from tkinter import font

class Player:
    '''
    Class to handle player data. Two instances are created (attacker and
    defender). Creates the UI for associated with each and tracks the respective
    unit numbers. Contains member functions to facilitate combat rounds.
    '''
    # Class wide variables giving the attacking value in order of increasing 
    # unit cost [infantry, artillery, tank, sub, destroyer, fighter, bomber,
    # cruiser, aircraft carrier, battleship]
    attackingVals = [1, 2, 3, 2, 2, 3, 4, 3, 1, 4]
    defendingVals = [2, 2, 3, 1, 2, 4, 1, 3, 2, 4]
    costVals = [3, 4, 6, 6, 8, 10, 12, 12, 14, 20]
    
    def __init__(self, parent: tk.Frame, allyTeam: bool):
        """
        Parameters
        ----------
        parent : tk.Frame
            TKinter root frame.
        allyTeam : bool
            Used to point to correct image folder for unit resources.
        """ 
        # Points to image folder
        self.team = "ALLIES" if allyTeam else "AXIS"
        self.imageFolder =  r"Images\\" + self.team + "\\" 
        
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
        
        # Label for the attacker/defender with an underline
        self.teamLabel =  tk.Label(frame, text = "Attacker" if allyTeam else "Defender", font = "TkFixedFont 42")
        underline = font.Font(self.teamLabel, self.teamLabel.cget("font"))
        underline.configure(underline=True)
        self.teamLabel.configure(font=underline)
        self.teamLabel.grid(row=1, column=1)
        
        # Add/Subtract buttons of each unit type (left click / right click)
        self.infantryBtn = UnitButtonAndCounter(frame, self.imageFolder + "Infantry.png", 2, self, 'infantry', allyTeam)
        self.artilleryBtn = UnitButtonAndCounter(frame, self.imageFolder + "Artillery.png", 3, self, 'artillery', allyTeam)
        self.tankBtn = UnitButtonAndCounter(frame, self.imageFolder + "Tank.png", 4, self, 'tank', allyTeam)
        self.fighterBtn = UnitButtonAndCounter(frame, self.imageFolder + "Fighter.png", 5, self, 'fighter', allyTeam)
        self.bomberBtn = UnitButtonAndCounter(frame, self.imageFolder + "Bomber.png", 6, self, 'bomber', allyTeam)
        self.subBtn = UnitButtonAndCounter(frame, self.imageFolder + "Submarine.png", 7, self, 'sub', allyTeam)
        self.destroyerBtn = UnitButtonAndCounter(frame, self.imageFolder + "Destroyer.png", 8, self, 'destroyer', allyTeam)
        self.cruiserBtn = UnitButtonAndCounter(frame, self.imageFolder + "Cruiser.png", 9, self, 'cruiser', allyTeam)
        self.carrierBtn = UnitButtonAndCounter(frame, self.imageFolder + "Carrier.png", 10, self, 'carrier', allyTeam)
        self.battleshipBtn = UnitButtonAndCounter(frame, self.imageFolder + "Battleship.png", 11, self, 'battleship', allyTeam)
        #---------------------------------------------------------------------#
        
        
    def getUnitArray(self) -> [int]:
        """
        Returns
        -------
        [int]
            An array with the number of units of each type in order of increasing
            cost. 
            [infantry, artillery, tank, sub, destroyer, fighter, bomber, 
            cruiser, aircraft carrier, battleship]
        """
        # Returns list of unit amounts in order of unit cost
        return [self.infantry, self.artillery, self.tank, self.sub, \
                self.destroyer, self.fighter, self.bomber,  self.cruiser, \
                self.carrier, self.battleship]
            
            
    def setUnitArray(self, newUnitNums):
        """
        Parameters
        ----------
        newUnitNums : TYPE
            An array representing the number of units of each type in order of 
            increasing cost.
            [infantry, artillery, tank, sub, destroyer, fighter, bomber, 
            cruiser, aircraft carrier, battleship]
        """
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
        """
        Returns
        -------
        int
            Total number of units.
        """
        return sum(self.getUnitArray())
    
        
    def getCostOfUnits(self) -> int:
        """
        Returns
        -------
        int
            Total cost of all units.
        """
        return sum([numUnit * unitCost for numUnit, unitCost in zip(self.getUnitArray(), Player.costVals)])
    
        
    def getHits(self, attacking: bool) -> int:
        """
        Parameters
        ----------
        attacking : bool
            Flag for attacking player.

        Returns
        -------
        int
            Number of successful hits for this round of combat.
        """
        
        # Gets the threshold values for
        hitValues = Player.attackingVals if attacking else Player.defendingVals
        
        unitArray = self.getUnitArray()
        
        # Has artillery and infantry and is attacking
        if (attacking and unitArray[0] > 0 and unitArray[1] > 0):
            
            # Count the infantry as artillery for the number of artillery units 
            # present (infantry-artillery support bonus)
            numInf = unitArray[0]
            unitArray[0] -= min(unitArray[1], unitArray[0])
            unitArray[1] += min(unitArray[1], numInf)
         
        # Calculates the total number of successful "rolls" for each unit type 
        # and then sums them to get the total hits.
        return sum([sum([1 if i else 0 for i in random.randint(1,7,size=numUnit) <= hitVal]) for numUnit, hitVal in zip(unitArray, hitValues)])
                    
        
    def handleHits(self, numHits: int):        
        """
        Parameters
        ----------
        numHits : int
            Total number hits to assign to units.
        """
        # Battleships can take two hits, if one hasn't been hit yet. Use that one
        while (self.battleshipHits < self.battleship):
            
            numHits -= 1
            
            self.battleshipHits += 1
            
        unitArray = self.getUnitArray()
        
        # Assign hits to lowest cost units first by iterating through array
        for i, unitNum in enumerate(unitArray):
            
            # Units of this type exists
            if (unitNum > 0):
                # If more units of this type than hits, subtract all hits from 
                # this unit. Otherwise, subtract this unit down to zero and 
                # move onto the next
                diff = unitNum if numHits >= unitNum else numHits
                numHits -= diff
                unitArray[i] -= diff
            
            # Done hits
            if (numHits == 0):
                break
        
        self.setUnitArray(unitArray)
            
        
class UnitButtonAndCounter:
    '''
    Class to handle the unit button and counter display and functionality. 
    Receives a references to a player upon initialization.
    '''
    
    def __init__(self, parent: tk.Frame, photoPath: str, row: int, player, unitName, allyTeam: bool):
        """
        Parameters
        ----------
        parent : tk.Frame
            Tkinter root frame.
        photoPath : str
            Path to folder containing unit images.
        row : int
            Row of the Tkinter grid.
        player : TYPE
            Player object that the buttons and counters are associated with.
        unitName : TYPE
            Unit type.
        allyTeam : bool
            Flag for allies or axis team.
        """
        # Frame holder
        frame = tk.Frame(parent)
        frame.grid(row = row, column = 1)#, sticky = "ew")
        
        # GUI components for the unit button and amount label
        self.buttonPhoto = tk.PhotoImage(file=photoPath)
        self.unitCount = tk.Label(frame, text = "0", font = "TkFixedFont 42")
        self.unitCount.pack(side = tk.RIGHT if allyTeam else tk.LEFT)
        self.button = tk.Button(frame, image = self.buttonPhoto)#.pack()
        self.button.pack(side = tk.LEFT if allyTeam else tk.RIGHT)#pack(side=tk.TOP)
        
        def incrementUnit(e):
            """
            Parameters
            ----------
            e : TYPE
                Increase unit event.
            """
            numUnit = getattr(player, unitName) + 1
            setattr(player,unitName, numUnit)
            self.unitCount.config(text = str(numUnit))
        
        def decrementUnit(e):
            """
            Parameters
            ----------
            e : TYPE
                Decrease unit event.
            """
            # Manual implementation of button animation
            self.button.config(relief = tk.SUNKEN)
            numUnit = getattr(player, unitName)
            numUnit = 0 if numUnit <= 1 else numUnit - 1
            setattr(player,unitName, numUnit)          
            self.button.after(120, lambda: self.button.config(relief=tk.RAISED))
            self.unitCount.config(text = str(numUnit))
            
        # Binding of unit buttons to left (1) and right (3) clicks
        self.button.bind('<Button-1>', incrementUnit)
        self.button.bind('<Button-3>', decrementUnit)
        
class Results:
    '''
    Class to handle the calculation of outcome probabilities as well as their 
    respective display.
    '''
    # Tracked stats field names
    ATT_WIN_PROB = 'attackerWinProb'
    DEF_WIN_PROB = 'defenderWinProb'
    DRAW_PROB = 'drawProb'
    ATT_SURVIVE_COST = 'attackSurvivesCost'
    DEF_SURVIVE_COST = 'defenseSurvivesCost'
    MEAN_ATT_SURVIVES = 'meanAttackSurvives'
    MEAN_DEF_SURVIVES = 'meanDefenseSurvives'
    NUM_ATT_SURVIVORS = 'numAttackSurvivors'
    NUM_DEF_SURVIVORS = 'numDefenseSurvivors'
    
    def __init__(self, parent, attacker: Player, defender: Player):
        """
        Parameters
        ----------
        parent : TYPE
            Tkinter root frame.
        attacker : Player
            Attacking player (left side of GUI).
        defender : Player
            Defending player (right side).
        """
        # Group frame
        frame = tk.Frame(parent)
        frame.grid(row=1, column=2)
        frame.grid_rowconfigure(2,weight=1)
        
        # Holds references to the armies
        self.attacker = attacker
        self.defender = defender
        
        # Initializes the stats holder
        self.resultsDict = {
            Results.ATT_WIN_PROB: 0,
            Results.DEF_WIN_PROB: 0,
            Results.DRAW_PROB: 0,
            Results.ATT_SURVIVE_COST: [],
            Results.DEF_SURVIVE_COST: [],
            Results.MEAN_ATT_SURVIVES: 0,
            Results.MEAN_DEF_SURVIVES: 0,
            Results.NUM_ATT_SURVIVORS: [],
            Results.NUM_DEF_SURVIVORS: []
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
        """
        Parameters
        ----------
        e : TYPE
            Click event.
        """
        # Calculates and displays new statistics
        self.redrawGraph()
        
        # Updates probability labels        
        self.attackerProbLabel.config(text=str(self.resultsDict[Results.ATT_WIN_PROB]) + "%", fg = 'green' if self.resultsDict[Results.ATT_WIN_PROB] > 50 else 'red')
        self.defenderProbLabel.config(text=str(self.resultsDict[Results.DEF_WIN_PROB]) + "%", fg = 'green' if self.resultsDict[Results.DEF_WIN_PROB] > 50 else 'red')
        self.drawProbLabel.config(text=str(self.resultsDict[Results.DRAW_PROB]) + "%")
                
        
    def graphCostResults(self) -> Figure:
        """
        Returns
        -------
        Figure
            Graph of the number of surviving units for each team.
        """
        # Makes matplotlib figure, plots the two histograms on the axes and returns the figure for canvas display
        figure = Figure()
        # Matches Tkinter gray background
        figure.set_facecolor((0.94118, 0.94118, 0.92941))
        # Prevents the axis labels from getting cut-off
        figure.subplots_adjust(left=0.2, bottom=0.15)
        ax = figure.subplots()
        ax.set(xlabel="Number of surviving units", ylabel="Probability")
        sns.distplot(self.resultsDict[Results.NUM_ATT_SURVIVORS], norm_hist=True, hist=False, kde=True, ax=ax)
        sns.distplot(self.resultsDict[Results.NUM_DEF_SURVIVORS], norm_hist=True, hist=False, kde=True, ax=ax)
        return figure
    
    
    def redrawGraph(self):       
        # Calculates battle statistics for the current unit numbers
        self.resultsDict = self.CalculateBattle()
        
        # Redraws the graph
        self.canvas.figure = self.graphCostResults()
        self.canvas.draw()
        

    def CalculateBattle(self) -> {}:
        """
        Returns
        -------
        Dict
            Dictionary of statistics calculate for the battle.
        """
        # Stats to be calculated        
        numAttackerWins = 0        
        numDefenderWins = 0        
        numDraws = 0        
        attackSurvives = []        
        attackSurvivesCost = []        
        defenseSurvives = []        
        defenseSurvivesCost = []
        numAttackSurvivors = []
        numDefenseSurvivors = []
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
            
            # Attacker wins
            if (self.attacker.numUnits() > 0): 
                numAttackerWins += 1
                attackSurvives.append(attacker.getUnitArray())
                attackSurvivesCost.append(attacker.getCostOfUnits())
                numAttackSurvivors.append(attacker.numUnits())
            
            # Defender wins
            elif (self.defender.numUnits() > 0): 
                numDefenderWins += 1
                defenseSurvives.append(defender.getUnitArray())
                defenseSurvivesCost.append(defender.getCostOfUnits())
                numDefenseSurvivors.append(defender.numUnits())
            # Both armies lost all units 
            else:
            
                numDraws += 1
                
            # Restore units to what they were pre-battle for next iteration
            self.attacker.setUnitArray(attackerTroops)
            self.defender.setUnitArray(defenderTroops)
        
        # Output is used to overwrite self.resultsDict
        return {
            Results.ATT_WIN_PROB: floor(numAttackerWins * 100 / numIterations),
            Results.DEF_WIN_PROB: floor(numDefenderWins * 100 / numIterations),
            Results.DRAW_PROB: floor(numDraws * 100 / numIterations),
            Results.ATT_SURVIVE_COST: attackSurvivesCost,
            Results.DEF_SURVIVE_COST: defenseSurvivesCost,
            Results.MEAN_ATT_SURVIVES:  mean(attackSurvives,axis=0),
            Results.MEAN_DEF_SURVIVES: mean(defenseSurvives,axis=0),
            Results.NUM_ATT_SURVIVORS: numAttackSurvivors,
            Results.NUM_DEF_SURVIVORS: numDefenseSurvivors
            }
 
# --------------------------------- Main -------------------------------------#

# Plotting configurations
sns.set(font_scale=1.8, rc=rc('font', weight='bold'))
pyplot.rcParams["font.weight"] = "bold"
pyplot.rcParams["axes.labelweight"] = "bold"

# Tkinter root frame
root = tk.Tk()
root.resizable(0, 0) 

# Initialize players and GUI
attacker = Player(root, True)
defender = Player(root, False)
results = Results(root, attacker, defender)

root.mainloop()