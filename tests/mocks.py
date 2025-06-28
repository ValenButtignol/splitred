# Mock repositories for testing

from domain.models import User
from application.ports import UserRepository, ExpenseRepository

class InMemoryUserRepository(UserRepository):
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

class StubExpenseRepository(ExpenseRepository):
    def __init__(self, expenses):
        self.expenses = expenses

    def list_by_group(self, group_id):
        return self.expenses