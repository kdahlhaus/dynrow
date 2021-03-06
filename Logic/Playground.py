
from Storage.SQLiteStorage import SQLiteStorage

class Playground():
    def __init__(self):
        self.boats = []
        self.position = 0.0
        self.storage = SQLiteStorage() #needed to store the current workout to file (needed for ghosting)
        
    def getCurrentPosition(self):
        return self.position
        
    def addBoat(self, boat):
        self.boats.append(boat)
        
    def getBoats(self):
        return self.boats
        
    def getPlayerBoat(self):
        return self.playerBoat
        
    def setPlayerBoat(self, boat):
        self.playerBoat = boat

    def reset(self):
        for boat in self.boats:
            boat.reset()
        self.playerBoat.reset()

    def update(self, timeGone):
        #move all the bots
        for boat in self.boats:
            boat.move(timeGone)

        #move the player
        self.playerBoat.move(timeGone)

        #store the current state into the storage
        self.storage.storeState(timeGone)
