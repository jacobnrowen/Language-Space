class Syllable:
    #A syllable has a stress value:
    #0 for unstressed (s), 1 for secondary stress (s̀), 2 for primary stress (ś)
    #And a syllable has a weight:
    #False for light (lowercase 's'), True for heavy (uppercase 'S')
    #If unspecified, syllables are assumed to be light and unstressed (s)
    
    def __init__(self,stress=0,heavy=False, num=-1):
        self.stress = stress
        self.heavy = heavy
    def __str__(self):
        result = 'S' if self.heavy else 's'
        if self.stress==1:
            result+=u'\u0340'
        elif self.stress==2:
            result+=u'\u0341'
        if self.num >= 0 and self.num < 10:
            result+=chr(8320 + self.num)
        return result
    def __repr__(self):
        return str(self)
    
class Foot():
    
    def __init__(self,syllables,headedness,directionality):
        self.syllables = syllables
        if headedness == -1:
            self.syllables[0] = Syllable(stress=1, num=syllables[0].num)
        else:
            self.syllables[-1] = Syllable(stress=1, num=syllables[-1].num)
        self.headedness = headedness
        self.directionality = directionality
    def __len__(self):
        return len(self.syllables)
    def __str__(self):
        return '('+str(self.syllables)[1:-1]+')'
    def __repr__(self):
        return str(self)
        

class Language:
    
    def __init__(self):
        self.words = []
        for i in range(4,9):
            self.words.append([])
            for j in range(i):
                self.words[i-4].append(Syllable(num=i-4))
        self.properties = {prop: 0 for prop in ["extrametricality",
                "foot_headedness", "directionality", "iterativity", "degenerate_feet", "word_headedness"]}
        self.possible_feet = []
        self.make_possible_feet()
    
    def make_possible_feet(self):
        self.possible_feet = []
        if self.properties['iterativity']!=1:
            opts = [(1,1),(1,-1),(-1,1),(-1,-1)]
            for index, word in enumerate(self.words):
                self.possible_feet.append([])
                for opt in opts:
                    (headedness,directionality) = opt
                    if directionality == -1:
                        self.possible_feet[index].append(Foot(word[:2],headedness,directionality))
                    else:
                        self.possible_feet[index].append(Foot(word[-2:],headedness,directionality))       
        else:
            opts = [(1,1),(1,-1),(-1,1),(-1,-1)]
            for index, word in enumerate(self.words):
                self.possible_feet.append([])
                for opt in opts:
                    (headedness,directionality) = opt
                    if len(word) % 2 == 0:
                        for i in range(0,len(word),2):
                            self.possible_feet[index].append(Foot(word[i:i+2],headedness,directionality))
                    else:
                        if directionality == -1:
                            for i in range(0,len(word)-2,2):
                                self.possible_feet[index].append(Foot(word[i:i+2],headedness,directionality))
                            self.possible_feet[index].append(Foot(word[-1],headedness,directionality))
                        else:
                            for i in range(len(word)-1,1,-2):
                                self.possible_feet[index].append(Foot(word[i-1:i+1],headedness,directionality))
                            self.possible_feet[index].append(Foot(word[0],headedness,directionality))
    
    def __str__(self):
        return str(self.properties)
    def __repr__(self):
        return str(self)
    def impossible(self):
        raise Exception("Combination of parameters impossible:\n"+str(self))
    
    def apply_properties(self):
        for i in self.properties:
            if self.properties[i] != 0:
                self.get_attr(self,'apply_'+i)()
                self.check_footability(i)
    def check_footability(self, prop):
        #Check that there is at least one comb
        if self.properties['iterativity']!=1:
            for i in self.possible_feet:
                if len(i) == 0:
                    self.impossible()
                
                
                
                
    def apply_extrametricality(self):
        if (self.properties['extrametricality'] == 1):
            self.properties['extrametricality'] = 2 #Ensures won't happen again
            for i in self.words:
                i.pop()
            self.make_possible_feet()
    
    
    def removal_helper(self,check):
        for i in self.possible_feet:
            for j in i:
                if (check(j)):
                    i.remove(j)
    
    def apply_foot_headedness(self):
        if self.properties['foot_headedness'] != 0:
            self.removal_helper(lambda x:
                x.headedness != self.properties['foot_headedness'])
    def apply_directionality(self):
        if self.properties['directionality'] != 0:
            self.removal_helper(lambda x:
                x.directionality != self.properties['directionality'])
    
    def apply_degenerate_feet(self):
        if (self.properties['degenerate_feet'] == -1):
            if (self.properties['iterativity'] == 1):
                self.removal_helper(lambda x: len(x) != 2)
    
    def apply_word_headedness(self):
        pass

    def apply_iterativity(self):
        if (self.properties['iterativity'] == 1):
            self.properties['iterativity'] = 2 #Ensures won't happen again
            self.make_possible_feet()










