# Use Cases
from domain.models import User, Group, Expense, ExpenseShare
from application.ports import UserRepository, GroupRepository, ExpenseRepository

# USERS

def create_user(user_repo: UserRepository, username: str) -> User:
    existing = user_repo.get_by_username(username)
    if existing:
        raise ValueError(f"Username '{username}' already taken.")
    new_user = User(id=0, username=username)
    user_repo.add(new_user)
    return new_user


# GROUPS

def create_group(group_repo: GroupRepository, name: str, owner: User) -> Group:
    group = Group(id=0, name=name, members=[owner])
    group_repo.add(group)
    return group

def add_user_to_group(group_repo: GroupRepository, group_id: int, user: User):
    group = group_repo.get_by_id(group_id)
    if user in group.members:
        raise ValueError("User is already in the group")
    group_repo.add_user_to_group(group_id, user.id)


# EXPENSES
from domain.models import Expense, ExpenseShare

def create_expense(
    expense_repo: ExpenseRepository,
    group_repo: GroupRepository,
    group_id: int,
    description: str,
    total_amount: float,
    creditor_shares: list[ExpenseShare],
    debtor_shares: list[ExpenseShare],
) -> Expense:
    group = group_repo.get_by_id(group_id)
    if not group:
        raise ValueError("Group not found")

    expense = Expense(
        id=0,
        description=description,
        total_amount=total_amount,
        group_id=group_id,
        creditors=creditor_shares,
        debtors=debtor_shares,
    )
    expense_repo.add(expense)
    return expense

def calculate_user_balance(
    expense_repo: ExpenseRepository,
    group_id: int,
    user_id: int
) -> float:
    expenses = expense_repo.list_by_group(group_id)
    balance = 0.0

    for expense in expenses:
        for creditor in expense.creditors:
            if creditor.user_id == user_id:
                balance += creditor.amount
        for debtor in expense.debtors:
            if debtor.user_id == user_id:
                balance -= debtor.amount

    return balance
