import pytest
from domain.models import User, Expense
from domain.services import calculate_group_balance
from tests.mocks import MockExpenseRepository, MockGroupRepository

# Utils to create users
def make_users(names):
    return [User(id=i+1, username=name) for i, name in enumerate(names)]

# Test 1: No expenses
def test_balance_empty_group():
    users = make_users(["alice", "bob"])
    group_repo = MockGroupRepository(users)
    expense_repo = MockExpenseRepository([])

    balances = calculate_group_balance(expense_repo, group_repo, group_id=1)
    assert all(balance == 0.0 for balance in balances.values())

# Test 2: 1 expense, 1 creditor, 1 debtor
def test_one_creditor_one_debtor():
    [alice, bob] = make_users(["alice", "bob"])
    expense = Expense(
        id=1, description="Taxi", total_amount=60.0, group_id=1,
        creditors=[(alice, 60.0)],
        debtors=[bob]
    )
    group_repo = MockGroupRepository([alice, bob])
    expense_repo = MockExpenseRepository([expense])

    balances = calculate_group_balance(expense_repo, group_repo, group_id=1)
    assert balances[alice] == 60.0
    assert balances[bob] == -60.0

# Test 3: 1 creditor, multiple debtors
def test_one_creditor_multiple_debtors():
    [alice, bob, carol] = make_users(["alice", "bob", "carol"])
    expense = Expense(
        id=1, description="Pizza", total_amount=90.0, group_id=1,
        creditors=[(alice, 90.0)],
        debtors=[alice, bob, carol]
    )
    group_repo = MockGroupRepository([alice, bob, carol])
    expense_repo = MockExpenseRepository([expense])

    balances = calculate_group_balance(expense_repo, group_repo, group_id=1)
    assert balances[alice] == 60.0
    assert balances[bob] == -30.0
    assert balances[carol] == -30.0

# Test 4: multiple creditors, multiple debtors
def test_multiple_creditors_multiple_debtors():
    [alice, bob, carol, dave] = make_users(["alice", "bob", "carol", "dave"])
    expense = Expense(
        id=1, description="Pizza", total_amount=90.0, group_id=1,
        creditors=[(alice, 30.0), (bob, 60.0)],
        debtors=[alice, bob, carol, dave]
    )
    group_repo = MockGroupRepository([alice, bob, carol, dave])
    expense_repo = MockExpenseRepository([expense])

    balances = calculate_group_balance(expense_repo, group_repo, group_id=1)
    assert balances[alice] == 7.5
    assert balances[bob] == 37.5
    assert balances[carol] == -22.5
    assert balances[dave] == -22.5