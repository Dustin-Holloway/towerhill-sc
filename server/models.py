from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    unit = db.Column(db.Integer)

    listings = db.relationship("Listing", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    favorites = db.relationship("Favorite", back_populates="user")

    favorited_listings = association_proxy("favorites", "listing")

    serialize_rules = (
        "-listings.user",
        "-comments.user",
        "-favorites.user",
    )

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, value):
        if self._password_hash is None:
            # User signing up with a password for the first time
            self._password_hash = Bcrypt.generate_password_hash(value.encode("utf-8"))
        else:
            # Updating the password
            self.set_password(value)

    def set_password(self, new_password):
        self._password_hash = Bcrypt.generate_password_hash(
            new_password.encode("utf-8")
        )

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))


class Listing(db.Model, SerializerMixin):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    image = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    type = db.Column(db.String)

    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    user = db.relationship("User", back_populates="listings")
    comments = db.relationship("Comment", back_populates="listing")

    serialize_rules = (
        "-user",
        "-comments",
    )


class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment_type = db.Column(db.String)
    content = db.Column(db.String, nullable=False)

    listing_id = db.Column(db.Integer, ForeignKey("listings.id"))
    user_id = db.Column(db.Integer, ForeignKey("users.id"))

    user = db.relationship("User", back_populates="comments")
    listing = db.relationship("Listing", back_populates="comments")
    favorite = db.relationship("Favorite", back_populates="comment")

    serialize_rules = ("-user", "-listings")


class Favorite(db.Model, SerializerMixin):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    comment_id = db.Column(db.Integer, ForeignKey("comments.id"))

    user = db.relationship("User", back_populates="favorites")
    comment = db.relationship("Comment", back_populates="favorite")

