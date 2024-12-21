class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.__balance = initial_balance
        self.__account_number = account_number

    def deposit(self, amount):
        print(f"You are depositing Rs. {amount} into your account.")
        self.__balance += amount
        print(f"Your total balance now is Rs. {self.__balance}")

    def withdraw(self, amount):
        if (self.__balance < amount):
            print(f"Insufficient balance in your account.")
            return
        print(f"You are withdraw Rs. {amount} from your account.")
        self.__balance -= amount
        print(f"Your remaining balance now is Rs. {self.__balance}")


acc = BankAccount(213235532)
acc.deposit(1000)
acc.withdraw(400)

