# Repo Interfaces

from abc import ABC, abstractmethod
from domain.models import User, Group, Expense, Member, User, Member
class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> User: pass

    @abstractmethod
    def add(self, user: User) -> None: pass

class MemberRepository(ABC):
    @abstractmethod
    def get_by_id(self, member_id: int) -> Member: pass

    @abstractmethod
    def add(self, member: Member) -> None: pass

class GroupRepository(ABC):
    @abstractmethod
    def get_by_id(self, group_id: int) -> Group: pass

    @abstractmethod
    def add(self, group: Group) -> None: pass

    @abstractmethod
    def add_member(self, group_id: int, member: Member) -> None: pass

    @abstractmethod
    def get_members(self, group_id: int) -> list[Member]: pass

    @abstractmethod
    def remove_member(self, group_id: int, member: Member) -> None: pass

    @abstractmethod
    def add_owner(self, group_id: int, owner: User) -> None: pass
    
    @abstractmethod
    def get_owners(self, group_id: int) -> list[User]: pass


class ExpenseRepository(ABC):
    @abstractmethod
    def add(self, expense: Expense) -> None: pass

    @abstractmethod
    def list_by_group(self, group_id: int) -> list[Expense]: pass
