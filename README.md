# Mini Banking System

## Overview
This project implements a simple banking backend using Object Oriented Programming (OOP) in Python.

It supports:

- Opening accounts
- Depositing money
- Withdrawing money
- Transferring money
- Viewing transaction history

The project demonstrates core OOP concepts such as encapsulation, inheritance, polymorphism, and abstraction.

---

## Project Structure

mini-banking-system
│
├── src
│   └── banking.py
│
├── tests
│   └── test_banking.py
│
├── cli.py
│
└── README.md

---

## OOP Design

### Encapsulation
Balance is stored in a private variable `__balance`.

### Inheritance
SavingsAccount and CurrentAccount inherit from Account.

### Polymorphism
Each account type overrides the withdraw() method.

### Abstraction
Account defines the common interface for all accounts.

---

## Business Rules

- Deposit amounts must be positive.
- Transfers cannot be to the same account.
- Savings accounts cannot go below zero.
- Current accounts can overdraft up to the overdraft limit.

---

## Running the CLI

Run the banking menu:

---

## Running Unit Tests

Run all tests using:

or

---

## Test Coverage

The unit tests check:

- Deposit functionality
- Savings overdraft rejection
- Current overdraft within limit
- Current overdraft exceeding limit
- Transfer functionality
- Transfer atomicity
- Statement history growth
- Duplicate account prevention
- Account lookup

Total tests: **10**