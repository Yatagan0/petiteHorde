
import random


toLog = []
def sparseLogs(name, toPrint):
    if name in toLog:
        print toPrint
    

class petitTerrain:
    def __init__(self, taille):
        self.taille = taille
        self.content =[["plaine"]*(2*taille + 1)]*(2*taille + 1)

        
consonnes_rares = "B.D.F.G.H.J.V.Qu.Ch.Pr.Cr.Sc"
consonnes_frequentes = "C.L.M.N.P.R.S.T.St.Tr"
consonnes = consonnes_frequentes.split('.')*2 + consonnes_rares.split('.')
voyelles_rares = "u.in.ai.ei.eu.ia.ui.io"
voyelles_frequentes = "a.e.i.o.on.ou.en.au"
voyelles = voyelles_frequentes.split('.')*2 + voyelles_rares.split('.')    
        
class petitHomme:
    def __init__(self, horde):
        self.horde = horde
        self.name = random.choice(consonnes)+random.choice(voyelles)+random.choice(consonnes)+random.choice(voyelles)
        if random.randint(0,1) ==0:
            self.name +=random.choice(consonnes)
            if random.randint(0,1) ==0:
                self.name +=random.choice(voyelles)
        #print self.name
        self.opinions = {}
        self.opinions[self.name]  = 1
        for p in self.horde.personnes.values():
            self.opinions[p.name]  = 1
            p.opinions[self.name] = 1
            
        self.age = 0
        self.sante = 1.
        self.forme = 1.
        
        self.action = "rester"
        self.group = None
        self.oldReserve = self.horde.reserve
        
    def update(self):
        self.age+= 1./52
        #~ print self.name
        self.averageOpinions()
        #~ print self.opinions
        
        self.resolveAction()

        self.selectNextAction()
        
    def resolveAction(self):
        
        if self.action == "cueillir":
            result = 0.6*(random.random()+random.random()) + 0.2
            #~ print "cueillette ", result
        elif self.action == "groupAction":
            result = self.group.resolveAction(self)
        else:
            result = 0.
            
        sparseLogs(self.name, self.name+ " brings from "+self.action+": "+str(result))
        #~ print self.name, " brings from ", self.action,": ",result
            
        if result >= 1:
            self.forme = 1.
            self.horde.reserve += result - 1.
            if self.action == "groupAction":
                self.horde.changeOpinion(self.name, (result - 1.)/2)
                self.opinions[self.name] +=  result/2
                self.horde.changeOpinion(self.group.leader.name, (result - 1.)/2)
                self.opinions[self.group.leader.name] +=  result/2
            else:
                
                self.horde.changeOpinion(self.name, result - 1.)
                self.opinions[self.name] +=  result 
            #changer opinion
        else:
            prendReserve = min(self.horde.reserve/len(self.horde.personnes.keys()), 1. - result)
            self.forme = result + prendReserve
            self.horde.reserve -= prendReserve 
            self.horde.changeOpinion(self.name, -prendReserve )
            self.opinions[self.name] -=  prendReserve
            
        
    def selectNextAction(self):
        hope = self.horde.getHope(self.name)
        sparseLogs(self.name, self.name+" hope "+str(hope))
        
        actions = ["cueillir", "rester", "groupAction"]
        self.action = random.choice(actions)
        if self.action == "groupAction":
            self.group = None
            for ga in self.horde.groupActivities:
                if ga.canJoin(self):
                    ga.join(self)
                    break
            if self.group is None:
                num = int(hope) +1
                if num > 1:
                    #~ sparseLogs(self.name,"creating group for "+str(num)+" people")
                    print self.name+"creating group for "+str(num)+" people"
                    ga = groupActivity(self, "chasse", {"people" : num})
                    self.horde.groupActivities.append(ga)
                    ga.join(self)
                else:
                    self.selectNextAction()
                    return
                
        sparseLogs(self.name,self.name+ ": chosen action "+self.action)
        #~ print self.name, ": chosen action ",self.action
        
        
        
    def averageOpinions(self):
        reserveDiff =  self.horde.reserve - self.oldReserve
        #~ print "reserve diff", reserveDiff
        self.oldReserve =  self.horde.reserve
        
        opinionTotal = 0.
        for p in self.opinions.values():
            #~ print p
            opinionTotal += p
        #~ print "opinion total ",opinionTotal
        
        

        for p in self.opinions.keys():
            if opinionTotal > 0.:
                self.opinions[p] /= opinionTotal
            self.opinions[p] += reserveDiff/len(self.horde.personnes.keys())
            if self.opinions[p]  < 0:
                self.opinions[p]  = 0
            if self.opinions[p]  > 1:
                self.opinions[p]  = 1 
    
            #~ print "after ",self.opinions[p]
    
class groupActivity:
    def __init__(self, leader, type, requirements):
        self.type = type
        self.requirements = requirements
        self.leader = leader
        
    def canJoin(self, people):
        for r in self.requirements.keys():
            if self.requirements[r] <= 0:
                return False
                
        return True
    
    def join(self, people):
        people.group = self
        for r in self.requirements.keys():
            if r == "people":
                self.requirements[r] -= 1
            else:
                self.requirements[r] -= people.carac[r]
        
    def resolveAction(self, people):
        #~ people.group = None
        if people == self.leader:
            people.horde.groupActivities.remove(self)
        return 1
            
class petiteHorde:
    def __init__(self, terrain):
        self.terrain = terrain
        self.reserve = 3.
        self.personnes = {}
        for i in range(10):
            self.addPersonne()
        for p in self.personnes.values():
            p.age = 15
            
        self.groupActivities = []
        
            
    def addPersonne(self):
        homme = petitHomme(self)
        self.personnes[homme.name] = homme
        
    def changeOpinion(self, name, quantite):
        for p in self.personnes.values():
            if p.name == name:
                continue
                
            if p.action == "rester":
                p.opinions[name] += quantite
                if p.opinions[name]  < 0:
                    p.opinions[name]  = 0
                if p.opinions[name]  > 1:
                    p.opinions[name]  = 1 

    def getHope(self, name):
        result = 0
        for p in self.personnes.values():
            result += p.opinions[name]
        return result

    def update(self):
        for p in self.personnes.values():
            
            p.update()
            
        

        

t = petitTerrain(5)

pH = petiteHorde(t)

toLog.append(pH.personnes.keys()[0])
print toLog

for i in range(10):
    print "---"
    pH.update()
    