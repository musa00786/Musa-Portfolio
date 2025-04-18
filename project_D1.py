# Code 1: Reverse a String

def reverse_string(s):
    return s[::-1]
print(reverse_string("KhaledMahbub")) 

# Code 2: Find factorial using recursion

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
print(factorial(5))  

# Code 3: Check for Prime Number

def is_prime(n):
    if n < 2:
        return False

    for i in range(2, n):
        if n % i == 0:  
            return False

    return True  
print(is_prime(7))  
print(is_prime(4))   


# Code 4: Count Words in a File

def count_words(filename):
    try:
        file = open(filename, "r")  
        text = file.read()  
        file.close()  
        words = text.split()  
        return len(words)  

    except FileNotFoundError:
        return "The file does not exist."  
print(count_words("sample.txt"))  
 

# Code 5: Class for Employee Management (OOP)

class Employee:
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary
    def display(self):
        print(f"Name: {self.name}, Age: {self.age}, Salary: ${self.salary}")
emp = Employee("KhaledMahbub", 22, 50000)
emp.display()

# Code 6: Handling Division by Zero (Exception Handling)

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero!"
print(safe_divide(10, 2))  
print(safe_divide(10, 0))  
