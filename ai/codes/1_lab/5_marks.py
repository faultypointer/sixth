def marks(n):
    return [float(mark) for mark in input(f"Enter marks of {n} students: ").split()]

if __name__ == "__main__":
    marks = marks(10)
    print("Marks of 10 students: ")
    for i in range(10):
        print(f"Mark of student {i+1}: {marks[i]}")
