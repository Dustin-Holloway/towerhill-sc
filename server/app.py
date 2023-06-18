#!/usr/bin/env python3


from flask import request, session, make_response, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from models import User, Listing, Comment
from config import app, api, db
import ipdb
from flask import request
from flask_restful import Resource

class NextAuthLogin(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            email = json_data.get("email")
            name = json_data.get("name")
            image = json_data.get("image")
            username = json_data.get("username")




            if not email:
                response = make_response({"error": "Email is required."}, 400)
                return response

            # Here, you can perform any additional validation or checks you need
            user = db.session.query(User).filter_by(email=email).first()

            if not user:

                newUser = User( username=username, name=name , email=email, image=image)
                db.session.add(newUser)
                db.session.commit()
               
            response = make_response(jsonify({"success": True}), 200)
            return response

        except Exception as e:
            response = make_response({"error": str(e)}, 500)
            return response




class UserById(Resource):
    def get(self, id):
        user = db.session.query(User).filter_by(id=id).first()

        if user:
            return make_response(jsonify(user.to_dict()), 201)

        return make_response(jsonify({"error": "user not found!"}), 404)

    def patch(self, id):
        request_json = request.get_json()
        updated_user = User.query.filter(User.id == id).first()
        if updated_user:
            new_password = request_json.get("new_password")

            if new_password:
                updated_user.set_password(new_password)

            for key, value in request_json.items():
                if hasattr(updated_user, key):
                    setattr(updated_user, key, value)

            db.session.add(updated_user)
            db.session.commit()
            return make_response(jsonify(updated_user.to_dict()), 200)

        return make_response({"Error": "User not found"}, 404)


class Login(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            email = json_data.get("email")
            password = json_data.get("password")
            name = json_data.get("name")


            if not email:
                response = make_response({"error": "Username is required."}, 400)
                return response

            current_user = User.query.filter_by(email=email).first()


            if current_user and current_user.authenticate(password):
                # session["email"] = current_user.email
                response = make_response(
                    jsonify(
                        current_user.to_dict(
                            only=(
                                "id",
                                "email",
                                "name",
                                "_password_hash"

                            )
                        )
                    ),
                    200,
                )  # Include the "username" key in the response JSON
                return response

            response = make_response({"error": "Invalid username or password."}, 401)
            return response

        except Exception as e:
            response = make_response({"error": str(e)}, 500)
            return response
        
        


class Logout(Resource):
    def delete(self):
        if session["username"]:
            session["username"] = None
            return {}, 200
        else:
            response = make_response({}, 401)
            return response


class CheckSession(Resource):
    def get(self):
        if "email" in session:
            user = User.query.filter_by(email=session["email"]).first()
            if user:
                response = make_response(jsonify(user.to_dict()), 200)
                
                return response

        response = make_response({}, 401)
        return response


class NewUser(Resource):
    def post(self):
        request_json = request.get_json()

        try:
            new_user = User(

                password=request_json.get("password"),
                email=request_json.get("email"),
                name=request_json.get("name"),
            )

            new_user.password = request_json.get("password")

            db.session.add(new_user)
            db.session.commit()

            return make_response(jsonify(new_user.to_dict()), 201)

        except Exception:
            return make_response(jsonify({}), 400)


class UserComments(Resource):
    def get(self):
        new_listings = Comment.query.all()

        if new_listings:
            return make_response(
                jsonify(
                    [
                        comment.to_dict(
                            only=(
                                "comment_type",
                                "content",
                                "listing_id",
                                "id",
                                "user_id",
                            )
                        )
                        for comment in new_listings
                    ]
                ),
                200,
            )
        return make_response({"error": "no comments found"}, 404)

    def post(self):
        request_json = request.get_json()

        try:
            email = session.get("email")
            user = User.query.filter_by(email=email).first()

            if not user:
                return make_response(
                    jsonify({"error": "User not found, please login"}), 401
                )

            new_comment = Comment(
                content=request_json.get("content"),
                # comment_type=request_json.get("comment_type"),
                # listing_id=request_json.get("listing_id"),
                user=user,
            )

            db.session.add(new_comment)
            db.session.commit()

            return make_response(
                jsonify(
                    new_comment.to_dict(
                        only=("content", "id")
                    )
                ),
                201,
            )

        except Exception:
            return make_response(jsonify({}), 400)


class UserCommentsById(Resource):
    def get(self, id):
        new_listing = Comment.query.get(id)

        if new_listing:
            return make_response(
                jsonify(new_listing.to_dict()),
                200,
            )
        return make_response({"error": "comment not found"}, 404)

    def delete(self, id):
        new_listing = Comment.query.get(id)

        if new_listing:
            db.session.delete(new_listing)
            db.session.commit()
            return make_response({}, 204)

    def patch(self, id):
        request_json = request.get_json()
        updated_comment = Comment.query.filter_by(id=id).first()
        if updated_comment:
            for key, value in request_json.items():
                if hasattr(updated_comment, key):
                    setattr(updated_comment, key, value)

            db.session.add(updated_comment)
            db.session.commit()
            return make_response(
                jsonify(updated_comment.to_dict(only=("id",))),
                201,
            )

        return make_response({"Error": "User not found"}, 404)


class ListingsById(Resource):
    def get(self, id):
        new_listing = Listing.query.get(id)

        if new_listing:
            return make_response(
                jsonify(new_listing.to_dict()),
                200,
            )
        return make_response({"error": "comment not found"}, 404)

    def delete(self, id):
        listing = Listing.query.get(id)

        if listing:
            db.session.delete(listing)
            db.session.commit()
            return make_response({}, 204)

    def patch(self, id):
        request_json = request.get_json()
        updated_comment = Listing.query.filter_by(id=id).first()
        if updated_comment:
            for key, value in request_json.items():
                if hasattr(updated_comment, key):
                    setattr(updated_comment, key, value)

            db.session.add(updated_comment)
            db.session.commit()
            return make_response(
                jsonify(updated_comment.to_dict(only=("id",))),
                201,
            )

        return make_response({"Error": "User not found"}, 404)


class Listings(Resource):
    def get(self):
        all_listings = Listing.query.all()

        if all_listings:
            return make_response(
                jsonify(
                    [
                        listing.to_dict(
                            only=("image", "title", "content", "id", "created_at")
                        )
                        for listing in all_listings
                    ]
                ),
                200,
            )
        return make_response({"error": "no comments found"}, 404)

    def post(self):
        request_json = request.get_json()

        try:
            user_id = request_json.get("user_id")
            user = User.query.get(user_id)

            if not user:
                return make_response(
                    jsonify({"error": "User not found, please login"}), 401
                )

            new_listing = Listing(
                image=request_json.get("image"),
                title=request_json.get("title"),
                content=request_json.get("content"),
                type=request_json.get("type"),
                user=user,
            )

            db.session.add(new_listing)
            db.session.commit()

            return make_response(
                jsonify(
                    new_listing.to_dict(
                        only=("image", "title", "user", "id", "content")
                    )
                ),
                201,
            )

        except Exception:
            return make_response(jsonify({}), 400)


api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Login, "/login")
api.add_resource(NextAuthLogin, "/authlogin")

api.add_resource(UserById, "/users/<int:id>")
api.add_resource(NewUser, "/new_user")
api.add_resource(UserCommentsById, "/comments/<int:id>")
api.add_resource(UserComments, "/messages")
api.add_resource(Listings, "/listings")
api.add_resource(ListingsById, "/listings/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)


