from main import app
from db import db
from models import User, Product, Purchase, PurchaseProduct
from datetime import datetime, timezone
import random

NEW_PURCHASES_PER_USER = 3
MIN_PRODUCTS_PER_PURCHASE = 1
MAX_PRODUCTS_PER_PURCHASE = 5

PURCHASE_TYPES = ["online", "store", "pickup"]


def seed(new_per_user=NEW_PURCHASES_PER_USER):
    with app.app_context():
        users = User.query.all()
        products = Product.query.all()

        if not users:
            print("No users found in DB. Run seed_users first.")
            return
        if not products:
            print("No products found in DB. Run seed_products first.")
            return

        total_created = 0
        for user in users:
            existing = Purchase.query.filter_by(user_id=user.id).count()
            if existing >= new_per_user:
                continue

            to_create = new_per_user - existing
            for _ in range(to_create):
                num_products = random.randint(MIN_PRODUCTS_PER_PURCHASE, min(MAX_PRODUCTS_PER_PURCHASE, len(products)))
                selected = random.sample(products, k=num_products)

                subtotal = sum([p.price for p in selected])
                extra = random.randint(0, int(subtotal * 0.1))
                total = subtotal + extra

                purchase = Purchase(
                    user_id=user.id,
                    purchase_date=datetime.now(timezone.utc),
                    purchase_total=total,
                    purchase_type=random.choice(PURCHASE_TYPES),
                    purchase_subtotal=subtotal,
                )
                for prod in selected:
                    qty = random.randint(1, 3)
                    assoc = PurchaseProduct(product_id=prod.id, quantity=qty)
                    purchase.items.append(assoc)

                db.session.add(purchase)
                total_created += 1
            db.session.commit()

        print(f"Seeding purchases complete. Created={total_created} (target per user={new_per_user}).")


if __name__ == "__main__":
    seed()
