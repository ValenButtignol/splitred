# Repo Interfaces

from abc import ABC, abstractmethod
from domain.models import User, Group, Expense

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User: pass

    @abstractmethod
    def get_by_username(self, username: str) -> User: pass

    @abstractmethod
    def add(self, user: User) -> None: pass

class GroupRepository(ABC):
    @abstractmethod
    def get_by_id(self, group_id: int) -> Group: pass

    @abstractmethod
    def add(self, group: Group) -> None: pass

    @abstractmethod
    def add_user_to_group(self, group_id: int, user_id: int) -> None: pass

    @abstractmethod
    def get_members(self, group_id: int) -> list[User]: pass

class ExpenseRepository(ABC):
    @abstractmethod
    def add(self, expense: Expense) -> None: pass

    @abstractmethod
    def list_by_group(self, group_id: int) -> list[Expense]: pass
