from flask import Flask, jsonify, request
from db import db
from flask_migrate import Migrate
import models

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///falabella.db"
db.init_app(app)
migrate = Migrate(app, db)


@app.after_request
def add_cors_headers(response):
    response.headers.setdefault("Access-Control-Allow-Origin", "*")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response


@app.route("/document-types", methods=["GET"])
def get_document_types():
    try:
        types = models.DocumentType.query.order_by(models.DocumentType.id).all()
        result = [{"id": t.id, "name": t.name} for t in types]
        return make_response_data(result)
    except Exception as e:
        return make_response_error("Error fetching document types", str(e))


def make_response_data(payload, status=200):
    return jsonify({"data": payload}), status


def make_response_error(message, details=None, status=500):
    body = {"data": None, "error": {"message": message}}
    if details:
        body["error"]["details"] = details
    return jsonify(body), status


@app.route('/users/dni/<int:dniNumber>', methods=['GET'])
def get_user_by_dniNumber(dniNumber: int):
    try:
        user = models.User.query.filter_by(dniNumber=dniNumber).first()
        if not user:
            return make_response_error(f"Usuario con documento {dniNumber} no encontrado", None, 404)

        payload = {
            "document_number": user.dniNumber,
            "first_name": user.firstname,
            "last_name": user.lastname,
            "email": user.email,
            "phone": user.phone,
        }

        return make_response_data(payload)
    except Exception as e:
        return make_response_error("Error al obtener usuario", str(e), 500)


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        per_page = min(per_page, 100)

        query = models.User.query.order_by(models.User.id)
        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()

        items = []
        for user in users:
            items.append({
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "dni_type_id": user.dni_type_id,
                "dniNumber": user.dniNumber,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            })

        total_pages = (total + per_page - 1) // per_page if per_page else 0
        meta = {"total": total, "page": page, "per_page": per_page, "total_pages": total_pages}

        return make_response_data({"items": items, "meta": meta})
    except Exception as e:
        return make_response_error("Error fetching users", str(e), 500)


@app.route('/users/<int:user_id>/purchases', methods=['GET'])
def get_purchases_by_user_id(user_id: int):
    try:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")

        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        per_page = min(per_page, 100)

        query = models.Purchase.query.filter_by(user_id=user_id)

        from datetime import datetime
        try:
            if start_date_str:
                sd = datetime.fromisoformat(start_date_str)
                query = query.filter(models.Purchase.purchase_date >= sd)
            if end_date_str:
                ed = datetime.fromisoformat(end_date_str)
                query = query.filter(models.Purchase.purchase_date <= ed)
        except ValueError:
            return make_response_error("Invalid date format. Use ISO format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS", None, 400)

        query = query.order_by(models.Purchase.purchase_date.desc())

        total = query.count()
        purchases = query.offset((page - 1) * per_page).limit(per_page).all()

        items = []
        for p in purchases:
            prods = []
            for item in p.items:
                prod = item.product
                prods.append({"id": prod.id, "name": prod.name, "price": prod.price, "quantity": item.quantity})

            pd = None
            if p.purchase_date is not None:
                try:
                    pd = p.purchase_date.isoformat()
                except Exception:
                    pd = str(p.purchase_date)

            items.append({
                "id": p.id,
                "purchase_date": pd,
                "purchase_subtotal": p.purchase_subtotal,
                "purchase_total": p.purchase_total,
                "purchase_type": p.purchase_type,
                "products": prods,
            })

        total_pages = (total + per_page - 1) // per_page if per_page else 0
        meta = {"total": total, "page": page, "per_page": per_page, "total_pages": total_pages}

        return make_response_data({"purchases": items, "meta": meta})
    except Exception as e:
        return make_response_error("Error fetching purchases", str(e), 500)
