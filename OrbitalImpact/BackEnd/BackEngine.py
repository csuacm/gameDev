from SolarSystem import SolarSystem
from Vessel import Vessel
from GUI import Button
from GUI import ScreenText
from GUI import PlanetButton


class BackEngine:
    #Main entry point for all back-end logic of the game, holding the vessels, and the solar systems, and controling all game events
    def __init__(self, backPanel):
        self.BP = backPanel
        self.turn = 0
        self.solSystem = SolarSystem(self,9)
        self.activeVessel = Vessel(self, "Endurance")
        ScreenText(self.BP,41,0,"Next\nTurn")
        self.turnButton = Button(self.BP,41,1,self.runTurn)

    def runTurn(self, turnButton):
        self.solSystem.runTurn()
        self.activeVessel.runTurn()
        self.turn = self.turn + 1

    #returns the solar system
    def getSolarSystem(self):
        return self.solSystem

    #returns the MainPannel object
    def getBackPanel(self):
        return self.BP
