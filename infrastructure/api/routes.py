from flask import request, jsonify
from domain.services import add_owner_to_group, calculate_group_balance, calculate_payments, create_expense, create_user, create_group, create_member, edit_member_name_in_group, get_expenses_by_group_id, get_groups_by_owner_id, get_member_by_id, get_member_by_username_and_group, get_members_by_group_id, get_user_by_id, add_member_to_group, get_group_by_id, remove_expense, remove_member_from_group, update_expense
from infrastructure.db.repository import SQLAlchemyUserRepository, SQLAlchemyGroupRepository, SQLAlchemyMemberRepository, SQLAlchemyExpenseRepository
from infrastructure.db import SessionLocal

def register_routes(app, limiter):

    # USERS

    @app.route("/users", methods=["POST"])
    @limiter.limit("10 per minute")
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

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        session = SessionLocal()
        repo = SQLAlchemyUserRepository(session)
        try:
            user = get_user_by_id(repo, user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify({"id": user.id})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    # GROUPS

    @app.route("/groups", methods=["POST"])
    @limiter.limit("10 per minute")
    def post_group():
        session = SessionLocal()
        user_repo = SQLAlchemyUserRepository(session)
        group_repo = SQLAlchemyGroupRepository(session)
        member_repo = SQLAlchemyMemberRepository(session)
        try:
            data = request.get_json()
            name = data["name"]
            owner_id = data["owner_id"]
            members = data["members"]

            owner = get_user_by_id(user_repo, owner_id)  
            if not owner:
                return jsonify({"error": "Owner not found"}), 404

            group = create_group(group_repo, name, owner)
            for member in members:
                m = create_member(member_repo, group_repo, member, str(group.id))
            session.flush()

            return jsonify({
                "id": str(group.id),
                "name": group.name,
                "members": [m for m in members],
                "owner_ids": [owner for owner in group.owners]
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/groups/<group_id>/join", methods=["POST"])
    def join_group(group_id: str):
        session = SessionLocal()
        group_repo = SQLAlchemyGroupRepository(session)
        user_repo = SQLAlchemyUserRepository(session)
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            if not user_id:
                return jsonify({"error": "user_id is required"}), 400
            new_owner = get_user_by_id(user_repo, user_id)
            
            if not new_owner:
                return jsonify({"error": "User not found"}), 404

            group = get_group_by_id(group_repo, group_id)
            if not group:
                return jsonify({"error": "Group not found"}), 404

            add_owner_to_group(group_repo, group_id, new_owner)
            return jsonify({"message": "User added as owner"}), 200

        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/groups", methods=["GET"])
    def get_groups():
        session = SessionLocal()
        group_repo = SQLAlchemyGroupRepository(session)

        try:
            owner_id = request.args.get("owner_id")
            groups = get_groups_by_owner_id(group_repo, owner_id)

            return jsonify([{
                "id": str(group.id), 
                "name": group.name, 
                "members": [member.username for member in group.members], 
                "owner_ids": [str(owner.id) for owner in group.owners]
            } for group in groups])
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()


    @app.route("/groups/<group_id>", methods=["GET"])
    def get_group(group_id: str):
        session = SessionLocal()
        group_repo = SQLAlchemyGroupRepository(session)
        try:
            owner_id = request.args.get("owner_id")

            if not owner_id:
                return jsonify({"error": "Missing owner_id"}), 400

            group = get_group_by_id(group_repo, group_id)
            if not group:
                return jsonify({"error": "Group not found"}), 404

            # Only allows owners of the group to access to the group data.
            if not any(str(owner.id) == owner_id for owner in group.owners):
                return jsonify({"error": "Access denied: not an owner of this group"}), 403

            return jsonify({
                "id": group.id,
                "name": group.name,
                "members": [member.username for member in group.members],
                "owner_ids": [str(owner.id) for owner in group.owners]
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()


    # EXPENSES

    @app.route("/groups/<group_id>/expenses", methods=["GET"])
    def get_expenses(group_id: str):
        session = SessionLocal()
        expenses_repo = SQLAlchemyExpenseRepository(session)
        try:
            expenses = get_expenses_by_group_id(expenses_repo, group_id)
            
            return jsonify([{
                "id": str(e.id),
                "description": e.description,
                "creditors": [{"name": c[0].username, "amount":c[1]} for c in e.creditors],
                "debtors": [d.username for d in e.debtors],
                "price": e.total_amount
            } for e in expenses])
        except Exception as e:
            return jsonify({"error" : str(e)}), 500
        finally:
            session.close()

    @app.route("/groups/<group_id>/expenses", methods=["POST"])
    @limiter.limit("30 per minute")
    def post_expense(group_id: str):
        session = SessionLocal()
        expense_repo = SQLAlchemyExpenseRepository(session)
        group_repo = SQLAlchemyGroupRepository(session)

        try:
            data = request.get_json()
            description = data["description"]
            price = data["price"]
            creditors = data["creditors"]  # [{name, amount}]
            debtors = data["debtors"]      # [name]

            expense = create_expense(
                expense_repo, group_repo, group_id,
                description, price, creditors, debtors
            )

            return jsonify({
                "id": str(expense.id),
                "description": expense.description,
                "creditors": [{"name": c[0].username, "amount": c[1]} for c in expense.creditors],
                "debtors": [d.username for d in expense.debtors],
                "price": expense.total_amount
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/expenses/<expense_id>", methods=["PUT"])   # This should depend of the group_id
    def update_expense_endpoint(expense_id: str):
        session = SessionLocal()
        expense_repo = SQLAlchemyExpenseRepository(session)
        group_repo = SQLAlchemyGroupRepository(session)

        try:
            data = request.get_json()
            description = data["description"]
            price = data["price"]
            creditors = data["creditors"]
            debtors = data["debtors"]

            expense = update_expense(
                expense_repo,
                group_repo,
                expense_id,
                description,
                price,
                creditors,
                debtors
            )

            return jsonify({
                "id": str(expense.id),
                "description": expense.description,
                "creditors": [{"name": c[0].username, "amount": c[1]} for c in expense.creditors],
                "debtors": [d.username for d in expense.debtors],
                "price": expense.total_amount
            }), 200

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    # MEMBERS

    @app.route("/groups/<group_id>/members", methods=["POST"])
    def post_member(group_id):
        session = SessionLocal()
        member_repo = SQLAlchemyMemberRepository(session)
        group_repo = SQLAlchemyGroupRepository(session)
        try:
            data = request.get_json()
            member_username = data["username"]

            member = create_member(member_repo, group_repo, member_username, group_id)
            
            return jsonify({
                "id": member.id,
                "member_username": member.username,
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/groups/<group_id>/members", methods=["GET"])
    def get_members(group_id):
        session = SessionLocal()
        group_repo = SQLAlchemyGroupRepository(session)
        try:
            members = get_members_by_group_id(group_repo, group_id)
            return jsonify([member.username for member in members])
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/groups/<group_id>/members/<username>", methods=["DELETE"])
    def delete_member(group_id, username):
        session = SessionLocal()
        group_repo = SQLAlchemyGroupRepository(session)
        expense_repo = SQLAlchemyExpenseRepository(session)
        try:
            member = get_member_by_username_and_group(group_repo, username, group_id)
            if not member:
                return jsonify({"error": "Member not found"}), 404

            remove_member_from_group(group_repo, expense_repo, group_id, member)
            return jsonify({"message": "Member removed"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @app.route("/groups/<group_id>/members/<old_name>", methods=["PUT"])
    def update_member(group_id, old_name):
        session = SessionLocal()
        group_repo = SQLAlchemyGroupRepository(session)
        body = request.get_json()
        new_name = body.get("new_name")
        if not new_name:
            return jsonify({"error": "Missing new_name"}), 400

        try:
            edit_member_name_in_group(group_repo, group_id, old_name, new_name)
            return jsonify({"success": True}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/expenses/<expense_id>", methods=["DELETE"])
    def delete_expense(expense_id):
        session = SessionLocal()
        expense_repo = SQLAlchemyExpenseRepository(session)
        try:
            remove_expense(expense_repo, expense_id)
            
            return jsonify({"message": "Member removed"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    # SUMMARY

    @app.route("/groups/<group_id>/summary", methods=["GET"])
    def get_group_summary(group_id):
        session = SessionLocal()
        expense_repo = SQLAlchemyExpenseRepository(session)
        group_repo = SQLAlchemyGroupRepository(session)
        try:
            balances = calculate_group_balance(expense_repo, group_repo, group_id)
            payments = calculate_payments(balances)

            response = {
                "balances": {
                    member.username: round(balance, 2)
                    for member, balance in balances.items()
                },
                "payments": [
                    {
                        "from": debtor.username,
                        "to": creditor.username,
                        "amount": round(amount, 2),
                    }
                    for creditor, debtor, amount in payments
                ],
            }
            return jsonify(response), 200
        except Exception as e:
            print(f"Error in /groups/{group_id}/summary: {e}")
            return jsonify({"error": str(e)}), 500
