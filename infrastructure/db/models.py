import uuid
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserDB(Base):
    """
    Represents a system user. A user can own multiple groups.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Groups this user owns
    owned_groups: Mapped[list["GroupOwnerDB"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class GroupDB(Base):
    """
    Represents a group that contains members and expenses.
    A group can be owned by multiple users and contain multiple members.
    """
    __tablename__ = "groups"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
            default=datetime.now(),
            onupdate=datetime.now()
        )
    # Users that own this group
    owners: Mapped[list["GroupOwnerDB"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )

    # Members belonging to this group
    members: Mapped[list["MemberDB"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )

    # Expenses created within this group
    expenses: Mapped[list["ExpenseDB"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ID: {self.id}, NAME: {self.name}, OWNERS: {self.owners}, MEMBERS: {self.members}"


class GroupOwnerDB(Base):
    """
    Intermediate table that maps a user as an owner of a group.
    Composite primary key: (group_id, user_id)
    """
    __tablename__ = "group_owners"

    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    # Owning group
    group: Mapped["GroupDB"] = relationship(back_populates="owners")
    # User who owns the group
    user: Mapped["UserDB"] = relationship(back_populates="owned_groups")


class MemberDB(Base):
    """
    Represents a member within a group.
    A member can participate in expenses as debtor and/or creditor.
    """
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("groups.id"), nullable=False)

    # Group this member belongs to
    group: Mapped["GroupDB"] = relationship(back_populates="members")

    # Expenses where this member is a debtor
    debtor_expenses: Mapped[list["ExpenseDebtorDB"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )

    # Expenses where this member is a creditor
    creditor_expenses: Mapped[list["ExpenseCreditorDB"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )


class ExpenseDB(Base):
    """
    Represents an expense made in a group. 
    It has a total amount and can have multiple creditors and debtors.
    """
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String)
    total_amount: Mapped[float] = mapped_column(nullable=False)
    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("groups.id"))

    # Group where this expense was made
    group: Mapped["GroupDB"] = relationship(back_populates="expenses")

    # Members who paid for this expense (with individual amounts)
    creditors: Mapped[list["ExpenseCreditorDB"]] = relationship(
        back_populates="expense", cascade="all, delete-orphan"
    )

    # Members who owe money for this expense
    debtors: Mapped[list["ExpenseDebtorDB"]] = relationship(
        back_populates="expense", cascade="all, delete-orphan"
    )


class ExpenseCreditorDB(Base):
    """
    Intermediate table for expense creditors.
    Indicates that a member paid a given amount for an expense.
    Composite primary key: (expense_id, member_id)
    """
    __tablename__ = "expense_creditors"

    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id"), primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)

    # The expense this credit is related to
    expense: Mapped["ExpenseDB"] = relationship(back_populates="creditors")
    # The member who paid
    member: Mapped["MemberDB"] = relationship(back_populates="creditor_expenses")


class ExpenseDebtorDB(Base):
    """
    Intermediate table for expense debtors.
    Indicates that a member is responsible for part of an expense.
    Composite primary key: (expense_id, member_id)
    """
    __tablename__ = "expense_debtors"

    expense_id: Mapped[int] = mapped_column(ForeignKey("expenses.id"), primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), primary_key=True)

    # The expense this debt is related to
    expense: Mapped["ExpenseDB"] = relationship(back_populates="debtors")
    # The member who owes
    member: Mapped["MemberDB"] = relationship(back_populates="debtor_expenses")
