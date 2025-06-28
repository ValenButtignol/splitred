# Mock repositories for testing

from domain.models import User
from application.ports import UserRepository, ExpenseRepository, GroupRepository

class MockUserRepository(UserRepository):
    def __init__(self):
        self.users = []

    def get_by_username(self, username):
        for u in self.users:
            if u.username == username:
                return u
        return None

    def add(self, user: User):
        user.id = len(self.users) + 1
        self.users.append(user)

    def get_by_id(self, user_id):
        return next((u for u in self.users if u.id == user_id), None)

class MockExpenseRepository(ExpenseRepository):
    def __init__(self, expenses):
        self.expenses = expenses

    def list_by_group(self, group_id):
        return self.expenses

    def add(self, expense):
        self.expenses.append(expense)
        return expense

class MockGroupRepository(GroupRepository):
    def __init__(self, members):
        self.members = members

    def get_members(self, group_id):
        return self.members

    def add_user_to_group(self, group_id, user_id):
        self.members.append(user_id)

    def get_by_id(self, group_id):
        return self.group_id

    def add(self, group):
        self.group_id = group.id
        self.group_name = group.name