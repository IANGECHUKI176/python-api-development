from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import time
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount(0)


@pytest.fixture
def hundred_bank_account():
    return BankAccount(100)


@pytest.mark.parametrize("num1, num2, result", [(2, 3, 5), (3, 4, 7), (5, 6, 11)])
def test_add(num1, num2, result):
    assert add(num1, num2) == result


def test_subtract():
    assert subtract(2, 3) == -1


def test_multiply():
    assert multiply(2, 3) == 6


def test_divide():
    assert divide(2, 3) == 0.6666666666666666


def test_bank_initial_balance(zero_bank_account):
    assert zero_bank_account.get_balance() == 0


def test_bank_deposit():
    account1 = BankAccount()
    account1.deposit(100)
    assert account1.get_balance() == 100


def test_bank_withdraw(hundred_bank_account):
    hundred_bank_account.withdraw(50)
    assert hundred_bank_account.get_balance() == 50


def test_bank_get_interest(hundred_bank_account):
    hundred_bank_account.collect_interest()
    assert hundred_bank_account.get_balance() == 101


@pytest.mark.parametrize("deposit, withdraw, result", [(100, 50, 50), (100, 100, 0)])
def test_bank_transaction(zero_bank_account, deposit, withdraw, result):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.get_balance() == result


def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds) as e:
        zero_bank_account.withdraw(100)
