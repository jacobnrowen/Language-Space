space = '   '
def space_sylls(syll):
    result = ' '
    temp = [i+space for i in syll[:-1]]
    for i in temp:
        result+=i
    result+=syll[-1]+' '
    return result
def make_grid(word):
    sylls = word.split('.')
    temp = [space_sylls(i)+'.' for i in sylls[:-1]]
    result=''
    for i in temp:
        result+=i
    print( result+space_sylls(sylls[-1]))
    
    
items = ['ma.la.bóŋ','ʔa.nán.da','si.líŋ.ɡi.si','tí.na.ma','i.ti.ʔín.di',
         'sán.de.o','ém.be.ʔi.o']
for i in items:
    make_grid(i)
    print('\n')