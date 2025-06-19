#Question1
d1={}
a=int(input("How many elements u=you want to enter: "))
for i in range(0,a):
    key=input('Key ')
    value=input('Value ')
    d1.update({key:value}) 
print(d1)

#Question2
print("------------------------------------")
employee_details = {23: {'name': 'John','department': 'HR','salary': 70000}
, 45: {'name': 'Alice','department': 'Finance','salary': 23000}, 67: {'name': 'Bob','department': 'IT','salary': 75000}
, 89: {'name': 'Charlie','department': 'Marketing','salary': 40000}}

l = [i['name'] for i in employee_details.values() if i['salary'] > 50000]
print(l)

#Question3
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

#Question4
print("------------------------------------")
price = float(input("Enter the price of the product: "))
if price>1000:
        discount= 0.1
elif price>1000 and price<1000:
        discount = 0.05
elif price<500:
        discount=0
discounted_price = price - (price * discount)
print("The original price is: ", price)
print("The discounted price is: ",discounted_price)

#Question5
print("------------------------------------")
passw=input("Enter your password: ")
while True:
    if len(passw) < 8:
        print("Password must be at least 8 characters long.")
        passw = input("Enter your password again: ")
    elif not any(char.isdigit() for char in passw):
        print("Password must contain at least one digit.")
        passw = input("Enter your password again: ")
    elif not any(char.isupper() for char in passw):
        print("Password must contain at least one uppercase letter.")
        passw = input("Enter your password again: ")
    elif not any(char.islower() for char in passw):
        print("Password must contain at least one lowercase letter.")
        passw = input("Enter your password again: ")
    elif not any(char in '!@#$%^&*()_+' for char in passw):
        print("Password must contain at least one special character (!@#$%^&*()_+).")
        passw = input("Enter your password again: ")
    else:
        print("Password is valid.")
        break

#Question6
print("------------------------------------")
li=[20,30,40,[57,66,30,[70,80],"Hello"],50,True]
print(li)
li[3][3].insert(1,76)
li[3].insert(1,88)
print(li)

#Question7
print("------------------------------------")
budget=int(input("Enter your budget for trip(5000-10000, 10000-20000, 20000-30000, 30000-40000): "))
if 5000 <= budget < 10000:
    print("You can go for a local trip or a short weekend getaway.")
elif 10000 <= budget < 20000:
    print("You can plan a trip to a nearby city or a longer weekend getaway.")
elif 20000 <= budget < 30000:
    print("countries available for you are: India,Thailand, Malaysia.")
    choice= input("Enter your choice of country from the above list: ")
    if choice=="India":
        print("You can visit Delhi, Mumbai, or Bangalore.") 
    elif choice=="Thailand":
        print("You can visit Bangkok, Phuket, or Chiang Mai.")
    elif choice=="Malaysia":
        print("You can visit Kuala Lumpur, Penang, or Langkawi.")
    else:
        print("Invalid choice. Please choose from the available countries.")
elif 30000 <= budget < 40000:
    print("countries available for you are: Indonesia, Vietnam,Singapore, Dubai.")
    choice= input("Enter your choice of country from the above list: ")
    if choice=="Indonesia":
        print("You can visit Bali, Yogyakarta, or Jakarta.")
    elif choice=="Vietnam":
        print("You can visit Hanoi, Ho Chi Minh City, or Da Nang.")
    elif choice=="Singapore":
        print("You can visit Marina Bay Sands, Sentosa Island, or Gardens by the Bay.")
    elif choice=="Dubai":
        print("You can visit Burj Khalifa, Dubai Mall, or Palm Jumeirah.")
    else:
        print("Invalid choice. Please choose from the available countries.")
else:
    print("Please enter a valid budget within the specified ranges (5000-40000).")

