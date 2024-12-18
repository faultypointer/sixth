# def swap_cases(string: str):
#     for i, char in enumerate(string):
#         if char.islower():
#             string[i] = char.upper()
#         elif char.isupper():
#             string

string = input("Enter something: ")
print(f"Case swapped: {string.swapcase()}")
