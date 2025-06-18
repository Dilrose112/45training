#Question1
t1=(3,34,93,27,'Hi','Hello',True,False,9,34,98,'Hello',False,3)
print("Original tuple:", t1)
t1=set(t1) 
t1=tuple(t1)     
print("After removing duplicates:", t1)

#Question2
print("-------------------------------------------")
l1=[[1,2,3],[4,5,6],[7,8,9]]
l1=[j for i in l1 for j in i]
print("Flattened list:", l1)

#Question3
print("-------------------------------------------")    
t2=(3,56,21,43,98,11,56,78,90,12,34)
t2=sorted(t2)
print("Min=", t2[0])
print("Max=", t2[-1])

#Question4
print("-------------------------------------------")
l2=[(i,i**3) for i in range(1,6)]
print("Required list", l2)