#For the sake of this program, for now, we're going to ignore quantity sensitivity
#All syllables will be assumed to be light except for the stressed syllables in iambs
parameters = ["iterativity","directionality", "extrametricality",
                    "foot_headedness", "degenerate_feet", "word_headedness"]

class Syllable:
#A syllable has a stress value:
#0 for unstressed (s), 1 for secondary stress (s̀), 2 for primary stress (ś)
#If unspecified, syllables are assumed to be unstressed (s)
#Syllables can also be assigned a number to keep track of where they fall in a word
    def __init__(self,stress=0, num=-1):
        self.stress = stress
        self.num = num
    def __str__(self):
        result = 's'
        if self.stress==1:
            result+=u'\u0340'
        elif self.stress==2:
            result+=u'\u0341'
        if self.num >= 0 and self.num < 10:
            result+=chr(8320 + self.num) #Adds a subscript in range 0-9 inclusive
        return result
    def __repr__(self):
        return str(self)
    


class Foot():
#In this program, feet will only ever be unary or binary, but this class is size agnostic
#A foot has its syllables and a headedness that determines which side is stressed
#The headedness doesn't actually matter for unary feet, of course
    def __init__(self,syllables,headedness):
        self.syllables = syllables
        if headedness == -1:
            self.syllables[0] = Syllable(stress = 1, num=syllables[0].num)
        else:
            self.syllables[-1] = Syllable(stress = 1, num=syllables[-1].num)
        self.headedness = headedness
    
    #A word's primary stress is handled at the foot level
    #If a word decides that a foot contains the primary stress, this function is called
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
#Much of the meat of the program is here in the Footed_Word class
#Each Footed_Word has a dictionary of its parameters
#Each parameter has a value of either 1 or -1
#A value of 1 repreents "yes" for extrametricality, degenerate feet, and iterativity
#A value of -1 represents "no" for these
#A value of 1 represents "right" for foot and word headedness
#A value of -1 represents "left" for foot and word headedness
#A value of 1 represents "Right to Left" for directionality
#A value of -1 represents "Left to Right" for directionality
#A Footed_Word is unfootable iff it is iterative and has an unfooted syllable
    def __init__(self, syllables, params):
        self.syllables = syllables.copy()
        self.parameters = params.copy()
        self.feet = []
        self.unfootable = False
        self.unfooted = '' #Just for help with the string representation
        
        if self.parameters['extrametricality'] == 1:
            self.syllables.pop() #Remove the last syllable from consideration
        
        if self.parameters['iterativity'] == 1:
            if len(self.syllables) % 2 == 0: #Directionality doesn't matter for even syllable counts
                for i in range(0,len(self.syllables),2):
                    self.feet.append(Foot(self.syllables[i:i+2],self.parameters['foot_headedness']))
            else:
                if self.parameters['directionality'] == 1:
                    if self.parameters['degenerate_feet'] == 1:
                        self.feet.append(Foot(self.syllables[:1],self.parameters['foot_headedness']))
                    else:
                        self.unfootable = True
                        self.unfooted = str(self.syllables[0])
                    for i in range(1,len(self.syllables),2):
                        self.feet.append(Foot(self.syllables[i:i+2],self.parameters['foot_headedness']))
                else:
                    for i in range(0,len(self.syllables)-1,2):
                        self.feet.append(Foot(self.syllables[i:i+2],self.parameters['foot_headedness']))
                    if self.parameters['degenerate_feet'] == 1:
                        self.feet.append(Foot(self.syllables[-1:],self.parameters['foot_headedness']))
                    else:
                        self.unfootable = True
                        self.unfooted = str(self.syllables[-1])
        else:
            if self.parameters['directionality'] == 1:
                self.feet.append(Foot(self.syllables[-2:],self.parameters['foot_headedness']))
                for i in self.syllables[:-2]:
                    self.unfooted += str(i)
            else:
                self.feet.append(Foot(self.syllables[:2],self.parameters['foot_headedness']))
                for i in self.syllables[2:]:
                    self.unfooted += str(i)
                    
        if self.parameters['word_headedness'] == 1:
            self.feet[-1].make_primary()
        else:
            self.feet[0].make_primary()
    
    def __str__(self):
        result = ''
        feet_strings = ''
        for i in self.feet:
            feet_strings+=str(i)
        if self.parameters['directionality'] == 1:
            result = self.unfooted + feet_strings
        else:
            result = feet_strings + self.unfooted
        if self.parameters['extrametricality'] == 1:
            result += '<' + str(Syllable(num=len(self.syllables))) + '>'
        return result
    def __repr__(self):
        return str(self)
        
        

