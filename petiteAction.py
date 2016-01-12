import random
import utils

class petiteAction:
    def __init__(self, name):
        self.name = name
        self.results = {}
        self.newActions = {}
        self.risks = {}
        self.requiredKnowledges = {}
        self.acquiredKnowledges = {}
        self.dontRemember = False
        
    def resolve(self, p, noChange=False):
        
        for n in self.newActions.keys():
            if not noChange:
                if random.random() < self.newActions[n]:
                    #~ print "will try ",n
                    if allActions[n].canDo(p):
                        #~ print "try ",n
                        p.action = n
                        return allActions[n].resolve(p)
                
        for r in self.risks.keys():
            if random.random() < self.risks[r][0]:
                
                p.addHealthEvent(r, self.risks[r][1],self.risks[r][2])
                
        for a in self.acquiredKnowledges.keys():
            #~ print a, ".. ",self.acquiredKnowledges[a]
            rr = random.random()
            #~ print rr
            if  rr < self.acquiredKnowledges[a]:
                #~ print "acquiring ",a
                utils.sparseLogs(p.name, p.name +" apprends "+a)
                k = p.knowledges.get(a, 0)
                k += (1-k)*0.1
                p.knowledges[a] = k

        res = {}
        if self.canDo(p):
            for r in self.results.keys():
                res[r] = self.results[r][0] + 0.5*(self.results[r][1] - self.results[r][0])*(random.random() + random.random())
        return res
        
    def canDo(self, p):
        for r in self.requiredKnowledges.keys():
            valp = p.knowledges.get(r, 0)
            if valp< self.requiredKnowledges[r]:
                #~ print valp, "is not enough ",r," for ",self.name
                return False
        return True

allActions = {}
act = petiteAction("rester")
act.newActions["cueillir fruits"] = 0.05
allActions[act.name] = act

act = petiteAction("cueillir baies")
act.results["baies"] = [0.2, 0.8]
act.newActions["cueillir champignons"] = 0.005
act.newActions["cueillir racines"] = 0.001
act.newActions["cueillir fruits"] = 0.001
act.risks["morsure de serpent"] = [0.01, 0.8, 2]
act.requiredKnowledges["connaissance des baies"] = 0.2
allActions[act.name] = act

act = petiteAction("cueillir racines")
act.results["racines"] = [0., 0.7]
act.results["champignons"] = [0., 0.2]
act.newActions["cueillir champignons"] = 0.005
act.newActions["cueillir baies"] = 0.001
act.risks["orties"] = [0.01, 0.9, 10]
act.newActions["fuir un loup"] = 0.001
act.newActions["fuir un sanglier"] = 0.001
act.acquiredKnowledges["connaissance des champignons"] = 0.01
allActions[act.name] = act

act = petiteAction("cueillir champignons")
act.results["champignons"] = [0.1, 0.6]
act.results["baies"] = [0., 0.3]
act.newActions["cueillir baies"] = 0.005
act.newActions["cueillir racines"] = 0.005
act.risks["champignon veneneux"] = [0.001, 0.7, 1]
act.newActions["fuir un loup"] = 0.001
act.newActions["fuir un sanglier"] = 0.001
act.requiredKnowledges["connaissance des champignons"] = 0.2
allActions[act.name] = act

act = petiteAction("cueillir fruits")
act.results["fruits"] = [0.3, 0.6]
act.results["baies"] = [0., 0.2]
act.newActions["cueillir baies"] = 0.005
act.newActions["ramasser miel"] = 0.005
act.newActions["ramasser oeufs"] = 0.005
act.acquiredKnowledges["connaissance des baies"] = 0.01
allActions[act.name] = act

act = petiteAction("ramasser miel")
act.results["miel"] = [0.0, 0.6]
act.newActions["cueillir fruits"] = 0.005
act.newActions["fuir un ours"] = 0.001
act.acquiredKnowledges["connaissance des abeilles"] = 0.01
act.risks["piqure d'abeille"] = [0.01, 0.8, 1]
allActions[act.name] = act

act = petiteAction("ramasser oeufs")
act.results["oeuf"] = [0.3, 0.7]
act.newActions["cueillir fruits"] = 0.005
act.newActions["fuir un ours"] = 0.001
act.newActions["ramasser oeufs de coucou"] = 0.005
act.newActions["ramasser oeufs de hiboux"] = 0.005
act.newActions["ramasser oeufs de perdrix"] = 0.005
act.acquiredKnowledges["connaissance des oiseaux"] = 0.01
act.risks["attaque d'oiseau"] = [0.001, 0.7, 3]
allActions[act.name] = act

act = petiteAction("ramasser oeufs de coucou")
act.results["oeuf"] = [0.4, 0.7]
act.newActions["fuir un ours"] = 0.001
act.acquiredKnowledges["connaissance des oiseaux"] = 0.01
act.requiredKnowledges["connaissance des oiseaux"] = 0.4
act.risks["attaque d'oiseau"] = [0.001, 0.7, 3]
allActions[act.name] = act

act = petiteAction("ramasser oeufs de hiboux")
act.results["oeuf"] = [0.4, 0.7]
act.newActions["fuir un ours"] = 0.001
act.acquiredKnowledges["connaissance des oiseaux"] = 0.01
act.requiredKnowledges["connaissance des oiseaux"] = 0.4
act.risks["attaque d'oiseau"] = [0.001, 0.7, 3]
allActions[act.name] = act

act = petiteAction("ramasser oeufs de perdrix")
act.results["oeuf"] = [0.4, 0.7]
act.newActions["fuir un ours"] = 0.001
act.acquiredKnowledges["connaissance des oiseaux"] = 0.01
act.requiredKnowledges["connaissance des oiseaux"] = 0.4
allActions[act.name] = act

act = petiteAction("fuir un ours")
act.acquiredKnowledges["connaissance des ours"] = 0.01
act.risks["griffures d'ours"] = [0.1, 0.6, 5]
act.risks["morsure d'ours"] = [0.1, 0.6, 5]
act.risks["devore par l'ours"] = [0.1, 0.1, 10]
act.dontRemember = True
allActions[act.name] = act

act = petiteAction("fuir un loup")
act.acquiredKnowledges["connaissance des loups"] = 0.01
act.risks["griffures de loup"] = [0.05, 0.7, 5]
act.risks["morsure de loup"] = [0.1, 0.6, 5]
act.risks["devore par les loups"] = [0.1, 0.1, 10]
act.dontRemember = True
allActions[act.name] = act

act = petiteAction("fuir un sanglier")
act.acquiredKnowledges["connaissance des sangliers"] = 0.01
act.risks["charge de sanglier"] = [0.02, 0.6, 5]
act.dontRemember = True
allActions[act.name] = act


