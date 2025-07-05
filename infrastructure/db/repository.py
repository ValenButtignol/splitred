# SQLAlchemy Ports

from application.ports import UserRepository, GroupRepository, ExpenseRepository, MemberRepository
from domain.models import User, Group, Expense, Member
from infrastructure.db.models import UserDB, GroupDB, ExpenseDB, ExpenseCreditorDB, MemberDB   

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        db_user = self.session.query(UserDB).filter_by(id=user_id).first()
        return User(id=db_user.id, username=db_user.username) if db_user else None

    def add(self, user: User) -> None:
        db_user = UserDB(username=user.username)
        self.session.add(db_user)
        self.session.commit()
        user.id = db_user.id # type: ignore

class SQLAlchemyMemberRepository(MemberRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, member_id: int) -> Member | None:
        db_member = self.session.query(MemberDB).filter_by(id=member_id).first()
        return Member(id=db_member.id, username=db_member.username) if db_member else None

    def add(self, member: Member) -> None:
        db_member = MemberDB(username=member.username)
        self.session.add(db_member)
        self.session.commit()
        member.id = db_member.id # type: ignore

class SQLAlchemyGroupRepository(GroupRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, group_id: int) -> Group | None:
        db_group = self.session.query(GroupDB).filter_by(id=group_id).first()
        if not db_group:
            return None
        return Group(
            id=db_group.id,
            name=db_group.name,
            owners=[User(id=u.id, username=u.username) for u in db_group.owners],
            members=[
                Member(id=u.id, username=u.username) for u in db_group.members
            ]
        )

    def add(self, group: Group) -> None:
        db_group = GroupDB(name=group.name)
        self.session.add(db_group)
        self.session.commit()
        group.id = db_group.id # type: ignore

    def add_member(self, group_id: int, member: Member) -> None:
        db_member = MemberDB(username=member.username, group_id=group_id)
        self.session.add(db_member)
        self.session.commit()
        member.id = db_member.id  # type: ignore

    def get_members(self, group_id: int) -> list[Member]:
        members = self.session.query(MemberDB).filter_by(group_id=group_id).all()
        return [Member(id=m.id, username=m.username) for m in members]

    def remove_member(self, group_id: int, member: Member) -> None:
        db_member = self.session.query(MemberDB).filter_by(id=member.id, group_id=group_id).first()
        self.session.delete(db_member)
        self.session.commit()

    def add_owner(self, group_id: int, owner: User) -> None:
        db_owner = UserDB(username=owner.username)
        self.session.add(db_owner)
        self.session.commit()
        owner.id = db_owner.id # type: ignore

    def get_owners(self, group_id: int) -> list[User]:
        db_group = self.session.query(GroupDB).filter_by(id=group_id).first()
        return [User(id=u.id, username=u.username) for u in db_group.owners] if db_group else []

class SQLAlchemyExpenseRepository(ExpenseRepository):
    def __init__(self, session):
        self.session = session

    def add(self, expense: Expense) -> None:
        db_expense = ExpenseDB(
            description=expense.description,
            total_amount=expense.total_amount,
            group_id=expense.group_id,
        )
        self.session.add(db_expense)
        self.session.flush()  # to obtain expense.id

        # Add debtors (members)
        for debtor in expense.debtors:
            db_member = self.session.query(MemberDB).get(debtor.id)
            db_expense.debtors.append(db_member)

        # Add creditors (with amount)
        for member, amount in expense.creditors:
            self.session.add(ExpenseCreditorDB(
                expense_id=db_expense.id,
                member_id=member.id,
                amount=amount
            ))

        self.session.commit()
        expense.id = db_expense.id # type: ignore

    def list_by_group(self, group_id: int) -> list[Expense]:
        expenses = self.session.query(ExpenseDB).filter_by(group_id=group_id).all()
        result = []

        for e in expenses:
            creditors = [
                (Member(id=c.member_id, username=self.session.get(MemberDB, c.member_id).username), c.amount)
                for c in e.creditors
            ]
            debtors = [Member(id=u.id, username=u.username) for u in e.debtors]

            result.append(Expense(
                id=e.id,
                description=e.description,
                total_amount=e.total_amount,
                group_id=e.group_id,
                creditors=creditors,
                debtors=debtors
            ))

        return result
