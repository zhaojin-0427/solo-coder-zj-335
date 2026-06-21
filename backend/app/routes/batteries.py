from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app import db
from app.models import BatteryRecord, Profile

bp = Blueprint('batteries', __name__)

WARN_DAYS_BEFORE = 3
ABNORMAL_LOW_DAYS = 3
ABNORMAL_HIGH_RATIO = 2.0


def _recompute_usage_days(profile_id, ear):
    records = BatteryRecord.query.filter_by(
        profile_id=profile_id, ear=ear
    ).order_by(BatteryRecord.change_date.asc()).all()
    for i in range(1, len(records)):
        prev = records[i - 1]
        curr = records[i]
        curr.last_change_date = prev.change_date
        curr.usage_days = (curr.change_date - prev.change_date).days
    if records:
        records[0].last_change_date = None
        records[0].usage_days = None


def _calc_ear_metrics(records_asc, today):
    if not records_asc:
        return {
            'count': 0,
            'last_change_date': None,
            'avg_cycle_days': 0,
            'min_cycle_days': 0,
            'max_cycle_days': 0,
            'next_expected_date': None,
            'overdue_days': 0,
            'status': 'no_data',
            'abnormal_cycles': []
        }

    usage_records = [r for r in records_asc if r.usage_days is not None]
    count = len(records_asc)
    last_record = records_asc[-1]
    last_change_date = last_record.change_date

    if usage_records:
        days_list = [r.usage_days for r in usage_records]
        avg_cycle = round(sum(days_list) / len(days_list), 1)
        min_cycle = min(days_list)
        max_cycle = max(days_list)
    else:
        avg_cycle = 0
        min_cycle = 0
        max_cycle = 0

    next_expected_date = None
    overdue_days = 0
    status = 'no_data'
    if avg_cycle > 0:
        next_expected_date = last_change_date + timedelta(days=int(round(avg_cycle)))
        delta = (today - next_expected_date).days
        overdue_days = max(0, delta)
        if overdue_days > 0:
            status = 'overdue'
        elif (next_expected_date - today).days <= WARN_DAYS_BEFORE:
            status = 'soon_due'
        else:
            status = 'normal'

    abnormal_cycles = []
    if usage_records and avg_cycle > 0:
        for r in usage_records:
            is_abnormal = False
            reason = None
            if r.usage_days < ABNORMAL_LOW_DAYS:
                is_abnormal = True
                reason = f'使用天数过短（{r.usage_days}天）'
            elif r.usage_days > avg_cycle * ABNORMAL_HIGH_RATIO:
                is_abnormal = True
                reason = f'使用天数过长（{r.usage_days}天，均值{avg_cycle}天）'
            if is_abnormal:
                abnormal_cycles.append({
                    'id': r.id,
                    'change_date': r.change_date.isoformat(),
                    'usage_days': r.usage_days,
                    'reason': reason
                })

    return {
        'count': count,
        'last_change_date': last_change_date.isoformat(),
        'avg_cycle_days': avg_cycle,
        'min_cycle_days': min_cycle,
        'max_cycle_days': max_cycle,
        'next_expected_date': next_expected_date.isoformat() if next_expected_date else None,
        'overdue_days': overdue_days,
        'status': status,
        'abnormal_cycles': abnormal_cycles
    }


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
    profile_id = data.get('profile_id')
    ear = data.get('ear')
    change_date_str = data.get('change_date')

    if not profile_id or not ear or not change_date_str:
        return jsonify({'error': '缺少必填字段: profile_id, ear, change_date'}), 400

    try:
        change_date = datetime.strptime(change_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': '日期格式错误，应为 YYYY-MM-DD'}), 400

    today = datetime.now().date()
    if change_date > today:
        return jsonify({'error': '更换日期不能晚于今天'}), 400

    existing_same_day = BatteryRecord.query.filter_by(
        profile_id=profile_id, ear=ear, change_date=change_date
    ).first()
    if existing_same_day:
        return jsonify({'error': f'{ear} 在 {change_date_str} 已经存在更换记录'}), 400

    profile = Profile.query.get(profile_id)
    if profile and profile.fitting_date and change_date < profile.fitting_date:
        return jsonify({'error': '更换日期不能早于验配日期'}), 400

    record = BatteryRecord(
        profile_id=profile_id,
        change_date=change_date,
        ear=ear,
        battery_type=data.get('battery_type'),
        battery_brand=data.get('battery_brand'),
        notes=data.get('notes')
    )
    db.session.add(record)
    db.session.flush()
    _recompute_usage_days(profile_id, ear)

    all_ear = BatteryRecord.query.filter_by(
        profile_id=profile_id, ear=ear
    ).order_by(BatteryRecord.change_date.asc()).all()
    for r in all_ear:
        if r.usage_days is not None and r.usage_days < 0:
            db.session.rollback()
            return jsonify({'error': '日期顺序错误：新记录日期早于前序记录，将导致负数使用天数'}), 400

    db.session.commit()
    return jsonify(record.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_battery_record(id):
    record = BatteryRecord.query.get_or_404(id)
    data = request.get_json()

    old_profile_id = record.profile_id
    old_ear = record.ear
    old_change_date = record.change_date

    new_profile_id = data.get('profile_id', old_profile_id)
    new_ear = data.get('ear', old_ear)
    new_change_date_str = data.get('change_date')

    new_change_date = old_change_date
    if new_change_date_str:
        try:
            new_change_date = datetime.strptime(new_change_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': '日期格式错误，应为 YYYY-MM-DD'}), 400

        today = datetime.now().date()
        if new_change_date > today:
            return jsonify({'error': '更换日期不能晚于今天'}), 400

        profile = Profile.query.get(new_profile_id)
        if profile and profile.fitting_date and new_change_date < profile.fitting_date:
            return jsonify({'error': '更换日期不能早于验配日期'}), 400

    if new_change_date_str or new_profile_id != old_profile_id or new_ear != old_ear:
        dup_check = BatteryRecord.query.filter(
            BatteryRecord.profile_id == new_profile_id,
            BatteryRecord.ear == new_ear,
            BatteryRecord.change_date == new_change_date,
            BatteryRecord.id != id
        ).first()
        if dup_check:
            return jsonify({'error': f'{new_ear} 在 {new_change_date.isoformat()} 已经存在更换记录'}), 400

    record.profile_id = new_profile_id
    record.change_date = new_change_date
    record.ear = new_ear
    record.battery_type = data.get('battery_type', record.battery_type)
    record.battery_brand = data.get('battery_brand', record.battery_brand)
    record.notes = data.get('notes', record.notes)

    affected_pairs = set()
    affected_pairs.add((old_profile_id, old_ear))
    affected_pairs.add((new_profile_id, new_ear))
    for pid, e in affected_pairs:
        _recompute_usage_days(pid, e)

    for pid, e in affected_pairs:
        all_ear = BatteryRecord.query.filter_by(
            profile_id=pid, ear=e
        ).order_by(BatteryRecord.change_date.asc()).all()
        for r in all_ear:
            if r.usage_days is not None and r.usage_days < 0:
                db.session.rollback()
                return jsonify({'error': '日期顺序错误：修改后将导致负数使用天数'}), 400

    db.session.commit()
    return jsonify(record.to_dict())


@bp.route('/<int:id>', methods=['DELETE'])
def delete_battery_record(id):
    record = BatteryRecord.query.get_or_404(id)
    profile_id = record.profile_id
    ear = record.ear
    db.session.delete(record)
    _recompute_usage_days(profile_id, ear)
    db.session.commit()
    return jsonify({'message': 'Battery record deleted successfully'})


@bp.route('/stats/<int:profile_id>', methods=['GET'])
def get_battery_stats(profile_id):
    records = BatteryRecord.query.filter_by(profile_id=profile_id).order_by(BatteryRecord.change_date.asc()).all()
    today = datetime.now().date()

    left_records = [r for r in records if r.ear == '左耳']
    right_records = [r for r in records if r.ear == '右耳']

    left_metrics = _calc_ear_metrics(left_records, today)
    right_metrics = _calc_ear_metrics(right_records, today)

    all_abnormal = left_metrics['abnormal_cycles'] + right_metrics['abnormal_cycles']
    global_status = 'normal'
    if left_metrics['status'] == 'overdue' or right_metrics['status'] == 'overdue':
        global_status = 'overdue'
    elif left_metrics['status'] == 'soon_due' or right_metrics['status'] == 'soon_due':
        global_status = 'soon_due'
    elif all_abnormal:
        global_status = 'abnormal'

    result = {
        'profile_id': profile_id,
        'today': today.isoformat(),
        'warn_days_before': WARN_DAYS_BEFORE,
        'status': global_status,
        'left_ear': left_metrics,
        'right_ear': right_metrics,
        'recent_records': [r.to_dict() for r in sorted(records, key=lambda x: x.change_date, reverse=True)[:10]]
    }

    return jsonify(result)
