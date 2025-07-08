# SQLAlchemy Models

import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)

class MemberDB(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    group = relationship("GroupDB", back_populates="members")

# Expense-User intermediate table with amount
class ExpenseCreditorDB(Base):
    __tablename__ = "expense_creditors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    amount = Column(Float)

expense_debtors = Table(
    "expense_debtors", Base.metadata,
    Column("expense_id", Integer, ForeignKey("expenses.id")),
    Column("member_id", Integer, ForeignKey("members.id")),
)

group_owners = Table(
    "group_owners",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

class GroupDB(Base):
    __tablename__ = "groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    owners = relationship("UserDB", secondary=group_owners)
    members = relationship("MemberDB", back_populates="group", cascade="all, delete-orphan")


class ExpenseDB(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    total_amount = Column(Float)
    group_id = Column(Integer, ForeignKey("groups.id"))
    debtors = relationship("MemberDB", secondary=expense_debtors)
    creditors = relationship("ExpenseCreditorDB", backref="expense")