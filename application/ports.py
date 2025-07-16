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
    def get_by_id(self, member_id: int, group_id: str) -> Member: pass

    @abstractmethod
    def add(self, member: Member, group_id:str) -> None: pass

class GroupRepository(ABC):
    @abstractmethod
    def get_by_id(self, group_id: str) -> Group: pass

    @abstractmethod
    def get_groups_by_owner_id(self, owner_id:str) -> list[Group]: pass

    @abstractmethod
    def add(self, group: Group) -> None: pass

    @abstractmethod
    def add_member(self, group_id: str, member: Member) -> None: pass

    @abstractmethod
    def update_member_name(self, group_id: str, old_name: str, new_name: str) -> None: pass

    @abstractmethod
    def get_members(self, group_id: str) -> list[Member]: pass

    @abstractmethod
    def remove_member(self, group_id: str, member: Member) -> None: pass

    @abstractmethod
    def add_owner(self, group_id: str, owner: User) -> None: pass
    
    @abstractmethod
    def get_owners(self, group_id: str) -> list[User]: pass


class ExpenseRepository(ABC):
    @abstractmethod
    def add(self, expense: Expense) -> None: pass

    @abstractmethod
    def list_by_group(self, group_id: str) -> list[Expense]: pass
