#types
age = 20
price = 19.95
first_name = "Dana"
is_online = False
print (is_online)
#float(), bool(), int(), str()


name = input ("What is your name?")
print("Hello " + name)
#type conversion
birth_year = input ("Enter your birth year: ")
age = 2024 - int(birth_year)
print(age)


------------------------------------------
first = input ("first: ")
second = input ("second: " )
sum = float(first) + float(second)
print (sum)

first = input ("first: ")
second = input ("second"  )
sum = int(first) + int(second)
print (sum)


first = input("first: ")
second = input("second: ")
sum = float(first) + float(second)
print("Sum: " + str(sum))
#OR
first = float(input("First: "))
second = float(input("Second: "))
sum = first + second
print(sum)
----------------------------------------

course = 'python for beginners'
print(course.upper())
print(course)
print(course.find('P'))
print(course.replace('for','dana'))
print('python' in course)

-----------------------------------------

#arithmetic operators
print(1 + 1)
print(1 - 1)
print(2 * 2)
print(25/2) #result with decimals
print(25//2) #result rounded, no decimals
print(10 % 3)
print(10 ** 3)

x = 10
x = x + 3
print(x)
x += 3  #augmented assignment operator
print(x)
x = 10 + 3 * 2
print(x)
x = (10 + 3) * 2
print(x)

#comparison operators
x = 3 > 2
print(x)
x = 2 >= 2
print(x)
x = 2 <= 2
print(x)
x = 2 == 2
print(x)
x = 3 != 2
print(x)


#logicaloperators

**and** returns true if both expressions are true
**or** returns true if at least one expression is true
**not** inverses any value

price = 25
print(price > 100)   *False*
print(not price > 100)  *True*
print(price > 10 and price < 30)  *True*
print(price > 10 or price < 30)   *True*

--------------------------------------------------------------------------
IF statements

temperature = 11  
if temperature > 30:  
    print("It's a hot day")  
    print("Drink water")  
elif temperature > 20:  
    print("It's a nice day")  
elif temperature > 10:  
    print("Yay")