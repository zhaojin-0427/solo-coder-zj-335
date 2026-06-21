from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app import db
from app.models import BatteryRecord

bp = Blueprint('batteries', __name__)

@bp.route('', methods=['GET'])
def get_battery_records():
    profile_id = request.args.get('profile_id', type=int)
    ear = request.args.get('ear')
    query = BatteryRecord.query
    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    if ear:
        query = query.filter_by(ear=ear)
    records = query.order_by(BatteryRecord.change_date.desc()).all()
    return jsonify([r.to_dict() for r in records])

@bp.route('/<int:id>', methods=['GET'])
def get_single_battery_record(id):
    record = BatteryRecord.query.get_or_404(id)
    return jsonify(record.to_dict())

@bp.route('', methods=['POST'])
def create_battery_record():
    data = request.get_json()
    
    last_record = BatteryRecord.query.filter_by(
        profile_id=data.get('profile_id'),
        ear=data.get('ear')
    ).order_by(BatteryRecord.change_date.desc()).first()
    
    usage_days = None
    last_change_date = None
    if last_record:
        last_change_date = last_record.change_date
        current_change_date = datetime.strptime(data['change_date'], '%Y-%m-%d').date()
        usage_days = (current_change_date - last_change_date).days
    
    record = BatteryRecord(
        profile_id=data.get('profile_id'),
        change_date=datetime.strptime(data['change_date'], '%Y-%m-%d').date(),
        ear=data.get('ear'),
        battery_type=data.get('battery_type'),
        battery_brand=data.get('battery_brand'),
        last_change_date=last_change_date,
        usage_days=usage_days,
        notes=data.get('notes')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_battery_record(id):
    record = BatteryRecord.query.get_or_404(id)
    data = request.get_json()
    record.profile_id = data.get('profile_id', record.profile_id)
    if data.get('change_date'):
        record.change_date = datetime.strptime(data['change_date'], '%Y-%m-%d').date()
    record.ear = data.get('ear', record.ear)
    record.battery_type = data.get('battery_type', record.battery_type)
    record.battery_brand = data.get('battery_brand', record.battery_brand)
    record.notes = data.get('notes', record.notes)
    db.session.commit()
    return jsonify(record.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_battery_record(id):
    record = BatteryRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Battery record deleted successfully'})

@bp.route('/stats/<int:profile_id>', methods=['GET'])
def get_battery_stats(profile_id):
    records = BatteryRecord.query.filter_by(profile_id=profile_id).order_by(BatteryRecord.change_date.desc()).all()
    
    left_records = [r for r in records if r.ear == '左耳' and r.usage_days]
    right_records = [r for r in records if r.ear == '右耳' and r.usage_days]
    
    def calc_stats(recs):
        if not recs:
            return {'count': 0, 'avg_days': 0, 'min_days': 0, 'max_days': 0, 'avg': 0, 'min': 0, 'max': 0}
        days = [r.usage_days for r in recs]
        avg_val = round(sum(days) / len(days), 1)
        min_val = min(days)
        max_val = max(days)
        return {
            'count': len(recs),
            'avg_days': avg_val,
            'min_days': min_val,
            'max_days': max_val,
            'avg': avg_val,
            'min': min_val,
            'max': max_val
        }
    
    def get_next_change(recs):
        if not recs:
            return None
        stats = calc_stats(recs)
        if stats['avg_days'] == 0:
            return None
        last_date = recs[0].change_date
        next_date = last_date + timedelta(days=stats['avg_days'])
        return next_date.isoformat()
    
    result = {
        'left_ear': calc_stats(left_records),
        'right_ear': calc_stats(right_records),
        'next_left_change': get_next_change(left_records),
        'next_right_change': get_next_change(right_records),
        'recent_records': [r.to_dict() for r in records[:10]]
    }
    
    return jsonify(result)
