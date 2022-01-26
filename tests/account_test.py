import pytest

@pytest.fixture
def zero_bank_account():
  return BankAccount()


@pytest.fixture
def bank_account():
  return BankAccount(50)


def add(num1:int, num2:int):
  return num1 + num2


def subtract(num1:int, num2:int):
  return num1 - num2


def multiply(num1:int, num2:int):
  return num1 * num2


def divide(num1:int, num2:int):
  return num1 / num2      


class BankAccount():
  def __init__(self, starting_balance=0) -> None:
      self.balance = starting_balance

  def deposit(self, amount):
    self.balance += amount

  def withdraw(self, amount):
    if amount > self.balance:
      raise Exception("Insufficient funds in account")
    self.balance -= amount

  def collect_interest(self):
    self.balance *= 1.1      


@pytest.mark.parametrize("x, y, z", [
  (3,5,8),
  (12,5,17),
  (3,7,10)
])
def test_add(x, y, z):
  assert add(x,y) == z


def test_subtract():
  result = subtract(5,7)
  assert result == -2


def test_multiply():
  result = multiply(5,7)
  assert result == 35


def test_divide():
  result = divide(25, 5)
  assert result == 5
  

def test_create_bank_account(bank_account):
  assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
  assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
  bank_account.withdraw(20)
  assert bank_account.balance == 30


def test_deposit(bank_account):
  bank_account.deposit(20)
  assert bank_account.balance == 70  


def test_collect_interest(bank_account):
  bank_account.collect_interest()
  assert round(bank_account.balance, 2) == 55


@pytest.mark.parametrize("x, y, z", [
  (300,50,250),
  (120,50,70),
  (300,70,230)
])
def test_bank_transaction(zero_bank_account, x, y, z):
  zero_bank_account.deposit(x)
  zero_bank_account.withdraw(y)
  assert zero_bank_account.balance == z


def test_insufficient_funds(bank_account):
  with pytest.raises(Exception):
    bank_account.withdraw(200)
