from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import  ShowBase
from panda3d.core import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
import sys
from BackEnd import BackEngine

#Grids go from (0,0) at (1.23,.67) to (42,23) at(-1.26,-.71) with a grid width of .06


class MainPanel (ShowBase):
    def __init__(self):
        #This is essantially the main, the Panda3d calls

        #variables for laying out GUI elements
        self.STEP=.06
        self.TOP=.67
        self.LEFT=1.23

        #Initialize the window
        loadPrcFileData("","window-title Orbital Impact")
        loadPrcFileData("", "fullscreen 0")
        loadPrcFileData("", "win-size 1280 720")
        ShowBase.__init__(self)

        #Initialize the actual GUI
        self.elementList=[] #a list of lists containing the GUI element and it's Panda3d node
        self.setUpCamNode()
        self.loadPanel()
        self.setupLights()
        self.BE=BackEngine(self)

    def setUpCamNode(self):
        #set cam position and orientation
        self.cam.setPos(0,-27,0)
        self.cam.setHpr(0,0,0)

        #Code for event detection
        self.picker= CollisionTraverser()
        self.queue = CollisionHandlerQueue()

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.cam.attachNewNode(self.pickerNode)

        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())

        self.pickerRay = CollisionRay()

        self.pickerNode.addSolid(self.pickerRay)

        self.picker.addCollider(self.pickerNP, self.queue)

        # this holds the object that has been picked
        self.pickedObj = None

        self.accept('mouse1', self.onClick)

    def loadPanel(self):
        #Enable shadows
        self.render.setShaderAuto()

        #Load the back panel that all elements will be attached to and orient it
        self.backPanel = self.loader.loadModel("GDAT/Meshes/BackPanel.egg")
        self.backPanel.setPos(0,1,0)
        self.backPanel.setScale(10)
        self.backPanel.setHpr(90,0,0)
        self.backPanel.reparentTo(self.render)
        self.backPanel.setShaderAuto() #Enable shadows on

        #load the sky_box This shouldn't ever be visible, but if it is, we maintain emersion
        self.skyBox = self.loader.loadModel("GDAT/Meshes/solar_sky_sphere.egg.pz")
        self.skyBox.reparentTo(self.render)
        self.skyBox.setScale(100)
        self.skyTexture = self.loader.loadTexture("GDAT/Textures/img2.jpg")#use img 2 or img3
        self.skyBox.setTexture(self.skyTexture,1)

        #self.grid() #For debug and showing gridding.

    def setupLights(self):
        #In general this method places a single spaotlight behind the camera, shinning at the panel

        #Create a holder node for debug, and finding the spothlight
        self.primaryLightHolder=self.loader.loadModel("GDAT/Meshes/planet_sphere.egg.pz")
        self.primaryLightHolder.setPos(0,-70,50)
        self.primaryLightHolder.setScale(1)
        self.primaryLightHolder.reparentTo(self.render)

        #load the light itself
        self.mLight = Spotlight("Light")
        self.mLight.setShadowCaster(True)
        lens = PerspectiveLens()
        self.mLight.setLens(lens)
        self.mLightPointer=self.primaryLightHolder.attachNewNode(self.mLight)
        self.mLightPointer.lookAt(self.backPanel)
        self.render.setLight(self.mLightPointer)

    def grid(self):
        step = .06
        for t in range(0,42):
            tNode=self.loader.loadModel("GDAT/Meshes/planet_sphere.egg.pz")
            tNode.setTexture(self.loader.loadTexture("GDAT/Textures/hubble_friday_07012016.jpg"))
            tNode.setScale(.03)
            x=1.23-(t*step)
            y=.67
            tNode.reparentTo(self.backPanel)
            tNode.setPos(-.13,x,y)
            tNode.setShaderAuto()

        for v in range (0,23):
            tNode = self.loader.loadModel("GDAT/Meshes/planet_sphere.egg.pz")
            tNode.setTexture(self.loader.loadTexture("GDAT/Textures/hubble_friday_07012016.jpg"))
            tNode.setScale(.03)
            x = 1.23
            y = .67-(v*step)
            tNode.reparentTo(self.backPanel)
            tNode.setPos(-.13, x, y)
            tNode.setShaderAuto()

    def getObjectHit(self, mpos):  # mpos is the position of the mouse on the screen
        self.pickedObj = None  # be sure to reset this
        self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
        self.picker.traverse(self.render)
        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            self.pickedObj = self.queue.getEntry(0).getIntoNodePath()
            parent = self.pickedObj.getParent()
            self.pickedObj = None
            while parent != self.render:
                if parent.getTag('pickable') == 'true':
                    self.pickedObj = parent
                    return parent
                else:
                    parent = parent.getParent()
        return None

    def makePickable(self, obj):
        obj.setTag('pickable', 'true')

    def onClick(self):
        #called when an object is clicked. selfpickedObj is the clicked object
        self.getObjectHit(self.mouseWatcherNode.getMouse())
        if self.pickedObj != None:
            self.handleEvent(self.pickedObj)

    def handleEvent(self, picked):
        for couple in self.elementList:#find the node that was clicked in the list of elements
            if couple[0] == picked:#once found call the elements onClickFunc
                couple[1].wasClicked()
        return

    def XgridToLoc(self, xgrid):
        #converts locations given by back-end to their actual locations
        return self.LEFT-(xgrid*self.STEP)

    def YgridToLoc(self, ygrid):
        return self.TOP-(ygrid*self.STEP)

    #Adds node to elemet list so it becomes clickable
    def addToElementList(self, nodeElement):
        self.elementList.append(nodeElement)

    #Returns the Panel node
    def getPanelNode(self):
        return self.backPanel

app=MainPanel()
app.run()