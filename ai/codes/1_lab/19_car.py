class Engine:
    def __init__(self, engine_type):
        self.type = engine_type

    def start(self):
        print(f"{self.type} engine started.")

    def stop(self):
        print(f"{self.type} engine stopped.")


class Wheel:
    def __init__(self, wheel_type):
        self.type = wheel_type

    def start(self):
        print(f"{self.type} wheel is rolling.")

    def stop(self):
        print(f"{self.type} wheel stopped.")


class Car:
    def __init__(self, engine_type, wheel_type):
        self.engine = Engine(engine_type)
        self.wheels = [Wheel(wheel_type) for _ in range(4)]

    def start_car(self):
        self.engine.start()
        for wheel in self.wheels:
            wheel.start()
        print("Car started.")


my_car = Car("V8", "Alloy")
my_car.start_car()
