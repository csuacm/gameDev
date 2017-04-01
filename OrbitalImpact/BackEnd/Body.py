import random
from random import *
class Body:
    def __init__(self, solSys, creationTier, rank, name="Noname Planet"):
        self.solSys=solSys
        self.name=name

        #Neighboring objects
        self.inferior=None
        self.inferior=None

        #dV distances to planets
        self.posteriorDistance=0
        self.inferiorDistance=0

        self.rank=rank

        self.orbitingEntities=[]


        #internal variables for handling transfer window costs and creation
        self.originalDistance = 0 #the original distance between self and the inferior planet
        self.distanceVariance = 0 #the absolute value that the distance will vary by
        self.activeVariance = 0 #the current amount of variance
        self.increasingVariance = False  #if the variance is increasing or decreasing
        self.orbitalVelocity = 0 #the amount of change in variance each turn (step)
        self.tier=creationTier

        if self.tier==1:
            self.createTier1()
        elif self.tier==2:
            self.createTier2()
        elif self.tier==3:
            self.createTier3()
        else:
            print("Tried to create a Body, but did not recieve valid tier type. Expected 1,2,3")
            exit(5)

        if rank!=0:
            self.inferior=self.solSys.getBody(rank-1)
            self.inferior.setPosterior(self)
            self.inferior.setPosteriorDistance(self.inferiorDistance)


    def createTier1(self):
        self.distanceVariance=randint(0,3)+1
        self.activeVariance=0
        self.increasingVariance=choice([True,False])

        self.orbitalVelocity=randint(0,2)

        if self.rank==0:
            self.inferiorDistance=0
        else:
            self.inferiorDistance=randint(0,5)+13
        self.originalDisance=self.inferiorDistance


    def createTier2(self):
        self.distanceVariance=randint(0,4)+5
        self.activeVariance=0
        self.increasingVariance=choice([True,False])

        self.orbitalVelocity=randint(0,5)+6

        if self.rank==0:
            self.inferiorDistance=0
        else:
            self.inferiorDistance=randint(0,20)+31
        self.originalDisance=self.inferiorDistance

    def createTier3(self):
        self.distanceVariance=randint(0,8)+7
        self.activeVariance=0
        self.increasingVariance=choice([True,False])

        self.orbitalVelocity=randint(0,6)+11

        if self.rank==0:
            self.inferiorDistance=0
        else:
            self.inferiorDistance=randint(0,30)+61
        self.originalDisance=self.inferiorDistance

    def __str__(self):
        ret = "BODY "+self.name+"{ Rank: "+str(self.rank)+ " Tier: "+str(self.tier)+" Inferior Distance: "+str(self.inferiorDistance) + " Posterior Distance: "+str(self.posteriorDistance)
        ret= ret + " Orbital Variance: "+str(self.distanceVariance)+" Increasing Variance: "+str(self.increasingVariance)+" Active Variance: "+str(self.activeVariance)+" Orbital Velocity: "+str(self.orbitalVelocity)+"}"
        return ret

    
    def runTurn(self):
        if self.rank !=0:
            #Change the inferior distance by the orbital velocity +- bassed on increasingVariencce
            if self.increasingVariance:
                self.inferiorDistance = self.inferiorDistance+self.orbitalVelocity
            if not self.increasingVariance:
                self.inferiorDistance = self.inferiorDistance-self.orbitalVelocity

            #If at apoapsis, or periapsis, flip increasing
            if self.inferiorDistance > (self.originalDisance+self.distanceVariance):
                self.increasingVariance = False
            if self.inferiorDistance < (self.originalDisance-self.distanceVariance):
                self.increasingVariance = True
            #set the distance on the inferior planet
            self.inferior.setPosteriorDistance(self.inferiorDistance)

    def distanceTo(self, targetBody):
        if targetBody == self:
            return 0
        if targetBody.getRank()<self.rank:
            return self.distanceToInferior(targetBody)
        if targetBody.getRank()>self.rank:
            return self.distanceToPosterior(targetBody)

    def distanceToPosterior(self, targetBody):
        head = self
        dvSum = 0
        while head.getRank() < targetBody.getRank():
            dvSum += head.getPosteriorDistance()
            head = head.getPosterior()
        return dvSum

    def distanceToInferior(self, targetBody):
        head = self
        dvSum = 0
        while head.getRank() > targetBody.getRank():
            dvSum += head.getInferiorDistance()
            head = head.getInferior()
        return dvSum


    def setPosteriorDistance(self, distance):
        self.posteriorDistance=distance

    def setPosterior(self, outer):
        self.posterior=outer

    def addToOrbit(self, other):
        self.orbitingEntities.append(other)

    def removeFromOrbit(self, other):
        self.orbitingEntities.remove(other)

    def getName(self):
        return self.name

    def getPosterior(self):
        if self.rank == len(self.solSys)-1:
            return self
        return self.posterior
    def getPosteriorDistance(self):
        return self.posteriorDistance

    def getInferior(self):
        if self.rank == 0:
            return self
        return self.inferior
    def getInferiorDistance(self):
        return self.inferiorDistance
    def getRank(self):
        return self.rank