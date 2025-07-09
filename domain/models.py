# Entities

from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    id: int
    
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

@dataclass
class Member:
    id: int
    username: str
    group_id: str

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

@dataclass
class Group:
    id: str
    name: str
    owners: List[User] = field(default_factory=list)
    members: List[Member] = field(default_factory=list)

@dataclass
class Expense:
    id: int
    description: str
    total_amount: float
    group_id: str
    creditors: List[tuple[Member, float]] = field(default_factory=list)
    debtors: List[Member] = field(default_factory=list)