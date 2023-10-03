from app.calculations import add, BankAccount
import pytest

@pytest.mark.parametrize("num1, num2, expected", [(3,2,5),(1,1,2),(12,13,25)])
def test_add(num1,num2,expected):
    sum = add(num1,num2)
    assert sum == expected

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

def test_bank_set_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_insufficent_funds(zero_bank_account):
  #  with pytest.raises(Exception):
    zero_bank_account.withdraw(20)

def test_bank_withdraw_amount():
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30