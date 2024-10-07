import logging
from flask import Flask, Blueprint, request, jsonify, abort
from marshmallow import Schema, fields, ValidationError
from models import Item, db
from config import Config

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

main_bp = Blueprint('main', __name__)


class ItemSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=False)


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API!"}), 200


@main_bp.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify(items_schema.dump(items)), 200


@main_bp.route('/api/items', methods=['POST'])
def add_item():
    try:
        new_item = item_schema.load(request.json)
        item = Item(**new_item)
        db.session.add(item)
        db.session.commit()
        logging.info("POST /api/items called successfully: %s", new_item)
        return jsonify(item_schema.dump(item)), 201
    except ValidationError as err:
        logging.error("Validation error: %s", err.messages)
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        logging.error("Database error: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


@main_bp.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        logging.warning("PUT /api/items/%d item not found", item_id)
        abort(404, description="Item not found")

    try:
        updated_item = item_schema.load(request.json)
        item.name = updated_item['name']
        item.description = updated_item.get('description', item.description)
        db.session.commit()
        logging.info(
            "PUT /api/items/%d called successfully: %s",
            item_id,
            updated_item
        )
        return jsonify(
            item_schema.dump(
                item
            )
        ),
        200
    except ValidationError as err:
        logging.error(
            "Validation error: %s",
            err.messages
        )
        return jsonify(
            {
                "errors": err.messages
            }
        ),
        400
    except Exception as e:
        logging.error(
            "Database error: %s",
            str(
                e
            )
        )
        return jsonify(
            {
                "error": "Internal Server Error"
            }
        ),
        500


@main_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        logging.warning("DELETE /api/items/%d item not found", item_id)
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    logging.info("DELETE /api/items/%d called successfully", item_id)
    return jsonify({"message": "Item deleted successfully"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=app.config['DEBUG'])
