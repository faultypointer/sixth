def odd_or_even(num):
    if num % 2 == 0:
        return "even"
    else:
        return "odd"


if __name__ == "__main__":
    num = int(input("Please enter a number: "))
    print("number is ", odd_or_even(num))
    
