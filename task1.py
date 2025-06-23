#Task1
print("----------------------------------------")
print("Welcome to CodeRail Railway Booking System ")
name=input("\nEnter your name: ")
age=int(input("Enter your age: "))
final_price = 0
classes={1: "First Class", 2: "Second Class", 3: "Third Class"}
print("\nclasses available:")
print("1. First Class - Rs. 1500")
print("2. Second Class - Rs. 1000") 
print("3. Third Class - Rs. 500") 
c=input("Choose a travel class(1/2/3): ")
if c == '1':
    final_price = 1500
elif c == '2':
    final_price = 1000
elif c == '3':
    final_price = 500
else:
    print("Invalid choice. Please restart the program and choose a valid class.")
    exit()
if age<5:
    final_price = 0
elif age>60:
    final_price = final_price * 0.8
else:
    final_price = final_price

meal=input("Do you want to add a meal? (yes/no): ")
if meal == 'yes':
    final_price += 200
elif meal == 'no':
    final_price = final_price
else:
    print("Invalid choice for meal. Please restart the program and choose 'yes' or 'no'.")
    exit()
print("-----------------------------------------")
print("Ticket Summary: ")
print("Name: ",name)
print("Age: ",age)    
print("Travel Class: ",classes[int(c)])
print("Meal Included: ",meal)
print("Final Price: ", final_price)
print("Enjoy your journey")

#Task2
print("----------------------------------------")
print("WELCOME TO BURGER KING  ")
print("\nMenu:")
print("1. Whopper Burger - Rs. 150")
print("2. Crispy Veg - Rs. 100")
print("3. Chicken Wings - Rs. 120")
d={1: "Whopper Burger", 2: "Crispy Veg", 3: "Chicken Wings"}
c=input("Enter the item number(1/2/3): ")
if c == '1':
    price = 150
elif c == '2':
    price = 100
elif c == '3':
    price = 120
else:
    print("Invalid choice. Please restart the program and choose a valid item.")
    exit()
q=int(input("Enter the quantity: "))


price = price * q
print("-----------------------------------------")
dis = "No discount"
code=input("Do you have a coupon code? (yes/no): ")
if code == 'yes':
    coupon = input("Enter the coupon code: ")
    if coupon == "KING50":
        dis= "50% off"
        dprice = price * 0.5
    elif coupon == "BK20":
        dis = "Rs. 20 off"
        dprice = price - 20
    else:
        print("Invalid coupon code. No discount applied.")
elif code == 'no':
    dprice = price
else:
    print("Invalid choice for coupon code. Please restart the program and choose 'yes' or 'no'.")
    exit()

print("-----------------------------------------")
print("Order Summary: ")
print("Item: ", d[int(c)])
print("Quantity: ", q)
print("Original Price: Rs.", price)
print("Discount: ", dis)
print("Final Price after discount: Rs.", dprice)
print("Thank you for ordering with us!")