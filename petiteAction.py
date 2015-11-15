import random

class petiteAction:
    def __init__(self, name):
        self.name = name
        self.results = {}
        self.newActions = {}
        
    def resolve(self, p):
        
        for n in self.newActions.keys():
            #~ print n
            if random.random() < self.newActions[n]:
                #~ print "bla !"
                p.action = n
                return allActions[n].resolve(p)
        
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
act.newActions["cueillir champignons"] = 0.05
act.newActions["cueillir racines"] = 0.01
act.newActions["cueillir fruits"] = 0.01
allActions[act.name] = act

act = petiteAction("cueillir racines")
act.results["racines"] = [0., 0.7]
act.results["champignons"] = [0., 0.2]
act.newActions["cueillir champignons"] = 0.05
act.newActions["cueillir baies"] = 0.01
allActions[act.name] = act

act = petiteAction("cueillir champignons")
act.results["champignons"] = [0.1, 0.6]
act.results["baies"] = [0., 0.3]
act.newActions["cueillir baies"] = 0.05
act.newActions["cueillir racines"] = 0.05
allActions[act.name] = act

act = petiteAction("cueillir fruits")
act.results["fruits"] = [0.3, 0.6]
act.results["baies"] = [0., 0.2]
act.newActions["cueillir baies"] = 0.05
allActions[act.name] = act

