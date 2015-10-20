__author__ = 'Mohamed Amine'


output = []
for idx in range(1, 100):
    if idx%3==0 and idx%5==0:
        output.append("fizbuzz")
    elif idx%5==0:
        output.append( "buzz")
    elif idx%3==0:
        output.append( "fiz")
    else:
        output.append( idx )
print output