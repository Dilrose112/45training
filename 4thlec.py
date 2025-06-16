#Question1
str=input("Enter a string: ")
if(len(str)<2):
    print("Not a valid String")
else:
    print(str[0:2]+str[len(str)-2:len(str)])

#Question2
print("---------------------------------------------------")
str1=input("Enter a string: ")
str2=input("Enter a string: ")
print("Concatenated String:",str2[0:1]+str1[1:len(str1)]+' '+str1[0:1]+str2[1:len(str2)])

#Question3
print("---------------------------------------------------")
str3=input("Enter a string: ")
if(len(str3)<3):
    print("Not a valid String")
else:
    if(str3[len(str3)-3:len(str3)]=='ing'):
        print(str3+'ly')
    else:
        print(str3+'ing')





        