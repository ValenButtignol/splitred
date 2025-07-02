# Use Cases
from domain.models import User, Group, Expense
from application.ports import UserRepository, GroupRepository, ExpenseRepository

# USERS

def create_user(user_repo: UserRepository, username: str) -> User:
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
from domain.models import Expense

def create_expense(
    expense_repo: ExpenseRepository,
    group_repo: GroupRepository,
    group_id: int,
    description: str,
    total_amount: float,
    creditor_shares: list[tuple[User, float]],
    debtor_shares: list[User],
) -> Expense:
    group = group_repo.get_by_id(group_id)
    if not group:
        raise ValueError("Group not found")

    if sum(share for _, share in creditor_shares) != total_amount:
        raise ValueError("Total amount of creditors does not match the total amount of the expense")

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

def calculate_group_balance(
    expense_repo: ExpenseRepository,
    group_repo: GroupRepository,
    group_id: int,
) -> dict[User, float]: # user -> balance
    expenses = expense_repo.list_by_group(group_id)
    members = group_repo.get_members(group_id)
    balances = {user: 0.0 for user in members}

    # Calculate balances for each user
    for expense in expenses:
        for creditor, creditor_amount in expense.creditors:
            balances[creditor] += creditor_amount
        for debtor in expense.debtors:
            balances[debtor] -= expense.total_amount / len(expense.debtors)
        
    return balances

def calculate_payments(balances: dict[User, float]) -> list[tuple[User, User, float]]:
    creditors, debtors = _split_group_creditors_and_debtors(balances)
    payments = []
    
    while creditors and debtors:
        creditor, creditor_balance = creditors.pop(0)
        debtor, debtor_balance = debtors.pop(0)
        payment = min(creditor_balance, debtor_balance)
        if creditor_balance > debtor_balance:
            _insert_ordered(creditors, (creditor, creditor_balance - payment))

        if debtor_balance > creditor_balance:
            _insert_ordered(debtors, (debtor, debtor_balance - payment))

        payments.append((creditor, debtor, payment))
    
    return payments

def _split_group_creditors_and_debtors(balances: dict[User, float]) -> tuple[list[tuple[User, float]], list[tuple[User, float]]]:
    creditors = []
    debtors = []
    for user, balance in sorted(balances.items(), key=lambda item: item[1], reverse=True):
        if balance > 0:
            creditors.append((user, balance))
        else:
            debtors.append((user, -balance))
    return creditors, debtors

def _insert_ordered(lst: list[tuple[User, float]], item: tuple[User, float]):
    for i, (_, balance) in enumerate(lst):
        if balance > item[1]:
            lst.insert(i, item)
            return
    lst.append(item)
