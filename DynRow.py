
import glob
import os
import dynrow_args

from UI.PyGameUi import PyGameUi
from Boats.BoatConcept2 import BoatConcept2
from Boats.BoatBoomerang import BoatBoomerang
from Boats.BoatGhost import BoatGhost
from Logic.Playground import Playground

# get erg data from either PyRow or pyerg
if not dynrow_args.args.pyerg:
    from PyRow.ErgStats import ErgStats
else:
    from pyerg_adapter.ErgStats import ErgStats


DELTAT = 16  # run with ~60FPS

#get newest workout file
#do this before the Playground gets created (thus creating a new Ghostfile)
ghostFiles = glob.glob('*.db')
if len(ghostFiles) > 0:
    newestGhost = max(ghostFiles, key=os.path.getctime)
else:
    newestGhost = ""

playground = Playground()  # the playground is a class which holds all the information (all the boats etc)
ui = PyGameUi() # the UI which will display the playground on a graphical interface


def gameLoop():
    #check if the workout is active
    isWorkoutActive = ErgStats.isWorkoutActive()
    if not isWorkoutActive:
        ErgStats.resetStatistics()
        playground.reset()
    else:
        #update the ergometer data
        ErgStats.update()

    playground.update(ErgStats.time)
    ui.update(playground)

    #display the message after the UI has been rendered
    if not isWorkoutActive:
        ui.showMessage("Please start rowing...")



def main():
    # init the player boat
    player = BoatConcept2(dynrow_args.args.name)
    playground.setPlayerBoat(player)

    #init the AI boats
    playground.addBoat(BoatBoomerang("Armin", 130, 20, 20))
    playground.addBoat(BoatBoomerang("Bahne", 135, 22, 20))

    if not newestGhost == "":
        playground.addBoat(BoatGhost("Ghost", newestGhost))

    # Init the Concept2
    ErgStats.connectToErg()

    #init the UI, register the GameLoop and run it
    ui.registerCallback(gameLoop)
    ui.setCycleTime(DELTAT)
    ui.run()

if __name__ == "__main__":
    main()

