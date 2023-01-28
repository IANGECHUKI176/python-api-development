def add(a: int, b: int):
    return a + b


def multiply(x, y):
    return x * y


def divide(x, y):
    return x / y


def subtract(x, y):
    return x - y


class InsufficientFunds(Exception):
    pass


class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        if self.balance < amount:
            raise InsufficientFunds("Insufficient funds")
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance

    def collect_interest(self):
        self.balance *= 1.01
