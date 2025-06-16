#question 1
a=int(input("Enter a number "))
if(a==1):
    print("January")
elif(a==2):
    print("February")
elif(a==3):
    print("March")
elif(a==4):
    print("April")
elif(a==5):
    print("may")
elif(a==6):
    print("june")
elif(a==7):
    print("july")
elif(a==8):
    print("august")
elif(a==9):
    print("september")
elif(a==10):
    print("october")
elif(a==11):
    print("november")
elif(a==12):
    print("december")
else:
    print("Invalid input")

    
#Question2
print("-------------------------------------------")
t=int(input("first number "))
b=int(input("second number "))
if t==b:
    print("both are equal")
else:
    print("both are  not equal")
if t>b:
    print("a is bigger than b")
else:
    print("b is bigger than a")
if t<b:
    print("a is smaller than b")
elif t==b:
    print("a is equal to b")
c=input("first name ") 
d=input("surname ")
e=len(c)
f=len(d)
if a>b:
    for i in range(0,5):
      print(c)
else:
    for i in range(0,3):
        print(d)

#question 4--error in question

#Question 5
print("-------------------------------------------")
g=int(input("Enter g "))
h=0
for i in range(0,g+1):
    h+=i
print("Sum upto g is ",h)

#Question 6
print("-------------------------------------------")
j=int(input("Enter j "))
for i in range(0,j):
    if(i%2==0):
        print(i)
#Question 7
print("-------------------------------------------")
x=int(input("Enter x "))
y=input(("Enter(+,-)"))
if(y=='+'):
    for i in range(0,x+1):
        print(i,end=',')
elif(y=='-'):
    for i in range(x+1,-1,-1):
        print(i,end=',')
    print()

#Question 8
print("-------------------------------------------")
k=int(input("Enter k "))
print("Table of ",k)
for i in range(1,11):
    print(k*i)
#Question 9
print("-------------------------------------------")
for i in range(0,4):
    for j in range(0,i+1):
        print(j+1 ,' ',end="")
    print()

#question 10
print("-------------------------------------------")
n=int(input("Enter n "))
for i in range(1,n+1):
    print(i**2)
