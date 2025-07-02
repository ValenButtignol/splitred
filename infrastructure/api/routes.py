from flask import request, jsonify
from application.ports import UserRepository
from domain.services import create_user, create_group
from infrastructure.db.repository import SQLAlchemyUserRepository, SQLAlchemyGroupRepository
from infrastructure.db import SessionLocal
from infrastructure.db.models import UserDB, GroupDB

def register_routes(app):

    # USERS

    @app.route("/users", methods=["POST"])
    def post_user():
        session = SessionLocal()
        repo: UserRepository = SQLAlchemyUserRepository(session)
        try:
            data = request.get_json()
            username = data["username"]
            print("Creating user", username)
            user = create_user(repo, username)
            print("Created user", user)
            return jsonify({
                "id": user.id,
                "username": user.username
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/users", methods=["GET"])
    def get_users():
        session = SessionLocal()

        try:
            users = session.query(UserDB).all()
            return jsonify([
                {"id": user.id, "username": user.username}
                for user in users
            ])
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        session = SessionLocal()

        try:
            user = session.query(UserDB).filter_by(id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify({"id": user.id, "username": user.username})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    # GROUPS

    @app.route("/groups", methods=["POST"])
    def post_group():
        session = SessionLocal()
        user_repo = SQLAlchemyUserRepository(session)
        group_repo = SQLAlchemyGroupRepository(session)
        try:
            data = request.get_json()
            name = data["name"]
            owner_id = data["owner_id"]

            owner = user_repo.get_by_id(owner_id)
            if not owner:
                return jsonify({"error": "Owner not found"}), 404

            group = create_group(group_repo, name, owner)
            return jsonify({
                "id": group.id,
                "name": group.name,
                "members": [member.username for member in group.members],
                "owner": group.owner.username
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/groups", methods=["GET"])
    def get_groups():
        session = SessionLocal()
        try:
            groups = session.query(GroupDB).all()
            return jsonify([{
                "id": group.id, 
                "name": group.name, 
                "members": [member.username for member in group.members], 
                "owner_id": group.owner_id
                } for group in groups
            ])
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

