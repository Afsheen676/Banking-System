from __future__ import annotations
from datetime import date
from typing import Dict, List, Tuple

Txn = Tuple[str, str, float, float]


class Account:
    def __init__(self, account_id: str, owner: str):
        self.account_id = account_id
        self.owner = owner
        self.__balance: float = 0.0
        self._history: List[Txn] = []

    def _record(self, typ: str, amount: float) -> None:
        txn = (date.today().isoformat(), typ, amount, self.__balance)
        self._history.append(txn)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self._set_balance(self.__balance + amount)
        self._record("DEPOSIT", amount)

    def get_balance(self) -> float:
        return self.__balance

    def _set_balance(self, new_balance: float) -> None:
        self.__balance = new_balance

    def withdraw(self, amount: float) -> None:
        raise NotImplementedError

    def transfer(self, to: "Account", amount: float) -> None:
        if self.account_id == to.account_id:
            raise ValueError("Cannot transfer to same account")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.withdraw(amount)
        to.deposit(amount)

        self._record("TRANSFER_OUT", amount)
        to._record("TRANSFER_IN", amount)

    def statement(self) -> List[Txn]:
        return list(self._history)


class SavingsAccount(Account):

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")

        if self.get_balance() - amount < 0:
            raise ValueError("Savings account cannot overdraft")

        self._set_balance(self.get_balance() - amount)
        self._record("WITHDRAW", amount)


class CurrentAccount(Account):

    def __init__(self, account_id: str, owner: str, overdraft_limit: float = 5000.0):
        super().__init__(account_id, owner)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")

        new_balance = self.get_balance() - amount

        if new_balance < -self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded")

        self._set_balance(new_balance)
        self._record("WITHDRAW", amount)


class Bank:

    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def open_account(self, account: Account) -> None:
        if account.account_id in self.accounts:
            raise ValueError("Account ID already exists")

        self.accounts[account.account_id] = account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            raise KeyError("Account not found")

        return self.accounts[account_id]

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        from_acc = self.get_account(from_id)
        to_acc = self.get_account(to_id)

        from_acc.transfer(to_acc, amount)
        from src.banking import Bank, SavingsAccount, CurrentAccount

bank = Bank()

def menu():
    print("\nMini Banking System")
    print("1. Open Savings Account")
    print("2. Open Current Account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Transfer")
    print("6. Statement")
    print("7. Exit")

while True:

    menu()
    choice = input("Select option: ")

    try:

        if choice == "1":
            aid = input("Account ID: ")
            owner = input("Owner: ")
            bank.open_account(SavingsAccount(aid, owner))
            print("Savings account created")

        elif choice == "2":
            aid = input("Account ID: ")
            owner = input("Owner: ")
            limit = float(input("Overdraft limit: "))
            bank.open_account(CurrentAccount(aid, owner, limit))
            print("Current account created")

        elif choice == "3":
            aid = input("Account ID: ")
            amount = float(input("Amount: "))
            bank.get_account(aid).deposit(amount)

        elif choice == "4":
            aid = input("Account ID: ")
            amount = float(input("Amount: "))
            bank.get_account(aid).withdraw(amount)

        elif choice == "5":
            f = input("From Account: ")
            t = input("To Account: ")
            amount = float(input("Amount: "))
            bank.transfer(f, t, amount)

        elif choice == "6":
            aid = input("Account ID: ")
            acc = bank.get_account(aid)
            for txn in acc.statement():
                print(txn)

        elif choice == "7":
            break

    except Exception as e:
        print("Error:", e)
        import unittest
from src.banking import Bank, SavingsAccount, CurrentAccount


class TestBanking(unittest.TestCase):

    def setUp(self):

        self.bank = Bank()

        self.s1 = SavingsAccount("S1", "Ali")
        self.c1 = CurrentAccount("C1", "Sara", 5000)

        self.bank.open_account(self.s1)
        self.bank.open_account(self.c1)

    def test_deposit(self):
        self.s1.deposit(1000)
        self.assertEqual(self.s1.get_balance(), 1000)

    def test_savings_withdraw(self):
        self.s1.deposit(1000)
        self.s1.withdraw(500)
        self.assertEqual(self.s1.get_balance(), 500)

    def test_savings_overdraft_rejected(self):
        self.s1.deposit(500)

        with self.assertRaises(ValueError):
            self.s1.withdraw(600)

    def test_current_overdraft_within_limit(self):
        self.c1.deposit(1000)
        self.c1.withdraw(3000)
        self.assertEqual(self.c1.get_balance(), -2000)

    def test_current_overdraft_exceeded(self):
        with self.assertRaises(ValueError):
            self.c1.withdraw(6000)

    def test_transfer(self):
        self.s1.deposit(1000)
        self.bank.transfer("S1", "C1", 300)

        self.assertEqual(self.s1.get_balance(), 700)
        self.assertEqual(self.c1.get_balance(), 300)

    def test_transfer_atomic(self):
        self.s1.deposit(100)

        with self.assertRaises(ValueError):
            self.bank.transfer("S1", "C1", 200)

        self.assertEqual(self.c1.get_balance(), 0)

    def test_statement_history_increase(self):
        self.s1.deposit(100)
        self.s1.withdraw(50)

        self.assertEqual(len(self.s1.statement()), 2)

    def test_duplicate_account(self):
        with self.assertRaises(ValueError):
            self.bank.open_account(SavingsAccount("S1", "Test"))

    def test_account_lookup(self):
        acc = self.bank.get_account("S1")
        self.assertEqual(acc.owner, "Ali")


if __name__ == "__main__":
    unittest.main()