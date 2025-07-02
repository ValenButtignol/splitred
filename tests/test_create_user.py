import pytest
from domain.services import create_user
from tests.mocks import MockUserRepository

def test_create_user_success():
    repo = MockUserRepository()
    user = create_user(repo, "alice")
    assert user.username == "alice"
    assert user.id == 1

def test_create_user_duplicate():
    repo = MockUserRepository()
    create_user(repo, "alice")
    create_user(repo, "alice")
    assert repo.get_by_id(1).username == "alice" 
    assert repo.get_by_id(2).username == "alice"

def test_create_user_with_different_ids():
    repo = MockUserRepository()
    user1 = create_user(repo, "alice")
    user2 = create_user(repo, "bob")
    assert user1.id != user2.id
