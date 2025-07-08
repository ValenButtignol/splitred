from flask import request, jsonify
from domain.services import create_user, create_group, create_member, get_user_by_id, add_member_to_group, get_group_by_id
from infrastructure.db.repository import SQLAlchemyUserRepository, SQLAlchemyGroupRepository, SQLAlchemyMemberRepository
from infrastructure.db import SessionLocal
from infrastructure.db.models import UserDB, GroupDB

def register_routes(app):

    # USERS

    @app.route("/users", methods=["POST"])
    def post_user():
        session = SessionLocal()
        repo = SQLAlchemyUserRepository(session)
        try:
            data = request.get_json()
            user = create_user(repo)
            return jsonify({
                "id": user.id,
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
                {"id": user.id}
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
            return jsonify({"id": user.id})
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
            members = data["members"]

            owner = get_user_by_id(user_repo, owner_id) # type: ignore
            if not owner:
                return jsonify({"error": "Owner not found"}), 404

            group = create_group(group_repo, name, owner, members)
            return jsonify({
                "id": str(group.id),
                "name": group.name,
                "members": [member.username for member in group.members],
                "owner_ids": [owner.id for owner in group.owners]
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
                "owner_ids": [owner.id for owner in group.owners]
                } for group in groups
            ])
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/groups/<int:group_id>", methods=["GET"])
    def get_group(group_id):
        session = SessionLocal()
        try:
            group = session.query(GroupDB).filter_by(id=group_id).first()
            if not group:
                return jsonify({"error": "Group not found"}), 404
            return jsonify({
                "id": group.id, 
                "name": group.name, 
                "members": [member.username for member in group.members],
                "owner_ids": [owner.id for owner in group.owners]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    # MEMBERS

    @app.route("/groups/<int:group_id>/members", methods=["POST"])
    def post_member(group_id):
        session = SessionLocal()
        group_repo = SQLAlchemyGroupRepository(session)
        member_repo = SQLAlchemyMemberRepository(session)
        try:
            data = request.get_json()
            member_username = data["username"]
            group = get_group_by_id(group_repo, group_id) # type: ignore
            member = create_member(member_repo, member_username)
            add_member_to_group(group_repo, group_id, member)
            
            session.commit()
            return jsonify({
                "id": group.id,
                "name": group.name,
                "members": [member.username for member in group.members],
                "owner_ids": [owner.id for owner in group.owners]
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/groups/<int:group_id>/members", methods=["GET"])
    def get_members(group_id):
        session = SessionLocal()
        group_repo = SQLAlchemyGroupRepository(session)
        try:
            group = get_group_by_id(group_repo, group_id) # type: ignore
            return jsonify([member.username for member in group.members])
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    # EXPENSES
    