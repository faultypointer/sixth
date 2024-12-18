def arithmetics(x, y):
    summ = x + y
    diff = x-y
    product = x * y
    quotient = x // y
    return summ, diff, product, quotient

if __name__ == "__main__":
    x = int(input("Enter a number: "))
    y = int(input("Enter another number: "))
    result = arithmetics(x, y);
    print(f"sum = {result[0]}")
    print(f"difference = {result[1]}")
    print(f"product = {result[2]}")
    print(f"quotient = {result[3]}")
