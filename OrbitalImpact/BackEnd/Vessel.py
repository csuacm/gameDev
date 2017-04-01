import math

from GUI import ScreenText
from GUI import PlanetButton
from GUI import Button


class Vessel:
    def __init__(self, BE, name):
        self.name = name
        self.BE = BE
        self.ChoseStart() #Get the starting planet
        self.vesselData=ScreenText(self.BE.getBackPanel(),15,2,"No Planet Data")

    def completeInit(self):
        #Setting up the navigation pane
        self.navData = ScreenText(self.BE.getBackPanel(), 15, 7, "")
        self.targetPlanet = self.planet
        self.navPlanet = self.planet
        self.navInfButton = Button(self.BE.getBackPanel(),15,9.5,self.navInfEvent)
        self.navinfMessage = ScreenText(self.BE.getBackPanel(),15,11, "Inf")
        self.navSelButton = Button(self.BE.getBackPanel(),16,9.5,self.navSelEvent)
        self.navSelMessage = ScreenText(self.BE.getBackPanel(),16,11, "Sel")
        self.navPostButton = Button(self.BE.getBackPanel(),17,9.5,self.navPostEvent)
        self.navPostMessage = ScreenText(self.BE.getBackPanel(), 17, 11, "Pos")

        self.dV = 45  # In the future this will come from some combination of subsystems
        self.jumpTurns = 0
        self.displayVesselInfo()

    #Sets up GUI for users to select starting planet
    def ChoseStart(self):
        self.message = ScreenText(self.BE.getBackPanel(),0,.5,"Select a Starting Planet")
        self.pButtons = []
        for i in range (0, len(self.BE.getSolarSystem()),1):
            self.pButtons.append(PlanetButton(self.BE.getBackPanel(),i,1,self.selectedPlanet))
    #Gets Event handler for the clicked planet
    def selectedPlanet(self, buttonClicked):
        for i in range(0, len(self.pButtons), 1):
            if self.pButtons[i] == buttonClicked:
                self.clearStart(i)
                return
    #Clears the starting UI
    def clearStart(self, planetIndex):
        self.message.remove()
        self.planet=self.BE.getSolarSystem()[planetIndex]
        self.planet.addToOrbit(self)
        for p in self.pButtons:
            p.remove()
            self.completeInit()

    #Shows the current vessel data
    def displayVesselInfo(self):
        data = "Vessel Data:\n"
        data += "Name: "+str(self.name)+"\n"
        data += "Location: "+self.planet.getName()+"\n"
        data += "Target: "+self.targetPlanet.getName()+"\n"
        data += "Dv: "+str(self.dV)+"\n"
        data += "Turns to transfer "+str(self.jumpTurns)
        self.vesselData.updateText(data)

    #Complete navigation
    def displayNavigation(self):
        navDataText = "NAV Data\n"
        navDataText += "Selected Target: "+self.navPlanet.getName()+"\n"
        navDataText += "Dv To Target: "+str(self.planet.distanceTo(self.navPlanet))+"\n"
        self.navData.updateText(navDataText)

    def navInfEvent(self, button):
        self.navPlanet = self.navPlanet.getInferior()
        self.displayNavigation()

    def navPostEvent(self, button):
        self.navPlanet = self.navPlanet.getPosterior()
        self.displayNavigation()

    def navSelEvent(self, button):
        self.targetPlanet = self.navPlanet
        self.jumpTurns = self.planet.distanceTo(self.targetPlanet)/self.dV
        math.floor(self.jumpTurns)
        self.displayNavigation()
        self.displayVesselInfo()

    def runTurn(self):
        if self.targetPlanet != self.planet:
            if self.jumpTurns == 0:
                self.planet.removeFromOrbit(self)
                self.planet = self.targetPlanet
                self.planet.addToOrbit(self)
            else:
                self.jumpTurns = self.jumpTurns - 1
        self.displayVesselInfo()
        self.displayNavigation()

