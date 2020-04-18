import tkinter as tk
from numpy import random
class Player:
    
    def __init__(self, parent: tk.Frame, allyTeam: bool):
        
        self.team = "ALLIES" if allyTeam else "AXIS"
        
        self.imageFolder = r"C:\\Users\\TheMainframe\\Documents\\Code\\Personal\\AxisVsAlliesCalculator\\Images\\" + self.team + "\\"
        
        self.infantry = 0
        self.artillery = 0
        self.tank = 0
        self.fighter = 0
        self.bomber = 0
        self.sub = 0
        self.destroyer = 0
        self.cruiser = 0
        self.carrier = 0
        self.battleship = 0
        
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
        
        def hasUnits(self) -> bool:
            
            return any([self.infantry, self.artillery, self.tank, self.fighter, \
                        self.bomber, self.sub, self.destroyer, self.cruiser, \
                        self.carrier, self.battleship])
                
        def numUnits(self) -> int:
            
            return sum([self.infantry, self.artillery, self.tank, self.fighter, \
                        self.bomber, self.sub, self.destroyer, self.cruiser, \
                        self.carrier, self.battleship])
                
        def getUnitHitArray(attacking: bool) -> [tuple]:
            
            pass
        
        def getHits(self, attacking) -> int:
            
            pass
        
        def handleHits(self, numHits: int):
            
            pass


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
    
    while (attacker.hasUnits() and defender.hasUnits()):
        
        # Attacker attacks
        #attAttacks = randint(1, 6, size=attacker.numUnits())
        attAttacks = attacker.getHits(True)
        
        # Defender attacks
        #defAttacks = randint(1, 6, size=defender.numUnits())
        # Remove hits from both
        attacker.handleHits(defender.getHits(False))
        defender.handleHits(attAttacks)
    
    pass
    
    
        
     
        
root = tk.Tk()

attacker = Player(root, True)
defender = Player(root, False)

calcButton = tk.Button(root, text = "CALCULATE", font = "TkFixedFont 32", command = lambda: CalculateBattle(ally, axis))
calcButton.grid(row=1,column=2)

root.mainloop()