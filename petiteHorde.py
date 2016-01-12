#!/env/bin/python

import random

import petiteAction
import utils
#TODO

#sante
## plus d evenements sante
## maladies
## ne pas aller chasser si trop malade
#actions de groupe
# gestion du risque des actions
#objets
# connaissances
## plus de connaissances
## apprentissage pour les jeunes


def dictDist(dict1, dict2):
    d = 0.
    for k1 in dict1.keys():
        d += abs(dict1[k1] - dict2.get(k1, 0))
        
    for k2 in dict2.keys():
        if k2 not in dict1.keys():
            d += abs(dict2[k2])
    return d
 
from json import JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__           


class petitHomme:
    def __init__(self, horde, saved=None):
        self.horde = horde
        

        self.objects = {}
        self.asked = {}
        self.knownActions = {}
        self.knowledges = {}
        
        self.sante = []
        
        if saved is None:
            self.name = utils.getName()

            self.knownActions["rester"]= petiteActionConnue("rester")
            
            self.age = 0
            self.male = random.randint(0, 1)==0
            self.forme = 1.
            
            self.action = "rester"
            self.accompagniedBy = []
            
            
        else:
            #~ print saved
            #~ print saved["name"]
            self.name = saved["name"]
            
            for a in saved["knownActions"].values():
                self.knownActions[a["name"]]= petiteActionConnue(a["name"], a)
 
            self.knowledges=  saved["knowledges"]
            
            self.age = float(saved["age"])
            self.sante = list(saved["sante"])
            self.male = bool(saved["male"] ) #saved["male"] == "True"
            #~ print self.sante
            self.forme =  float(saved["forme"])
            
            self.action = saved["action"]
            self.accompagniedBy =  list(saved["accompagniedBy"])
            
            self.objects = saved["objects"]


    def write(self):
        self.horde = None
        #~ print self.__dict__
        jwrite = json.dumps(self, cls=MyEncoder)#self.__dict__)#, default=lambda o: o.__dict__)
        return jwrite

    def update(self):
        self.updateHealth()

        
        self.resolveAction()
        if self.forme == 0:
            #~ print self.name," dead"
            return
        self.consume()
        #~ self.getExpectations()
        self.selectAction()
        
    def updateHealth(self):
        oldAge = int(self.age)
        self.age+= 1./52    

        if int(self.age) > oldAge:
            print self.name+" anniversaire : "+str(int(self.age))
            if int(self.age) == 30:
                self.sante.append(["age", 1.0, -1])
                
        
        isEnceinte = False
        for h in self.sante:
            if h[2] >=0:
                h[2] -=1
            if h[0] == "enceinte" :
                isEnceinte  = True
                if random.randint(0, 7) == 0:
                    h[1] -= 0.1
                if self.getHealth() <= 0.:
                    self.forme = 0.
                    print "##Unfortunately, ",self.name," died of grossesse. She was ",int(self.age)           
                    
            if h[0] == "age" and random.randint(0, 100) == 0:
                h[1] -= 0.1
                if self.getHealth() <= 0.:
                    self.forme = 0.
                    if self.male:
                        print "##Unfortunately, ",self.name," died. He was ",int(self.age)
                    else:
                        print "##Unfortunately, ",self.name," died. She was ",int(self.age)
                    
            if h[2] == 0:
                if h[0] == "enceinte":
                    print self.name, " accouche"
                    self.addHealthEvent("accouchement", 0.6, 1)
                    
                    probaBebe = 10
                    if self.forme == 0:
                        probaBebe = 1
                        
                    
                        #~ print self.name, " a accouche"
                    if random.randint(0, probaBebe )==0:
                        print "mais le bebe n'a pas survecu"
                    else:
                        p = self.horde.addPersonne()
                        if p.male:
                            print "le bebe s'appelle ",p.name,", c'est un garcon"
                        else:
                            print "le bebe s'appelle ",p.name,", c'est une fille"

                        
                self.sante.remove(h)
                
                
        if not isEnceinte and not self.male and self.age>15 and self.age < 30 and self.getHealth() >= 0.3 and random.randint(0, 25)==0:

            self.sante.append(["enceinte", 1.0, 40])
            

        
    def addHealthEvent(self, name, gravity, time):
        utils.sparseLogs(self.name, self.name +" subit "+name)
        #~ print self.name +" subit "+name
        h = self.getHealth()
        if h < 1 - gravity:
            if h < random.random()*(1 - gravity):
                self.forme = 0
                if self.male:
                    print "##Unfortunately, ",self.name," died of "+name+". He was ",int(self.age)
                else:
                    print "##Unfortunately, ",self.name," died of "+name+". She was ",int(self.age)
                
        self.sante.append([name,gravity,time ])


    def resolveAction(self):
        if self.age < 10. + 1/52.:
            return
            
        if self.action != "resolved":
            
            prevAct = self.action
            result = petiteAction.allActions[self.action].resolve(self)
            if self.action is not prevAct:
                utils.sparseLogs(self.name, self.name+ ": in fact, I did "+self.action+" instead of "+prevAct)
                
            utils.sparseLogs(self.name, self.name+ " brings from "+self.action+": "+str(result))
            if not petiteAction.allActions[self.action].dontRemember:
                if self.action not in self.knownActions.keys():
                    self.knownActions[self.action] = petiteActionConnue(self.action)
                    
                self.knownActions[self.action].feedback({}, result)


        
            for r in result.keys():
                #~ self.horde.shelter.addObject(r, result[r])
                self.objects[r] = self.objects.get(r, 0) + result[r]
                for n in utils.needsFromObjects[r].keys():
                    self.horde.askFor(n, - utils.needsFromObjects[r][n]*result[r])
    ##                self.asked[n] = max(-1, self.asked.get(n, 0) - needsFromObjects[r][n]*result[r])
    
                    
            for n in self.accompagniedBy:
                personne = self.horde.personnes[n]
                result = petiteAction.allActions[self.action].resolve(personne, noChange=True)
                utils.sparseLogs(personne.name, personne.name+ " brings from "+self.action+" with "+self.name+": "+str(result))
                if not petiteAction.allActions[self.action].dontRemember:
                    if self.action not in personne.knownActions.keys():
                        personne.knownActions[self.action] = petiteActionConnue(self.action)
                    
                    personne.knownActions[self.action].feedback({}, result)
                
                for r in result.keys():
                    #~ self.horde.shelter.addObject(r, result[r])
                    personne.objects[r] = personne.objects.get(r, 0) + result[r]
                    for n in utils.needsFromObjects[r].keys():
                        self.horde.askFor(n, - utils.needsFromObjects[r][n]*result[r])
                
                personne.action = "resolved"

        self.accompagniedBy = []
        self.action = ""     
 
    def consume(self):
        
        for o in self.objects.keys():
            self.horde.shelter.addObject(o, self.objects[o])
            self.objects[o] = 0

        n = len(self.horde.personnes.keys())
        
        for need in ["faim"]:#, "soif"]:
            
            manger = self.horde.shelter.needs.get(need, 0.)
            toEat = min(manger/n, 1.)
            #~ print toEat
            self.horde.shelter.getFromNeeds(need, toEat)
            #~ utils.sparseLogs(self.name, self.name+" eats "+str( toEat))
            
            if need == "faim":
                self.forme = toEat
                if self.age < 15.:
                    toEat = self.age*toEat/self.age     
                
            if toEat == 1.:
                self.horde.askFor(need, max(0, 2 - manger/n))
                #~ utils.sparseLogs(self.name, "asking1 for "+str( max(0, 2 - manger/n)))
            else:
                self.horde.askFor(need, 1.)
                

    def selectAction(self):
        if self.age < 10.:
            return

        numRandom = 10
        if self.age < 15.:
            numRandom = 1 + int(9*self.age/15.) #les jeunes imitent plus
        if random.randint(0, numRandom) ==0:
            name = random.choice(self.horde.personnes.keys())
            if name != self.name and self.horde.personnes[name].age > 15.:
                act = self.horde.personnes[name].action
                #~ if petiteAction.allActions[act].canDo(self):
                self.action = act
                self.horde.personnes[name].accompagniedBy.append(self.name)
            
                utils.sparseLogs(self.name, "chosen "+str(self.action)+", like "+name)
                return
            
        action = "rester"
        exp = 100.
        for a in self.knownActions.values():
            if petiteAction.allActions[a.name].canDo(self):
                e= dictDist(a.expects({}), self.asked)
                #~ utils.sparseLogs(self.name, a.name+" exp "+str(e))
                if e < exp and random.random() < 0.9:
                    exp = e
                    action = a.name
