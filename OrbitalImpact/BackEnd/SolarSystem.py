from Body import Body



class SolarSystem:
    #Models the solar system by a list of Body objects

    def __init__(self,backEngine, size):
        self.BE=backEngine
        self.celestials=[]
        self.size = size

        for i in range (0,size,1):
            self.celestials.append(Body(self,self.computeTier(i),i,("Planet: "+str(i))))

    def __str__(self):
        s=""
        for planet in self.celestials:
            s=s+str(planet)+"\n"
        return s
    def __len__(self):
        return len(self.celestials)
    def __getitem__(self, item):
        return self.celestials[item]

    def getBody(self, index):
        return self.celestials[index]

    def runTurn(self):
        for planet in self.celestials:
            planet.runTurn()

    #computes the tier of each planet bassed on it's index reletive to the solarsystem size
    def computeTier(self, i):
        if(i>(self.size/(3.0)*2.0)):
            return 3
        if (i>(self.size/(3.0))):
            return 2
        else:
            return 1