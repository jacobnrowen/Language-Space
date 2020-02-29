import random

class Syllable:
    #A syllable has a stress value:
    #0 for unstressed (s), 1 for secondary stress (s̀), 2 for primary stress (ś)
    #And a syllable has a weight:
    #False for light (lowercase 's'), True for heavy (uppercase 'S')
    #If unspecified, syllables are assumed to be light and unstressed (s)
    
    def __init__(self,stress=0,heavy=False):
        self.stress = stress
        self.heavy = heavy
    def __str__(self):
        result = 'S' if self.heavy else 's'
        if self.stress==1:
            result+=u'\u0340'
        elif self.stress==2:
            result+=u'\u0341'
        return result
    def __repr__(self):
        return str(self)

class Foot:
    
    def __init__(self,syllables,trochaic=True,moraic=False):
        if not moraic:
            if len(syllables)!=2:
                raise Exception("Non-binary foot")
            (a,b)=syllables
            if trochaic:
                if a.stress==0 or b.stress>0:
                    raise Exception("Expected trochee, found "+str(a)+str(b))
            else:
                if a.stress>0 or b.stress==0:
                    raise Exception("Expected iamb, found "+str(a)+str(b))
        self.syllables=syllables
        self.trochaic=trochaic
        self.moraic=moraic
    
    def __str__(self):
        return '('+str(self.syllables[0])+', '+str(self.syllables[1])+')'
    def __repr__(self):
        return str(self)




class Word:
    
    #A Word is created by providing a list of syllables and a list of tuples,
    #called the parameters. The first element of these tuples is the name,
    #followed by a pure function, followed by the expected return value of
    #the function. For example, ("iterative",f,True), where f is:
    #(lambda w : True if len([i for i in w.syllables if i.stress==1])>0 else False)
    
    
    def __init__(self,syllables,parameters):
        self.syllables=syllables
        self.parse_results = self.parse_syllables(parameters)
        
    def parse_syllables(self,parameters):
        results=[]
        for (name,f,val) in parameters:
            if f(self)==val:
                results.append(name)
        return results
    
    def __str__(self):
        return str(self.parse_results)
    def __repr__(self):
        return str(self)



def generate():
    syllables=[]
    for i in range(random.randint(1,7)):
        syllables.append(Syllable(random.randint(0,2)))
    return syllables


def iterative(w):
    return True if len([i for i in w.syllables if i.stress==1])>0 else False
def no_extrametric_trochaic_right(w):
    isodd = len(w.syllables)%2
    endindex = len(w.syllables)-isodd
    try:
        for i in range(0,endindex,2):
            Foot(w.syllables[i],w.syllables[i+1])
    except:
        try:
            if isodd==1:
                for i in range(1,endindex,2):
                    Foot(w.syllables[i],w.syllables[i+1])
        except:
            return False
    return True


for i in range(5):
    g = generate()
    print(g)
    print(Word(g,[("iterative",iterative,True),("standard",
               no_extrametric_trochaic_right,True)]))





