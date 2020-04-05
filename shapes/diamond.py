b=input("width of diamond")
b=int(float(b))
b=int((b+1)/2)*2
a=1
sp=-a+int(b+1/2)
st=2*a-1

for st in range (1, b, 2):
    print (' '*sp+'*'*st)
    sp=sp-1
    a=a+1
b=b-2
a=a+1
sp=sp+1
st=st-2

for st in range (b, 1, -2):
    print (' '*(sp+1)+'*'*(st-1))
    sp=sp+1
    a=a+1
    
