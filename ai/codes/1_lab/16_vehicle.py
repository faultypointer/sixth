class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model


    def drive(self):
        print(f"Driving the {self.make} {self.model}")


class Car(Vehicle):
    def __init__(self, make, model):
        super().__init__(make, model)

    def drive(self):
        print(f"Driving the {self.make} {self.model} car")


vmake = input("Enter your Vehicle's make: ")
vmodel = input("Enter your Vehicle's model: ")
cmake = input("Enter your Car's make: ")
cmodel = input("Enter your Car's model: ")


veh = Vehicle(vmake, vmodel)
veh.drive()
car = Car(cmake, cmodel)
car.drive()

