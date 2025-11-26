from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Date, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import db


class PurchaseProduct(db.Model):
    __tablename__ = "purchase_products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purchase_id: Mapped[int] = mapped_column(Integer, ForeignKey("purchases.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    purchase: Mapped["Purchase"] = relationship("Purchase", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="purchase_items")


class DocumentType(db.Model):
    __tablename__ = "documents_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="dni_type")


class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_items: Mapped[list["PurchaseProduct"]] = relationship("PurchaseProduct", back_populates="product")


class Purchase(db.Model):
    __tablename__ = "purchases"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="purchases")

    items: Mapped[list["PurchaseProduct"]] = relationship("PurchaseProduct", back_populates="purchase", cascade="all, delete-orphan")

    purchase_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    purchase_total: Mapped[int] = mapped_column(Integer, nullable=True)
    purchase_type: Mapped[str] = mapped_column(String, nullable=True)
    purchase_subtotal: Mapped[int] = mapped_column(Integer, nullable=True)


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    dni_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("documents_types.id"), nullable=False)
    dni_type: Mapped[DocumentType] = relationship("DocumentType", back_populates="users")
    dniNumber: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    purchases: Mapped[list[Purchase]] = relationship("Purchase", back_populates="user")

