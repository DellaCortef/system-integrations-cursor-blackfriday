print("Hello World")

def fibbonaci_function(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibbonaci_function(n-1) + fibbonaci_function(n-2)

print(fibbonaci_function(10))