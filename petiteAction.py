import random

class petiteAction:
    def __init__(self, name):
        self.name = name
        self.results = {}
        self.newActions = {}
        self.risks = {}
        
    def resolve(self, p):
        
        for n in self.newActions.keys():
            #~ print n
            if random.random() < self.newActions[n]:
                #~ print "bla !"
                p.action = n
                return allActions[n].resolve(p)
                
        for r in self.risks.keys():
            if random.random() < self.risks[r][0]:
                p.addHealthEvent(r, self.risks[r][1],self.risks[r][2])

                #~ if p.getHealth() > 1 - self.risks[r][1]:
                    #~ p.sante.append([r,self.risks[r][1],self.risks[r][2] ])

                #~ else:

                    #~ p.forme = 0
        
        res = {}
        for r in self.results.keys():
            res[r] = self.results[r][0] + 0.5*(self.results[r][1] - self.results[r][0])*(random.random() + random.random())
        return res
        

allActions = {}
act = petiteAction("rester")
act.newActions["cueillir baies"] = 0.05
allActions[act.name] = act

act = petiteAction("cueillir baies")
act.results["baies"] = [0.2, 0.8]
act.newActions["cueillir champignons"] = 0.005
act.newActions["cueillir racines"] = 0.001
act.newActions["cueillir fruits"] = 0.001
allActions[act.name] = act

act = petiteAction("cueillir racines")
act.results["racines"] = [0., 0.7]
act.results["champignons"] = [0., 0.2]
act.newActions["cueillir champignons"] = 0.005
act.newActions["cueillir baies"] = 0.001
act.risks["orties"] = [0.01, 0.9, 10]
allActions[act.name] = act

act = petiteAction("cueillir champignons")
act.results["champignons"] = [0.1, 0.6]
act.results["baies"] = [0., 0.3]
act.newActions["cueillir baies"] = 0.005
act.newActions["cueillir racines"] = 0.005
act.risks["champignon veneneux"] = [0.001, 0.7, 1]
allActions[act.name] = act

act = petiteAction("cueillir fruits")
act.results["fruits"] = [0.3, 0.6]
act.results["baies"] = [0., 0.2]
act.newActions["cueillir baies"] = 0.005
allActions[act.name] = act


