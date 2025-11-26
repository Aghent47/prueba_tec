from main import app
from db import db
from models import DocumentType

DOCUMENT_TYPES = [
    "CC",
    "TI",
    "NIT",
    "PASAPORTE",
    "Other",
]


def seed():
    with app.app_context():
        created = 0
        for name in DOCUMENT_TYPES:
            existing = DocumentType.query.filter_by(name=name).first()
            if not existing:
                db.session.add(DocumentType(name=name))
                created += 1
        if created:
            db.session.commit()
        print(f"Seeding complete. Created={created}. Total target types={len(DOCUMENT_TYPES)}")


if __name__ == "__main__":
    seed()
