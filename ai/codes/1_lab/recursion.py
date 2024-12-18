def factorial(n):
    if n < 2:
        return n
    return factorial(n-1) * n

def fibonacci(n):
    n1, n2 = 0, 1
    for i in range(n):
        temp = n1 + n2
        n1 = n2
        n2 = temp

    return n1
