b=(input("please type the base of the triangle "))
b=int(float(b))
a=1
sp=int((b-1)/2)
st=3

print(' '*sp+'*')
sp=sp-1
for st in range (3, b, 2):
    print(' '*sp+'*'+' '*(st-2)+'*')
    sp=sp-1
    a=a+1
print('*'*b)