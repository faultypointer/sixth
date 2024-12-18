def factorial(n):
    if n < 2:
        return n
    return factorial(n-1) * n

n = int(input("Enter a number: "))
fact = factorial(n)
print("Factorial of ", n, ": ", fact)