class Language:
#For representative purposes, a language has six "words" from lengths 4 through 8
#The Language also keeps track of its parameters, with the same dictionary structure as above.
#However, Language parameters can have a value of 0, meaning "undecided"
#The main purpose of a language is to show all the possible footings given limited data
#On instantiation, a language has a list of all possible footings of each syllable sequence
#As parameters are decided as either 1 or -1, the list of possible footings shrinks
#The way this is designed to be done is by changing the dictionary directly, then calling update()
#Example:
#   example_lang['iterativity'] = 1
#   example_lang.update()
#The possible_footings list itself is actually a list of lists, one list of options for each word
#To see the current list of possibilities for a word with six syllables:
#   example_lang.possible_footings[2]
#   (The first word is four syllables, so the third is six)
    def __init__(self):
        self.words = []
        for i in range(4,9):
            self.words.append([])
            for j in range(i):
                self.words[i-4].append(Syllable(num=j))
        self.parameters = {prop: 0 for prop in parameters}
        
        self.possible_footings = []
        l = [-1,1]
        opts = [[a,b,c,d,e,f] for a in l for b in l for c in l for d in l for e in l for f in l]
        for index,word in enumerate(self.words):
            self.possible_footings.append([])
            for opt in opts:
                props = {}
                for i,prop in enumerate(parameters):
                    props[prop] = opt[i]
                self.possible_footings[index].append(Footed_Word(word,props))
        
        
    def update(self):
        keep_footings = []
        for index,word in enumerate(self.possible_footings):
            keep_footings.append([])
            for footing in word:
                keep = True
                for prop in parameters:
                    if self.parameters[prop] != 0:
                        if self.parameters[prop] != footing.parameters[prop]:
                            keep = False
                if keep:
                    keep_footings[index].append(footing)
        self.possible_footings = keep_footings
    
    def remove_possibility(self,params):
        keep_footings = []
        for index,word in enumerate(self.possible_footings):
            keep_footings.append([])
            for footing in word:
                if footing.parameters != params:
                    keep_footings[index].append(footing)
        self.possible_footings = keep_footings
        
                    
    
    def __str__(self):
        return str(self.parameters)
    def __repr__(self):
        return str(self)
    



#--------------------------------------------------------------------------------
#Let's go through an example of how the structures above can be used in practice:
#--------------------------------------------------------------------------------


#Given a data set with stress markings and at least one word of five syllables of
#unknown weight, the iterativity and word headedness can be determined trivially.
#Let's explore the options from there.
non_iterative = Language()
iterative = Language()
non_iterative.parameters['iterativity'] = -1
non_iterative.update()
iterative.parameters['iterativity'] = 1
iterative.update()
#Let's explore the non_iterative options first
print('Non-iterative round one:\n')
for i in non_iterative.possible_footings[1]:
    print(i.parameters,'\n',i,'\n\n')
[print('------------------------------\n') for i in range(3)]
#That's a lot of options
#But if it's non-iterative, there's more free information
#The directionality can be determined by which side the stress is on
#or, since extrametricality is assumed to be on the right side only,
#if the stress is on the middle syllable, then the directionality must be right to left.
#The word headedness doesn't even matter in a non-iterative language
#So we have something that, at worst, looks like this:
non_iterative.parameters['directionality'] = 1
non_iterative.parameters['word_headedness'] = 1
non_iterative.update()
print('Non-iterative round two:\n')
for i in non_iterative.possible_footings[1]:
    print(i.parameters,'\n',i,'\n\n')
