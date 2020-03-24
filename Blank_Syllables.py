class Syllable:
    #A syllable has a stress value:
    #0 for unstressed (s), 1 for secondary stress (s̀), 2 for primary stress (ś)
    #And a syllable has a weight:
    #False for light (lowercase 's'), True for heavy (uppercase 'S')
    #If unspecified, syllables are assumed to be light and unstressed (s)
    
    def __init__(self,stress=0,heavy=False, num=-1):
        self.stress = stress
        self.heavy = heavy
        self.num = num
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
    
    def __init__(self,syllables,headedness):
        self.syllables = syllables
        if headedness == -1:
            self.syllables[0] = Syllable(stress = 1, num=syllables[0].num)
        else:
            self.syllables[-1] = Syllable(stress = 1, num=syllables[-1].num)
        self.headedness = headedness
    def make_primary(self):
        if self.headedness == -1:
            self.syllables[0] = Syllable(stress = 2, num=self.syllables[0].num)
        else:
            self.syllables[-1] = Syllable(stress = 2, num=self.syllables[-1].num)
    def __len__(self):
        return len(self.syllables)
    def __str__(self):
        return '('+str(self.syllables)[1:-1]+')'
    def __repr__(self):
        return str(self)
    
    
class Footed_Word:
    
    def __init__(self, syllables, properties):
        self.syllables = syllables.copy()
        self.properties = properties
        self.feet = []
        self.unfootable = False
        self.unfooted = ''
        
        if properties['extrametricality'] == 1:
            self.syllables.pop()
        
        if properties['iterativity'] == 1:
            if len(self.syllables) % 2 == 0:
                for i in range(0,len(self.syllables),2):
                    self.feet.append(Foot(self.syllables[i:i+2],self.properties['foot_headedness']))
            else:
                if properties['directionality'] == 1:
                    if self.properties['degenerate_feet'] == 1:
                        self.feet.append(Foot(self.syllables[:1],self.properties['foot_headedness']))
                    else:
                        self.unfootable = True
                        self.unfooted = str(self.syllables[0])
                    for i in range(1,len(self.syllables),2):
                        self.feet.append(Foot(self.syllables[i:i+2],self.properties['foot_headedness']))
                else:
                    for i in range(0,len(self.syllables)-1,2):
                        self.feet.append(Foot(self.syllables[i:i+2],self.properties['foot_headedness']))
                    if self.properties['degenerate_feet'] == 1:
                        self.feet.append(Foot(self.syllables[-1:],self.properties['foot_headedness']))
                    else:
                        self.unfootable = True
                        self.unfooted = str(self.syllables[-1])
        else:
            if properties['directionality'] == 1:
                self.feet.append(Foot(self.syllables[-2:],self.properties['foot_headedness']))
                for i in self.syllables[:-2]:
                    self.unfooted += str(i)
            else:
                self.feet.append(Foot(self.syllables[:2],self.properties['foot_headedness']))
                for i in self.syllables[2:]:
                    self.unfooted += str(i)
                    
        if properties['word_headedness'] == 1:
            self.feet[-1].make_primary()
        else:
            self.feet[0].make_primary()
    
    def __str__(self):
        result = ''
        feet_strings = ''
        for i in self.feet:
            feet_strings+=str(i)
        if self.properties['directionality'] == 1:
            result = self.unfooted + feet_strings
        else:
            result = feet_strings + self.unfooted
        if self.properties['extrametricality'] == 1:
            result += '<' + str(Syllable(num=len(self.syllables))) + '>'
        return result
    def __repr__(self):
        return str(self)
        
        

class Language:
    
    def __init__(self):
        self.words = []
        for i in range(4,9):
            self.words.append([])
            for j in range(i):
                self.words[i-4].append(Syllable(num=j))
        self.properties = {prop: 0 for prop in 
                   ["iterativity","directionality", "extrametricality",
                    "foot_headedness", "degenerate_feet", "word_headedness"]}
        
        self.possible_footings = []
        l = [-1,1]
        opts = [[a,b,c,d,e,f] for a in l for b in l for c in l for d in l for e in l for f in l]
        for index,word in enumerate(self.words):
            self.possible_footings.append([])
            for opt in opts:
                props = {}
                for i,prop in enumerate(self.properties):
                    props[prop] = opt[i]
                self.possible_footings[index].append(Footed_Word(word,props))
        
        
    def update(self):
        for word in self.possible_footings:
            for footing in word:
                for prop in footing.properties:
                    if self.properties[prop] != 0:
                        if self.properties[prop] != footing.properties[prop]:
                            word.remove(footing)
                    
    
    def __str__(self):
        return str(self.properties)
    def __repr__(self):
        return str(self)
    


lang = Language()
s = {str(i) for i in lang.possible_footings[0]}
[print(i) for i in s]
print(len(s))







