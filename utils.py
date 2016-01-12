 
import random
    
needsFromObjects = {}
needsFromObjects["baies"] = {"faim":0.6, "soif":0.5}
needsFromObjects["racines"] = {"faim":0.9}
needsFromObjects["champignons"] = {"faim":0.8, "soif":0.2}
needsFromObjects["eau"] = {"soif":1.}
needsFromObjects["viande"] = {"faim":1.}
needsFromObjects["fruits"] = {"faim":0.8, "soif":0.2}
needsFromObjects["miel"] = {"faim":0.8}
needsFromObjects["oeuf"] = {"faim":0.9}
        
        
consonnes_rares = "B.D.F.G.H.J.V.Qu.Ch.Pr.Cr.Sc"
consonnes_frequentes = "C.L.M.N.P.R.S.T.St.Tr"
consonnes = consonnes_frequentes.split('.')*2 + consonnes_rares.split('.')
voyelles_rares = "u.in.ai.ei.eu.ia.ui.io"
voyelles_frequentes = "a.e.i.o.on.ou.en.au"
voyelles = voyelles_frequentes.split('.')*2 + voyelles_rares.split('.')    

def getName():
    n = random.choice(consonnes)+random.choice(voyelles)+random.choice(consonnes).lower()+random.choice(voyelles)
    if random.randint(0,1) ==0:
        n +=random.choice(consonnes).lower()
        if random.randint(0,1) ==0:
            n+=random.choice(voyelles)
    #~ print n
    return n
    
toLog = []
def sparseLogs(name, toPrint):
    if name in toLog:
        print ".."+toPrint
        