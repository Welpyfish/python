l=int(input("length of rectangle"))
w=int(input("width of rectangle"))

print ('* '*l)
for a in range (2, w, 1):
    print ('*'+'  '*(l-2)+' *')
print ('* '*l)




