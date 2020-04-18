import tkinter as tk
from numpy import random
from numpy import mean

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
        
        self.battleshipHits = 0
        
        frame = tk.Frame(parent)
        frame.grid(row = 1, column = 1 if allyTeam else 3, sticky = "nsew")
        
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
        
    def getUnitArray(self) -> [int]:
        
        return [self.infantry, self.artillery, self.tank, self.sub, \
                self.destroyer, self.fighter, self.bomber,  self.cruiser, \
                self.carrier, self.battleship]
            
    def setUnitArray(self, newUnitNums):
        
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
            
            self.unitCount.config(text = str(numUnit))
            
            self.button.after(200, lambda: self.button.config(relief=tk.RAISED))
            
                              
        self.button.bind('<Button-1>', incrementUnit)
        
        self.button.bind('<Button-3>', decrementUnit)
        

def CalculateBattle(attacker: Player, defender: Player):
    
    numAttackerWins = 0
    
    numDefenderWins = 0
    
    attackSurvives = []
    
    attackSurvivesCost = []
    
    defenseSurvives = []
    
    defenseSurvivesCost = []
    
    numIterations = 100
    
    for i in range(numIterations):
        
        # Store the pre-battle troop amounts
        attackerTroops = attacker.getUnitArray()
        defenderTroops = defender.getUnitArray()
        
        # Battle loop
        while (attacker.numUnits() != 0 and defender.numUnits() != 0):
            
            # Attacker attacks
            attAttacks = attacker.getHits(True)
            
            # Defender attacks and remove hits from both
            attacker.handleHits(defender.getHits(False))
            defender.handleHits(attAttacks)
            
            # Check for ties?
            
            
        if (attacker.numUnits() > 0): 
            numAttackerWins += 1
            attackSurvives.append(attacker.getUnitArray())
            attackSurvivesCost.append(attacker.getCostOfUnits())
        
        else: 
            numDefenderWins += 1
            defenseSurvives.append(defender.getUnitArray())
            defenseSurvivesCost.append(defender.getCostOfUnits())
            
        # Restore units to what they were pre-battle for next iteration
        attacker.setUnitArray(attackerTroops)
        defender.setUnitArray(defenderTroops)
        
    
    print(numAttackerWins / numIterations)
    print(numDefenderWins / numIterations)
    
    print(mean(attackSurvives, axis = 0))
    print(mean(defenseSurvives, axis = 0))
    
    print(mean(attackSurvivesCost))
    print(mean(defenseSurvivesCost))
    
    
    
        
     
        
root = tk.Tk()

attacker = Player(root, True)
defender = Player(root, False)

calcButton = tk.Button(root, text = "CALCULATE", font = "TkFixedFont 32", command = lambda: CalculateBattle(attacker, defender))
calcButton.grid(row=1,column=2)

root.mainloop()