#Question1
print("----------------------------------------")
for i in range(1,51):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

#Question2
print("----------------------------------------")
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

for i in range(101):
    if is_prime(i):
        print(i)

#Question3
print("----------------------------------------")
def grading_system(score):
    if score < 0 or score > 100:
        return "Invalid score"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

n= int(input("Enter the number of score: "))
print(grading_system(n))

#Question4
print("----------------------------------------")
def table(n):
    for i in range(1, 11):
        print(i*n)
n = int(input("Enter a number to print its multiplication table: "))
table(n)

#Question5
print("----------------------------------------")
li=[i**2 for i in range(1, 21)]
print("List of squares from 1 to 20:", li)

#Question6
print("----------------------------------------")
def leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

year = int(input("Enter a year to check if it is a leap year: "))
if leap_year(year):
    print("Leap year.")
else:
    print("Not a leap year.")

#Question7
print("----------------------------------------")
def check_triangle_type(a, b, c):
    if a + b > c and a + c > b and b + c > a:
        if a == b == c:
            return "Equilateral triangle"
        elif a == b or b == c or a == c:
            return "Isosceles triangle"
        elif c**2 == a**2 + b**2 or a**2 == b**2 + c**2 or b**2 == a**2 + c**2:
            return "Right triangle"
        else:
            return "Scalene triangle"
    else:
        return "Not a triangle"
    
a = int(input("Enter the first side of the triangle: "))
b = int(input("Enter the second side of the triangle: "))   
c = int(input("Enter the third side of the triangle: "))
print(check_triangle_type(a, b, c))
#Question8
print("----------------------------------------")
def number(n):
    if n < 0:
        return "Negative number"
    elif n == 0:
        return "Zero"
    else:
        return "Positive number"
n = int(input("Enter a number: "))
print(number(n))
#Question9
print("----------------------------------------")
passw=input("Enter your password: ")
strength=0
if len(passw) > 8:
     strength += 1
if any(char.isdigit() for char in passw):
     strength += 1
if any(char.isupper() for char in passw):
        strength += 1
if any(char.islower() for char in passw):
        strength += 1
if any(char in '!@#$%^&*()_+' for char in passw):
        strength += 1
if strength == 5:
    print("Password is strong") 
elif(strength<5 and strength>=3):
    print("Password is medium")
else:
    print("Password is weak, please try again")

#Question10
print("----------------------------------------") 
def bmi(weight, height):
    bmi_value = weight / (height ** 2)
    if bmi_value < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_value < 24.9:
        return "Normal weight"
    elif 25 <= bmi_value < 29.9:
        return "Overweight"
    else:
        return "Obesity"

weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in meters: "))
print("Your BMI category is:", bmi(weight, height))

#Question11
print("----------------------------------------")
def days(n):
    if n < 1 or n > 7:
        return "Invalid input."
    days_of_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days_of_week[n-1]
n = int(input("Enter a number(1-7): "))
print(days(n))

#Question12
print("------------------------------------")
price = float(input("Enter the price of the product: "))
if price>1000:
        discount= 0.1
elif price>500 and price<1000:
        discount = 0.05
elif price<500:
        discount=0
discounted_price = price - (price * discount)
print("Discount: ", discount)
print("The discounted price is: ",discounted_price)


#Question13
print("------------------------------------")
n= int(input("Enter a natural number: "))
sum=0
for i in range(1, n + 1):
    sum += i
print("Sum: ", sum)

#Question14
print("------------------------------------")
employee_details = {23: {'name': 'John','department': 'HR','salary': 70000}
, 45: {'name': 'Alice','department': 'Finance','salary': 23000}, 67: {'name': 'Bob','department': 'IT','salary': 75000}
, 89: {'name': 'Charlie','department': 'Marketing','salary': 40000}}

l = [i['name'] for i in employee_details.values() if i['salary'] > 50000]
print(l)

#Question15
print("------------------------------------")
def vowel_count(s):
    vowels = "aeiouAEIOU"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

s = input("Enter a string: ")
print("Number of vowels:", vowel_count(s))

#Question16
print("------------------------------------")
def dig_sum(n):
    sum = 0
    if n < 0:
        n = -n
    for digit in str(n):
        sum += int(digit)
    return sum
n = int(input("Enter a number: "))
print("Sum of digits:", dig_sum(n))
#Question17
print("------------------------------------")
def seq(n):
    for i in range(0,n):
        for j in range(0,i+1):
            print("*",end='')
        print()
n=int(input("Enter a number: "))
seq(n)
#Question18
print("------------------------------------")
import random
n=random.randint(1, 100)
guess=0
while guess!=n:
    guess = int(input("Enter your guess: "))
    if guess < n:
        print("Too low! Try again.")
    elif guess > n:
        print("Too high! Try again.")
    else:
        print("Congratulations! You've guessed the number!")

#Question19
print("------------------------------------")
n= int(input("Enter a number: "))
for i in range(1,n):
    if i%2==0:
        print(i, end=' ')
#Question20
print("------------------------------------")
li=[23,67,84,34,98,12,45,67,89,90]
print(li)
print(25 in li)
print(len(li))
print(li.count(25))
for i in li:
    if i % 2 == 0:
        print(i, end=' ')
#Question21
print("------------------------------------")
str=input("Enter a string(10-19 words): ")
print(str)
print(len(str))
str1=str[::-1]
if str == str1:
    print("The string is a palindrome.")
else:
    print("The string is not a palindrome.")
print(str[len(str)//2])
print(str[-2])

#Question22
print("------------------------------------")
def calculator(choice):
    if choice==1:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        print("Sum:", a + b)
    elif choice==2:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        print("Difference:", a - b)
    elif choice==3:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        print("Product:", a * b)
    elif choice==4:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        if b != 0:
            print("Quotient:", a / b)
        else:
            print("Cannot divide by zero.")

print("Calculator Menu:")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
choice = int(input("Enter your choice (1-4): "))
calculator(choice)

#Question23
print("------------------------------------")
w=['fill','xyz','lullaby','fif','hello','world','python','programming','kik']
count = 0
for i in w:
    if len(i)>2 and i[0] == i[-1]:
        count += 1

print("Output:", count)
