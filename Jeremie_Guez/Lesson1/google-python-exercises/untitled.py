for i in range[0:100]:
    test=" "
    if i%3==0:
        test=test+'fiz'
    if i%5==0:
        test=test+'buzz'
    if test[-1]!='z':
        test=test+i
print test