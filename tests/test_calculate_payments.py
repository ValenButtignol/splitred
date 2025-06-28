import pytest
from domain.models import User
from domain.services import calculate_payments

def make_users(names):
    return [User(id=i+1, username=name) for i, name in enumerate(names)]

# Test 1: No payments needed
def test_no_payments_needed():
    [alice, bob] = make_users(["alice", "bob"])
    balances = {alice: 0.0, bob: 0.0}
    payments = calculate_payments(balances)
    assert payments == []

# Test 2: Single debt
def test_single_debt():
    [alice, bob] = make_users(["alice", "bob"])
    balances = {
        alice: 50.0,  # debtor
        bob: -50.0,   # creditor
    }
    payments = calculate_payments(balances)
    assert payments == [(alice, bob, 50.0)]

# Test 3: Debtor pays to multiple creditors
def test_debtor_pays_two_creditors():
    [alice, bob, carol] = make_users(["alice", "bob", "carol"])
    balances = {
        alice: 30.0,
        bob: 70.0,
        carol: -100.0,
    }
    payments = calculate_payments(balances)
    assert (alice, carol, 30.0) in payments
    assert (bob, carol, 70.0) in payments
    assert len(payments) == 2

# Test 4: Multiple debtors and creditors
def test_multiple_creditors_and_debtors():
    [alice, bob, carol, dave] = make_users(["alice", "bob", "carol", "dave"])
    balances = {
        alice: 60.0,   # creditor
        bob: 40.0,     # creditor
        carol: -50.0,  # debtor
        dave: -50.0,   # debtor
    }
    payments = calculate_payments(balances)
    assert (alice, carol, 50.0) in payments
    assert (alice, dave, 10.0) in payments
    assert (bob, dave, 40.0) in payments
    assert len(payments) == 3

# Test 5: Cases with decimals
def test_floating_point_precision():
    [alice, bob, carol] = make_users(["alice", "bob", "carol"])
    balances = {
        alice: 33.33,
        bob: 33.33,
        carol: -66.66
    }
    payments = calculate_payments(balances)
    assert (alice, carol, 33.33) in payments
    assert (bob, carol, 33.33) in payments
    assert len(payments) == 2

# Test 6: Multiple payments
def test_multiple_payments():
    [alice, bob, carol, jason, mike] = make_users(["alice", "bob", "carol", "jason", "mike"])
    balances = {
        alice: 100.0,
        bob: 130.0,
        carol: -70.0,
        jason: -105.0,
        mike: -55.0,
    }
    payments = calculate_payments(balances)
    assert (bob, mike, 55.0) in payments
    assert (bob, carol, 70.0) in payments
    assert (bob, jason, 5.0) in payments
    assert (alice, jason, 100.0) in payments
    assert len(payments) == 4