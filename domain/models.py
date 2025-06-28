# Entities

from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    id: int
    username: str

@dataclass
class Group:
    id: int
    name: str
    members: List[User] = field(default_factory=list)

@dataclass
class Expense:
    id: int
    description: str
    total_amount: float
    group_id: int
    creditors: List['ExpenseShare'] = field(default_factory=list)
    debtors: List['ExpenseShare'] = field(default_factory=list)

@dataclass
class ExpenseShare:
    user_id: int
    amount: float
