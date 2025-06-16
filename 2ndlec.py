#Question No.1

name=input("Name-")
classs=input("Class-")
sec=input("Section-")
print("Enter Marks(Out of 100)-")
sub1=int(input("English-"))
sub2=int(input("Hindi-"))
sub3=int(input("SST-"))
sub4=int(input("Maths-"))
sub5=int(input("Science-"))
total=sub1+sub2+sub3+sub4+sub5
ptg=(total/500)*100
print("Results stats-")
print("Name--",name)
print("Class--",classs)
print("Section--",sec)
print("Percentage--",ptg)

#Question 2
print("-------------------------------")
a=int(input("a "))
b=int(input("b "))
c=int(input("c "))
print("Sum ",a+b+c)

#Question 3
print("-------------------------------")
d=int(input("d "))
print("Square ",d**2)

#Question 4
print("-------------------------------")
cel=input("Temperature(In celcius) ")
cel=float(cel)
fah=(cel*(9/5))+32
print("Temperature(In celcius) ",cel)
print("Temperature(In fahrenheit) ",fah)

#Question 5
print("-------------------------------")
x=int(input("x "))
y=int(input("y "))
print("Quotient" ,x//y)
print("Remainder ",x%y)
