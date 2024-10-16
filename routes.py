from flask import Blueprint, jsonify, request
from models import db, Hero, Power, HeroPower
from marshmallow import Schema, fields, ValidationError, validates

bp = Blueprint('api', __name__)

# Schema for validating HeroPower creation
class HeroPowerSchema(Schema):
    strength = fields.String(required=True)
    hero_id = fields.Integer(required=True)
    power_id = fields.Integer(required=True)


    @validates('strength')
    def validate_strength(self, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValidationError('Invalid strength value')

@bp.route('/heroes', methods=['GET'])
def get_heroes():
    """Get a list of all heroes."""
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200

@bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    """Get a single hero by ID."""
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict()), 200
    return jsonify({"error": "Hero not found"}), 404

@bp.route('/powers', methods=['GET'])
def get_powers():
    """Get a list of all powers."""
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200

@bp.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    """Get a single power by ID."""
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict()), 200
    return jsonify({"error": "Power not found"}), 404

@bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    """Create a new HeroPower association."""
    data = request.get_json()

    schema = HeroPowerSchema()
    try:
        schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    # Create new HeroPower
    new_hero_power = HeroPower(**data)
    db.session.add(new_hero_power)
    db.session.commit()

    return jsonify(new_hero_power.to_dict()), 201

@bp.route('/hero_powers/<int:id>', methods=['DELETE'])
def delete_hero_power(id):
    """Delete a HeroPower association."""
    hero_power = HeroPower.query.get(id)
    if hero_power:
        db.session.delete(hero_power)
        db.session.commit()
        return jsonify({"message": "HeroPower deleted successfully"}), 200
    return jsonify({"error": "HeroPower not found"}), 404

@bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    """Update an existing power."""
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get("description")

    if description:
        power.description = description
        db.session.commit()
        return jsonify(power.to_dict()), 200

    return jsonify({"errors": ["Description is required"]}), 400
