
import random

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
        print self.name
        self.opinions = {}
        self.opinions[self.name]  = 1
        for p in self.horde.personnes.values():
            self.opinions[p.name]  = 1
            p.opinions[self.name] = 1
            
        self.age = 0
        self.sante = 1.
        self.forme = 1.
        
        self.action = "rester"
        self.oldReserve = self.horde.reserve
        
    def update(self):
        self.age+= 1./52
        print self.name
        self.averageOpinions()
        print self.opinions
        
        if self.action == "cueillir":
            result = 0.6*(random.random()+random.random()) + 0.2
            print "cueillette ", result
        else:
            result = 0.
        if result >= 1:
            self.forme = 1.
            self.horde.reserve += result - 1.
            self.horde.changeOpinion(self.name, result - 1.)
            self.opinions[self.name] +=  result - 1.
            #changer opinion
        else:
            prendReserve = min(self.horde.reserve/len(self.horde.personnes.keys()), 1. - result)
            self.forme = result + prendReserve
            self.horde.reserve -= prendReserve 
            self.horde.changeOpinion(self.name, -prendReserve )
            self.opinions[self.name] -=  prendReserve
            
        
        #~ print "forme ",self.forme
        #~ print "reserve ",self.horde.reserve
        
        actions = ["cueillir", "rester"]
        self.action = random.choice(actions)
        
        
        
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
     
            
class petiteHorde:
    def __init__(self, terrain):
        self.terrain = terrain
        self.reserve = 3.
        self.personnes = {}
        for i in range(10):
            self.addPersonne()
        for p in self.personnes.values():
            p.age = 15
            
        
            
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
        
    def update(self):
        for p in self.personnes.values():
            
            p.update()
            
        

        

t = petitTerrain(5)

pH = petiteHorde(t)

for i in range(10):
    pH.update()
    