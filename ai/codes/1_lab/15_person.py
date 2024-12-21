import datetime
class Person:
    def __init__(self, name, country, dob):
        self.name = name
        self.country = country
        self.dob = dob

    def age(self):
        year, month, day = [int(value.strip()) for value in self.dob.split('/')]
        delta =  datetime.date.today() - datetime.date(year, month, day)
        return delta.days // 365, delta.days % 365


name = input("Enter your name: ")
country = input("Enter your country: ")
dob = input("Enter your date of birth (yyyy/mm/dd): ")

person = Person(name, country, dob)
year, days = person.age()
print(f"Your age is: {year} years, {days} days.")

