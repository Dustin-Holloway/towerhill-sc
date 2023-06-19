#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
# from app import app
from config import app
from models import db, User, Listing, Comment

fake = Faker()

if __name__ == "__main__":
    fake = Faker()

    # Create seed data
with app.app_context():
    print("Starting seed...")

    # Delete existing data
    db.drop_all()
    db.create_all()

    # Seed users
    User.query.delete()
    for _ in range(5):
        user = User(
            username=fake.user_name(),
            password=fake.password(),
            name=fake.name(),
            image=fake.image_url(),
            unit=fake.random_int(min=1, max=10),
        )
        db.session.add(user)

    db.session.commit()

    # Seed listings
    Listing.query.delete()
    users = User.query.all()
    for _ in range(10):
        listing = Listing(
            image=fake.image_url(),
            title=fake.sentence(),
            content=fake.paragraph(),
            user=fake.random_element(users),
        )
        db.session.add(listing)

    db.session.commit()

    # Seed comments
    Comment.query.delete()
    listings = Listing.query.all()
    for _ in range(20):
        comment = Comment(
            comment_type=fake.word(),
            content=fake.sentence(),
            listing=fake.random_element(listings),
        )
        db.session.add(comment)

    db.session.commit()

    print("Seed completed successfully.")
