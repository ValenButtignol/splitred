# SQLAlchemy Models

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

# Group-User intermediate table
group_members = Table(
    "group_members", Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

expense_debtors = Table(
    "expense_debtors", Base.metadata,
    Column("expense_id", Integer, ForeignKey("expenses.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)

class GroupDB(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", backref="owned_groups")
    members = relationship("UserDB", secondary=group_members)

class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    total_amount = Column(Float)
    group_id = Column(Integer, ForeignKey("groups.id"))

    debtors = relationship("UserDB", secondary=expense_debtors)

    creditors = relationship("ExpenseCreditorDB", backref="expense")

# Expense-User intermediate table with amount
class ExpenseCreditorDB(Base):
    __tablename__ = "expense_creditors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
