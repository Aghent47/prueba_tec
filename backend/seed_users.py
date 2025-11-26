from main import app
from db import db
from models import User, DocumentType
import random

FIRST_NAMES = [
    "Carlos", "María", "Luis", "Andrea", "José", "Lucía", "Miguel", "Sofía",
    "Diego", "Valentina", "Jorge", "Camila", "Pablo", "Isabella", "Andrés",
    "Elena", "Ricardo", "Martina", "Santiago", "Paula"
]

LAST_NAMES = [
    "González", "Rodríguez", "López", "Martínez", "García", "Sánchez", "Ramírez",
    "Torres", "Flores", "Rivera", "Gutiérrez", "Vargas", "Rojas", "Romero",
    "Herrera", "Silva", "Mendoza", "Díaz", "Castro", "Paredes"
]

DEFAULT_DOCUMENT_TYPES = [ 
    "CC",
    "TI",
    "NIT",
    "PASAPORTE",
    "Other",
    ]


def ensure_document_types():
    existing = DocumentType.query.all()
    if existing:
        return [d.id for d in existing]

    ids = []
    for name in DEFAULT_DOCUMENT_TYPES:
        dt = DocumentType(name=name)
        db.session.add(dt)
    db.session.commit()
    existing = DocumentType.query.all()
    ids = [d.id for d in existing]
    return ids


def generate_email(first, last, idx):
    base = f"{first.lower()}.{last.lower()}"
    base = base.replace(" ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return f"{base}{idx}@example.com"


def seed(n=20):
    with app.app_context():
        doc_type_ids = ensure_document_types()
        created = 0
        for i in range(1, n + 1):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            email = generate_email(first, last, i)

            if User.query.filter_by(email=email).first():
                continue

            user = User(
                firstname=first,
                lastname=last,
                dni_type_id=random.choice(doc_type_ids) if doc_type_ids else 1,
                dniNumber=10000000 + i,
                email=email,
                phone=900000000 + i,
                address=f"Calle Falsa {i}"
            )
            db.session.add(user)
            created += 1

        if created:
            db.session.commit()

        total = User.query.count()
        print(f"Seeding users complete. Created={created}. Total users in DB={total}.")


if __name__ == "__main__":
    seed(20)
