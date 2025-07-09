# Use Cases
from click import group
from domain.models import User, Group, Expense, Member
from application.ports import UserRepository, GroupRepository, ExpenseRepository, MemberRepository

# USERS

def create_user(user_repo: UserRepository) -> User:
    new_user = User(id=0)
    user_repo.add(new_user)
    return new_user

def get_user_by_id(user_repo: UserRepository, user_id: int) -> User:
    user = user_repo.get_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    return user

# MEMBERS

def create_member(member_repo: MemberRepository, username: str, group_id: str) -> Member:
    new_member = Member(id=0, username=username, group_id=group_id)
    member_repo.add(new_member, group_id)
    return new_member

def get_member_by_id(member_repo: MemberRepository, member_id: int, group_id: str) -> Member:
    member = member_repo.get_by_id(member_id, group_id)
    if not member:
        raise ValueError("Member not found")
    return member

# GROUPS

def get_group_by_id(group_repo: GroupRepository, group_id: str) -> Group:
    group = group_repo.get_by_id(group_id)
    if not group:
        raise ValueError("Group not found")
    return group

def create_group(group_repo: GroupRepository, name: str, owner: User) -> Group:
    group = Group(id="", name=name, owners=[owner])
    group_repo.add(group)
    group_repo.add_owner(group.id, owner)
    return group

def add_owner_to_group(group_repo: GroupRepository, group_id: str, owner: User):
    group = get_group_by_id(group_repo, group_id)
    if owner in group.owners:
        raise ValueError("Owner is already in the group")
    group_repo.add_owner(group_id, owner)

def add_member_to_group(group_repo: GroupRepository, group_id: str, member: Member):
    group = get_group_by_id(group_repo, group_id)
    group_repo.add_member(group_id, member)

def remove_member_from_group(group_repo: GroupRepository, expense_repo: ExpenseRepository, group_id: str, member: Member):
    group = get_group_by_id(group_repo, group_id)
    if member not in group.members:
        raise ValueError("Member is not in the group")
    expenses = expense_repo.list_by_group(group_id)
    for expense in expenses:
        if member in expense.creditors:
            raise ValueError("Member is in an expense of the group")
        if member in expense.debtors:
            raise ValueError("Member is in an expense of the group")
    group_repo.remove_member(group_id, member)


# EXPENSES
from domain.models import Expense

def create_expense(
    expense_repo: ExpenseRepository,
    group_repo: GroupRepository,
    group_id: str,
    description: str,
    total_amount: float,
    creditor_shares: list[tuple[Member, float]],
    debtor_shares: list[Member],
) -> Expense:
    group = get_group_by_id(group_repo, group_id)
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
    group_id: str,
) -> dict[Member, float]: # member -> balance
    expenses = expense_repo.list_by_group(group_id)
    members = group_repo.get_members(group_id)
    balances = {member: 0.0 for member in members}

    # Calculate balances for each member
    for expense in expenses:
        for creditor, creditor_amount in expense.creditors:
            balances[creditor] += creditor_amount
        for debtor in expense.debtors:
            balances[debtor] -= expense.total_amount / len(expense.debtors)
        
    return balances

def calculate_payments(balances: dict[Member, float]) -> list[tuple[Member, Member, float]]:
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

def _split_group_creditors_and_debtors(balances: dict[Member, float]) -> tuple[list[tuple[Member, float]], list[tuple[Member, float]]]:
    creditors = []
    debtors = []
    for member, balance in sorted(balances.items(), key=lambda item: item[1], reverse=True):
        if balance > 0:
            creditors.append((member, balance))
        else:
            debtors.append((member, -balance))
    return creditors, debtors

def _insert_ordered(lst: list[tuple[Member, float]], item: tuple[Member, float]):
    for i, (_, balance) in enumerate(lst):
        if balance > item[1]:
            lst.insert(i, item)
            return
    lst.append(item)
