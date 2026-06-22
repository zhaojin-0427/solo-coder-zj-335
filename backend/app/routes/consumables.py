from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Consumable, Profile, CONSUMABLE_TYPES, EAR_OPTIONS

bp = Blueprint('consumables', __name__)


def parse_bool_arg(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return str(value).lower() in ('true', '1', 'yes')


@bp.route('', methods=['GET'])
def get_consumables():
    profile_id = request.args.get('profile_id', type=int)
    consumable_type = request.args.get('consumable_type')
    ear = request.args.get('ear')
    is_low_stock_raw = request.args.get('is_low_stock')
    is_low_stock = parse_bool_arg(is_low_stock_raw)
    needs_replacement_raw = request.args.get('needs_replacement')
    needs_replacement = parse_bool_arg(needs_replacement_raw)

    query = Consumable.query

    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    if consumable_type:
        query = query.filter_by(consumable_type=consumable_type)
    if ear:
        query = query.filter_by(ear=ear)

    consumables = query.order_by(Consumable.created_at.desc()).all()

    result = [c.to_dict() for c in consumables]

    if is_low_stock is not None:
        result = [c for c in result if c['is_low_stock'] == is_low_stock]
    if needs_replacement is not None:
        result = [c for c in result if (c['is_overdue'] or c['is_soon_due']) == needs_replacement]

    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def get_consumable(id):
    consumable = Consumable.query.get_or_404(id)
    return jsonify(consumable.to_dict())


@bp.route('', methods=['POST'])
def create_consumable():
    data = request.get_json()

    if not data.get('profile_id'):
        return jsonify({'error': 'profile_id is required'}), 400
    if not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    if data.get('consumable_type') not in CONSUMABLE_TYPES:
        return jsonify({'error': f'Invalid consumable_type, must be one of: {CONSUMABLE_TYPES}'}), 400
    if data.get('ear') and data['ear'] not in EAR_OPTIONS:
        return jsonify({'error': f'Invalid ear, must be one of: {EAR_OPTIONS}'}), 400

    profile = Profile.query.get(data.get('profile_id'))
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404

    consumable = Consumable(
        profile_id=data.get('profile_id'),
        name=data.get('name'),
        consumable_type=data.get('consumable_type'),
        ear=data.get('ear'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
        replacement_cycle_days=data.get('replacement_cycle_days'),
        stock_quantity=data.get('stock_quantity', 0),
        last_replacement_date=datetime.strptime(data['last_replacement_date'], '%Y-%m-%d').date() if data.get('last_replacement_date') else None,
        notes=data.get('notes')
    )

    db.session.add(consumable)
    db.session.commit()
    return jsonify(consumable.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_consumable(id):
    consumable = Consumable.query.get_or_404(id)
    data = request.get_json()

    if data.get('consumable_type') and data['consumable_type'] not in CONSUMABLE_TYPES:
        return jsonify({'error': f'Invalid consumable_type, must be one of: {CONSUMABLE_TYPES}'}), 400
    if data.get('ear') and data['ear'] not in EAR_OPTIONS:
        return jsonify({'error': f'Invalid ear, must be one of: {EAR_OPTIONS}'}), 400

    consumable.profile_id = data.get('profile_id', consumable.profile_id)
    consumable.name = data.get('name', consumable.name)
    consumable.consumable_type = data.get('consumable_type', consumable.consumable_type)
    consumable.ear = data.get('ear', consumable.ear)

    if data.get('start_date'):
        consumable.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    if data.get('last_replacement_date'):
        consumable.last_replacement_date = datetime.strptime(data['last_replacement_date'], '%Y-%m-%d').date()

    consumable.replacement_cycle_days = data.get('replacement_cycle_days', consumable.replacement_cycle_days)
    consumable.stock_quantity = data.get('stock_quantity', consumable.stock_quantity)
    consumable.notes = data.get('notes', consumable.notes)

    db.session.commit()
    return jsonify(consumable.to_dict())


@bp.route('/<int:id>', methods=['DELETE'])
def delete_consumable(id):
    consumable = Consumable.query.get_or_404(id)
    db.session.delete(consumable)
    db.session.commit()
    return jsonify({'message': 'Consumable deleted successfully'})


@bp.route('/meta', methods=['GET'])
def get_meta():
    return jsonify({
        'consumable_types': CONSUMABLE_TYPES,
        'ear_options': EAR_OPTIONS,
        'status_labels': {
            'normal': '正常',
            'soon_due': '即将更换',
            'overdue': '已逾期',
            'low_stock': '库存不足'
        }
    })