[print('------------------------------\n') for i in range(3)]
#After looking at these options, it becomes clear that the allowability of
#degenerate feet isn't knowable from a five (or more) syllable word in a non-iterative language.
#In our current view of the options, this parameter is basically pointless to try to learn about.
#So let's just decide on not having degenerate feet:
print('Non-iterative round three:\n')
non_iterative.parameters['degenerate_feet'] = -1
non_iterative.update()
for i in non_iterative.possible_footings[1]:
    print(i.parameters,'\n',i,'\n\n')
[print('------------------------------\n') for i in range(3)]
#With that done, there are only four possibilities remaining
#If the last syllable is stressed, then the language must be iambic without extrametricality
#If the middle syllable is stressed, then the language must be trochaic with extrametricality
#Unfortunately, if the second to last syllable is stressed, there are still two possibilities:
#Iambic with extrametricality, or trochaic without extrametricality
#This ambiguity is always going to be present without other kinds of data available to help,
#as each of these options always leave stress on the penult and nowhere else.

[print('------------------------------\n') for i in range(3)]

#Now let's look at the iterative options:
print('Iterative round one:\n')
for i in iterative.possible_footings[1]:
    print(i.parameters,'\n',i,'\n\n')
[print('------------------------------\n') for i in range(3)]
#That's even more options than we started with before!
#First, word headedness is easy to spot. let's say it's left this time.
print('Iterative round two:\n')
iterative.parameters['word_headedness'] = -1
iterative.update()
for i in iterative.possible_footings[1]:
    print(i.parameters,'\n',i,'\n\n')
[print('------------------------------\n') for i in range(3)]
#Next, if there are three stressed syllables, then there isn't extrametricality,
#and there must be a degenerate foot. Let's take a tangent down that road:
tangent = Language()
tangent.parameters = iterative.parameters.copy()
tangent.parameters['degenerate_feet'] = 1
tangent.parameters['extrametricality'] = -1
tangent.update()
print('Tangent:\n')
for i in tangent.possible_footings[1]:
    print(i.parameters,'\n',i,'\n\n')
[print('------------------------------\n') for i in range(3)]
#Two of the options here jump out as very strange:
#In one of them, the last two syllables are both stressed;
#in the other, the first two syllables are both stressed.
#These seem like they would probably cause a stress clash in a real language,
#but they are certainly distinct. The first of these must be left to right iambic,
#and the second must be right to left trochaic.
#Unfortunately, the other two cases look exactly the same. These are
#left to right trochaic and right to left iambic. In words with an odd number of
#metric syllables, these cases are indistinguishable.

[print('------------------------------\n') for i in range(3)]


#Back in our original iterative situation, let's say there are only two stressed syllables,
#as we would've spotted a third if it were present.
#That means either there is extrametricality, or there isn't a degenerate foot.
#If the last syllable is stressed, then that syllable can't be extrametric by definition.
#And in fact, the only possible combination of parameters to yield this would be
#right to left iambic with degenerate feet disallowed. So now we have some cases to remove by hand:

#The ones in our tangent with three stressed syllables:
r1 = tangent.parameters.copy()
r1['foot_headedness'] = 1
r1['directionality'] = 1
iterative.remove_possibility(r1)
r1['foot_headedness'] = 1
r1['directionality'] = -1
iterative.remove_possibility(r1)
r1['foot_headedness'] = -1
r1['directionality'] = 1
iterative.remove_possibility(r1)
r1['foot_headedness'] = -1
r1['directionality'] = -1
iterative.remove_possibility(r1)
r2 = iterative.parameters.copy()
r2['extrametricality'] = -1
r2['directionality'] = 1
r2['foot_headedness'] = 1
r2['degenerate_feet'] = -1
iterative.remove_possibility(r2)

print('Iterative round three:\n')
for i in iterative.possible_footings[1]:
    print(i.parameters,'\n',i,'\n\n')
[print('------------------------------\n') for i in range(3)]
#Now there are 11 possibilities left, 6 with stress on the first and third syllables,
#and five with stress on the second and fourth syllables. The lesson here is that
#it is really, really hard to tell the difference between an extrametric syllable
#and a syllable that just isn't footed because it would be degenerate in a
#language that doesn't permit degenerate syllables. There's really nothing to be done
#in these cases except look for other kinds of data.











