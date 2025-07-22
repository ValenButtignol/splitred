# SQLAlchemy Implementations of Repository Interfaces

from uuid import UUID

from flask import session
from application.ports import UserRepository, GroupRepository, ExpenseRepository, MemberRepository
from domain.models import User, Group, Expense, Member
from infrastructure.db.models import (
    UserDB,
    GroupDB,
    GroupOwnerDB,
    MemberDB,
    ExpenseDB,
    ExpenseCreditorDB,
    ExpenseDebtorDB,
)


class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of the UserRepository.
    Provides access to users stored in the database.
    """
    def __init__(self, session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        db_user = self.session.query(UserDB).filter_by(id=user_id).first()
        return User(id=db_user.id) if db_user else None

    def add(self, user: User) -> None:
        db_user = UserDB()
        self.session.add(db_user)
        self.session.commit()
        user.id = db_user.id


class SQLAlchemyMemberRepository(MemberRepository):
    """
    SQLAlchemy implementation of the MemberRepository.
    Allows managing members within groups.
    """
    def __init__(self, session):
        self.session = session

    def get_by_id(self, member_id: int, group_id: str) -> Member | None:
        db_member = self.session.query(MemberDB).filter_by(id=member_id).first()
        return Member(id=db_member.id, username=db_member.username, group_id=group_id) if db_member else None

    def add(self, member: Member, group_id: str) -> None:
        group_uuid = UUID(group_id)  # Convert string to UUID instance
        db_member = MemberDB(username=member.username, group_id=group_uuid)
        self.session.add(db_member)
        self.session.commit()
        member.id = db_member.id


class SQLAlchemyGroupRepository(GroupRepository):
    """
    SQLAlchemy implementation of the GroupRepository.
    Handles group creation, membership, and ownership.
    """
    def __init__(self, session):
        self.session = session

    def get_by_id(self, group_id: str) -> Group | None:
        group_uuid = UUID(group_id)  # Convert string to UUID instance

        db_group = self.session.query(GroupDB).filter_by(id=group_uuid).first()
        if not db_group:
            return None
        return Group(
            id=db_group.id,
            name=db_group.name,
            owners=[User(id=gp.user_id) for gp in db_group.owners],
            members=[
                Member(id=m.id, username=m.username, group_id=m.group_id) for m in db_group.members
            ]
        )

    def get_groups_by_owner_id(self, owner_id: str) -> list[Group]:
        db_groups_owners = self.session.query(GroupOwnerDB).filter_by(user_id=owner_id).all()
        db_groups = []
        for db_group_owner in db_groups_owners:
            db_group = self.session.query(GroupDB).filter_by(id=db_group_owner.group_id).first()
            if db_group:
                db_groups.append(db_group)

        return [Group(
            id=db_group.id,
            name=db_group.name,
            owners=[User(id=gp.user_id) for gp in db_group.owners],
            members=[
                Member(id=m.id, username=m.username, group_id=m.group_id) for m in db_group.members
            ]) for db_group in db_groups]

    def get_by_expense_id(self, expense_id:str) -> Group | None:
        db_expense = self.session.query(ExpenseDB).filter_by(id=expense_id).first()
        db_group = self.session.query(GroupDB).filter_by(id=db_expense.group_id).first()
        if not db_group:
            return 
        return Group(
            id=db_group.id,
            name=db_group.name,
            owners=[User(id=gp.user_id) for gp in db_group.owners],
            members=[
                Member(id=m.id, username=m.username, group_id=m.group_id) for m in db_group.members
            ])

    def add(self, group: Group) -> None:
        db_group = GroupDB(name=group.name)
        self.session.add(db_group)
        self.session.commit()
        group.id = str(db_group.id)

    def add_member(self, group_id: str, member: Member) -> None:
        group_uuid = UUID(group_id)  # Convert string to UUID instance
        db_member = MemberDB(username=member.username, group_id=group_uuid)
        self.session.add(db_member)
        self.session.commit()
        member.id = db_member.id

    def update_member_name(self, group_id: str, old_name: str, new_name: str) -> None:
        group_uuid = UUID(group_id)

        db_member = (
            self.session.query(MemberDB)
            .filter_by(group_id=group_uuid, username=old_name)
            .first()
        )

        if db_member:
            db_member.username = new_name
            self.session.commit()

    def get_members(self, group_id: str) -> list[Member]:
        group_uuid = UUID(group_id)  # Convert string to UUID instance

        members = self.session.query(MemberDB).filter_by(group_id=group_uuid).all()
        return [Member(id=m.id, username=m.username, group_id=m.group_id) for m in members]

    def remove_member(self, group_id: str, member: Member) -> None:
        group_uuid = UUID(group_id)  # Convert string to UUID instance
        db_member = self.session.query(MemberDB).filter_by(id=member.id, group_id=group_uuid).first()
        if db_member:
            self.session.delete(db_member)
            self.session.commit()

    def add_owner(self, group_id: str, owner: User) -> None:
        group_uuid = UUID(group_id)  # Convert string to UUID instance
        # Ensure user exists
        db_user = self.session.query(UserDB).filter_by(id=owner.id).first()
        if not db_user:
            db_user = UserDB()
            self.session.add(db_user)
            self.session.flush()
            owner.id = db_user.id

        db_owner = GroupOwnerDB(group_id=group_uuid, user_id=db_user.id)
        self.session.add(db_owner)
        self.session.commit()

    def get_owners(self, group_id: str) -> list[User]:
        group_uuid = UUID(group_id)  # Convert string to UUID instance

        owners = (
            self.session.query(GroupOwnerDB)
            .filter_by(group_id=group_uuid)
            .all()
        )
        return [User(id=o.user.id) for o in owners]


class SQLAlchemyExpenseRepository(ExpenseRepository):
    """
    SQLAlchemy implementation of the ExpenseRepository.
    Manages creation and retrieval of expenses, including creditors and debtors.
    """
    def __init__(self, session):
        self.session = session

    def get_by_id(self, expense_id: str) -> Expense | None:
        db_expense = self.session.query(ExpenseDB).filter_by(id=expense_id).first()
        if not db_expense:
            return
        return Expense(
            id=db_expense.id,
            description=db_expense.description,
            total_amount=db_expense.total_amount,
            group_id=db_expense.group_id,
        )

    def add(self, expense: Expense) -> None:
        db_expense = ExpenseDB(
            description=expense.description,
            total_amount=expense.total_amount,
            group_id=UUID(expense.group_id),
        )
        self.session.add(db_expense)
        self.session.flush()  # obtain db_expense.id

        # Add debtors
        for debtor in expense.debtors:
            self.session.add(ExpenseDebtorDB(
                expense_id=db_expense.id,
                member_id=debtor.id
            ))

        # Add creditors with amounts
        for member, amount in expense.creditors:
            self.session.add(ExpenseCreditorDB(
                expense_id=db_expense.id,
                member_id=member.id,
                amount=amount
            ))

        self.session.commit()
        expense.id = db_expense.id

    def update(self, expense: Expense) -> None:
        db_expense = self.session.query(ExpenseDB).filter_by(id=expense.id).first()
        if not db_expense:
            raise ValueError("Expense not found")

        # Update simple fields
        db_expense.description = expense.description
        db_expense.total_amount = expense.total_amount

        # Delete previous related data
        self.session.query(ExpenseDebtorDB).filter_by(expense_id=expense.id).delete()
        self.session.query(ExpenseCreditorDB).filter_by(expense_id=expense.id).delete()

        # Add new debtors and creditors
        for debtor in expense.debtors:
            self.session.add(ExpenseDebtorDB(
                expense_id=expense.id,
                member_id=debtor.id
            ))

        for member, amount in expense.creditors:
            self.session.add(ExpenseCreditorDB(
                expense_id=expense.id,
                member_id=member.id,
                amount=amount
            ))

        self.session.commit()

    def remove(self, expense_id: str) -> None:
        db_expense = self.session.query(ExpenseDB).filter_by(id=expense_id).first()
        if db_expense:
            self.session.delete(db_expense)
            self.session.commit()


    def list_by_group(self, group_id: str) -> list[Expense]:
        group_uuid = UUID(group_id)
        expenses = self.session.query(ExpenseDB).filter_by(group_id=group_uuid).all()
        result = []

        for e in expenses:
            creditors = []
            for c in e.creditors:
                db_member = self.session.query(MemberDB).filter_by(id=c.member_id).first()
                creditors.append(
                    (Member(id=db_member.id, username=db_member.username, group_id=db_member.group_id), c.amount)
                )

            debtors = []
            for d in e.debtors:
                db_member = self.session.query(MemberDB).filter_by(id=d.member_id).first()
                debtors.append(Member(id=db_member.id, username=db_member.username, group_id=db_member.group_id))

            result.append(Expense(
                id=e.id,
                description=e.description,
                total_amount=e.total_amount,
                group_id=e.group_id,
                creditors=creditors,
                debtors=debtors
            ))

        return result
