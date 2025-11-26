from main import app
from db import db
from models import Product
import random

COUNT = 100
MIN_PRICE = 1000
MAX_PRICE = 100000


def seed(count=COUNT):
    with app.app_context():
        created = 0
        for i in range(1, count + 1):
            name = f"Product {i:03d}"
            if Product.query.filter_by(name=name).first():
                continue
            price = random.randint(MIN_PRICE, MAX_PRICE)
            p = Product(name=name, price=price)
            db.session.add(p)
            created += 1
            if created % 20 == 0:
                db.session.commit()
        if created % 20 != 0:
            db.session.commit()

        total = Product.query.count()
        print(f"Seeding products complete. Created={created}. Total products in DB={total}.")


if __name__ == "__main__":
    seed()