##                sparseLogs(self.name, "exp "+str(exp))
            
            
        #~ self.action = random.choice()
        self.action = action
        #~ sparseLogs(self.name, "chosen "+str(self.action))
        
        
    def getHealth(self):
        h = self.forme
        #~ print h
        for i in self.sante:
            h *= i[1]
            #~ print h
            
        #~ print "health ",h
        return h

class petiteActionConnue:
    def __init__(self, name, saved = None):
        self.name = name
        self.needs = {}
        self.results = {}
        if saved is not None:
            #~ print saved
            for r in saved["results"].keys():
                self.results[r] = float(saved["results"][r])
            for n in saved["needs"].keys():
                self.results[n] = float(saved["nedds"][n])
        
    def expects(self, objects):
##        d = dictDist(objects, self.needs)
        
        distanceRate = 0.01
        totalFactor = 1.
        for o in self.needs.keys():
            quantity = 0
            if o in objects.keys():
                quantity = objects[o]
            totalFactor *= 1 - distanceRate*abs(quantity - self.needs[o])
            
        res = {}
        for r in self.results.keys():
            res[r] = totalFactor*self.results[r]

        return res
    
    def feedback(self, objects, results):
        rate = 0.1
        for o in self.needs.keys():
            self.needs[o]*=(1 - rate)
            
        for o in objects.keys():
            self.needs[o] = self.needs.get(o, 0) +rate*objects[o]
            


                
        for r in self.results.keys():
            self.results[r] *= (1 - rate)
            
        for r in results.keys():
            for n in utils.needsFromObjects[r]:
                self.results[n] = self.results.get(n, 0) +rate*results[r]*utils.needsFromObjects[r][n]

      
