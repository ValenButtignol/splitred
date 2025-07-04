# SQLAlchemy Ports

from application.ports import UserRepository, GroupRepository, ExpenseRepository
from domain.models import User, Group, Expense
from infrastructure.db.models import UserDB, GroupDB, ExpenseDB, ExpenseCreditorDB

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
            owner=User(id=db_group.owner_id, username=db_group.owner.username),
            members=[
                User(id=u.id, username=u.username) for u in db_group.members
            ]
        )

    def add(self, group: Group) -> None:
        db_group = GroupDB(name=group.name, owner_id=group.owner.id)
        self.session.add(db_group)
        self.session.commit()
        group.id = db_group.id # type: ignore
        # Add members if any
        for member in group.members:
            db_user = self.session.query(UserDB).filter_by(id=member.id).first()
            db_group.members.append(db_user)
        self.session.commit()

    def add_user_to_group(self, group_id: int, user_id: int) -> None:
        db_group = self.session.query(GroupDB).get(group_id)
        db_user = self.session.query(UserDB).get(user_id)
        if db_user not in db_group.members:
            db_group.members.append(db_user)
            self.session.commit()

    def get_members(self, group_id: int) -> list[User]:
        db_group = self.session.query(GroupDB).get(group_id)
        return [User(id=u.id, username=u.username) for u in db_group.members] if db_group else []

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

        # Add debtors (users)
        for debtor in expense.debtors:
            db_user = self.session.query(UserDB).get(debtor.id)
            db_expense.debtors.append(db_user)

        # Add creditors (with amount)
        for user, amount in expense.creditors:
            self.session.add(ExpenseCreditorDB(
                expense_id=db_expense.id,
                user_id=user.id,
                amount=amount
            ))

        self.session.commit()
        expense.id = db_expense.id # type: ignore

    def list_by_group(self, group_id: int) -> list[Expense]:
        expenses = self.session.query(ExpenseDB).filter_by(group_id=group_id).all()
        result = []

        for e in expenses:
            creditors = [
                (User(id=c.user_id, username=self.session.get(UserDB, c.user_id).username), c.amount)
                for c in e.creditors
            ]
            debtors = [User(id=u.id, username=u.username) for u in e.debtors]

            result.append(Expense(
                id=e.id,
                description=e.description,
                total_amount=e.total_amount,
                group_id=e.group_id,
                creditors=creditors,
                debtors=debtors
            ))

        return result
