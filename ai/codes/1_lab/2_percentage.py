def division(percentage):
    if percentage < 40:
        return "Fail"
    elif percentage < 55:
        return "Third Division"
    elif percentage < 65:
        return "Second Division"
    elif percentage < 80:
        return "First Division"
    else:
        return "Distinction"

if __name__ == "__main__":
    percentage = float(input("Enter your percentage: "))
    print("Your division: ", division(percentage))
