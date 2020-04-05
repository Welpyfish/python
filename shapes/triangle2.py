b=input("base of triangle")
b=int(float(b))
b=int((b+1)/2)*2
a=1
sp=int((b-1)/2)
st=2*a-1

for st in range (1, b, 2):
    print (' '*sp+'*'*st)
    sp=sp-1







