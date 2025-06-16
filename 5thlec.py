#Question1
l1=[3,4,12,65,224,65,24,25,3,2]
print(l1)

#Question2
print("-------------------------------------------")
l2=[1,10,100,3,6,8]
l2.insert(3,59)
l2.append(5)
print(l2)
print(len(l2))

#Question3
print("-------------------------------------------")
l3=[1,2,3,4,5,6,7,8,9,10]
print(l3[::2])

#Question4
print("-------------------------------------------")
l4=["Gaurav",12,23,33.33,"Sharma",True]
for i in l4:
    if type(i) == str:
        print(i)

#Question5
print("-------------------------------------------")
sum=0
for i in l4:
    if type(i) == int or type(i)==float:
        sum += i
print(sum)

#Question6
print
l5=['Dilrose','Maninder','Gaurav','Melvin','Sahil']
print(l5)
a=input("Enter a friend's name to add: ")
l5.append(a)
print(l5)
b=input("Enter your most important friend's name to add: ")
c=int(input("Enter the index to add the name: "))
l5.insert(c, b)
print(l5)