class petiteMaison:
    def __init__(self, saved = None):
        self.objects = {}
        self.needs = {}
        
        
        if saved is None:
            self.type = "grotte"
        else:
            self.type = saved["type"]
            
            for o in saved["objects"].keys():
                self.addObject(o, saved["objects"][o])

    def write(self):
        return json.dumps(self, default=lambda o: o.__dict__)
        #~ return self.type
        
    def addObject(self, name, num):
        self.objects[name] = self.objects.get(name, 0.) + num
        for n in utils.needsFromObjects.get(name, {}).keys():
            #~ print n
            self.needs[n] = self.needs.get(n, 0.) +num*utils.needsFromObjects[name][n]
        #~ print self.objects
        #~ print self.needs
        
    def getFromNeeds(self, need, num):
        allObj = self.objects.keys()
        random.shuffle(allObj)
        for o in allObj:
            #~ print needsFromObjects.get(o, {}).get(need, 0)
            if self.objects[o] == 0:
                continue
            if utils.needsFromObjects.get(o, {}).get(need, 0) > 0:
                n = min(self.objects[o], num/utils.needsFromObjects[o][need])
                num -= n*utils.needsFromObjects[o][need]
                #~ print "eating ",n,o, "remaining ", num
                
                self.addObject(o, -n)
                if num < 0.01:
                    return

class petiteHorde:
    def __init__(self, saved = None):
        self.personnes = {}
        
        if saved == None:
            self.shelter = petiteMaison()
            
            for i in range(12):
                p = self.addPersonne()
                p.age = 10 +10*random.random()

        else:
            self.shelter = petiteMaison(saved["shelter"])
            for n in saved["personnes"].values():
                self.addPersonne(n)
            
    def addPersonne(self, saved=None):
        homme = petitHomme(self, saved)

        self.personnes[homme.name] = homme
        return homme
        
    def write(self):

        for p in self.personnes.values():
            p.horde = None
            
        return json.dumps(self, cls=MyEncoder, sort_keys = True, indent = 4)

                    
    def peopleAtHome(self):
        result = []
        for p in self.personnes.values():
            if p.action == "" or p.action == "rester":
                result.append(p)
        return result
                

    def askFor(self, need, num):
        people = self.peopleAtHome()
        for p in people:
##            print p.name
##            print p.asked[need]
            p.asked[need] = max(-1, p.asked.get(need, 0.) + num/len(people))
##            print p.asked[need]

                


    def update(self):
        for p in self.personnes.values():
            
            p.update()
            if p.forme == 0:
                
                del self.personnes[p.name]
                
    def run(self, num=10):
        for i in range(num):
            print "---"
            self.update()
            
            
        print "il y a ",len(self.personnes.keys())," personnes dans la horde"
        nbFemmes = 0
        nbFilles = 0
        nbHommes = 0
        nbGarcons = 0
        for p in self.personnes.values():
            if p.male:
                if p.age < 15:
                    nbGarcons +=1
                nbHommes +=1
            else:
                if p.age < 15:
                    nbFilles +=1
                nbFemmes +=1        
                
        print nbHommes," hommes, dont ",nbGarcons," enfants"
        print nbFemmes," femmes, dont ",nbFilles," enfants"
        print ""
        print "manger ",self.shelter.needs.get("faim", 0.)/len(self.personnes.keys())
                        
            
import json
newHorde =False
if newHorde:
    pH = petiteHorde()

    pH.shelter.addObject("baies", 2)
    pH.shelter.addObject("viande", 2)
else:
    f = open('horde.json', 'r')
    content = json.loads(f.read())
    #~ print content
    pH = petiteHorde(content)


#~ utils.toLog.append(pH.personnes.keys()[0])
#~ utils.toLog.append(pH.personnes.keys()[1])
##print toLog

pH.run(10)

f = open('horde.json', 'w')
f.write(pH.write())
f.close()

