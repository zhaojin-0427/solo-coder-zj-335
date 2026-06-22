from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import TrainingPlan, TrainingRecord, TRAINING_SCENARIOS, TRAINING_PLAN_STATUSES, VOLUME_LEVELS, REMINDER_FREQUENCIES, FATIGUE_LEVELS, CLARITY_LEVELS

bp = Blueprint('training', __name__)


@bp.route('/meta', methods=['GET'])
def get_meta():
    return jsonify({
        'training_scenarios': TRAINING_SCENARIOS,
        'plan_statuses': TRAINING_PLAN_STATUSES,
        'volume_levels': VOLUME_LEVELS,
        'reminder_frequencies': REMINDER_FREQUENCIES,
        'fatigue_levels': FATIGUE_LEVELS,
        'clarity_levels': CLARITY_LEVELS,
        'status_labels': {
            'active': '进行中',
            'paused': '已暂停',
            'completed': '已完成',
            'cancelled': '已取消'
        }
    })


@bp.route('/plans', methods=['GET'])
def get_plans():
    profile_id = request.args.get('profile_id', type=int)
    status = request.args.get('status')
    scenario = request.args.get('scenario')
    has_discomfort = request.args.get('has_discomfort')

    query = TrainingPlan.query
    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    if status:
        query = query.filter_by(status=status)
    if scenario:
        query = query.filter_by(training_scenario=scenario)

    plans = query.order_by(TrainingPlan.created_at.desc()).all()

    if has_discomfort == 'true':
        result = []
        for p in plans:
            recent_records = TrainingRecord.query.filter_by(plan_id=p.id).order_by(TrainingRecord.record_date.desc()).limit(7).all()
            if any(r.has_discomfort for r in recent_records):
                result.append(p.to_dict())
        return jsonify(result)

    return jsonify([p.to_dict() for p in plans])


@bp.route('/plans/<int:id>', methods=['GET'])
def get_plan(id):
    plan = TrainingPlan.query.get_or_404(id)
    return jsonify(plan.to_dict())


@bp.route('/plans', methods=['POST'])
def create_plan():
    data = request.get_json()
    plan = TrainingPlan(
        profile_id=data.get('profile_id'),
        goal=data.get('goal'),
        cycle_days=data.get('cycle_days'),
        daily_wear_minutes=data.get('daily_wear_minutes'),
        training_scenario=data.get('training_scenario'),
        volume_level=data.get('volume_level', '中'),
        reminder_frequency=data.get('reminder_frequency', '每天'),
        responsible_person=data.get('responsible_person'),
        notes=data.get('notes'),
        status=data.get('status', 'active'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else datetime.utcnow().date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify(plan.to_dict()), 201


@bp.route('/plans/<int:id>', methods=['PUT'])
def update_plan(id):
    plan = TrainingPlan.query.get_or_404(id)
    data = request.get_json()
    plan.goal = data.get('goal', plan.goal)
    plan.cycle_days = data.get('cycle_days', plan.cycle_days)
    plan.daily_wear_minutes = data.get('daily_wear_minutes', plan.daily_wear_minutes)
    plan.training_scenario = data.get('training_scenario', plan.training_scenario)
    plan.volume_level = data.get('volume_level', plan.volume_level)
    plan.reminder_frequency = data.get('reminder_frequency', plan.reminder_frequency)
    plan.responsible_person = data.get('responsible_person', plan.responsible_person)
    plan.notes = data.get('notes', plan.notes)
    plan.status = data.get('status', plan.status)
    if data.get('start_date'):
        plan.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    if data.get('end_date'):
        plan.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    elif 'end_date' in data and data['end_date'] is None:
        plan.end_date = None
    db.session.commit()
    return jsonify(plan.to_dict())


@bp.route('/plans/<int:id>', methods=['DELETE'])
def delete_plan(id):
    plan = TrainingPlan.query.get_or_404(id)
    TrainingRecord.query.filter_by(plan_id=id).delete()
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'message': 'Training plan deleted successfully'})


@bp.route('/records', methods=['GET'])
def get_records():
    plan_id = request.args.get('plan_id', type=int)
    profile_id = request.args.get('profile_id', type=int)
    has_discomfort = request.args.get('has_discomfort')

    query = TrainingRecord.query
    if plan_id:
        query = query.filter_by(plan_id=plan_id)
    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    if has_discomfort == 'true':
        query = query.filter_by(has_discomfort=True)

    records = query.order_by(TrainingRecord.record_date.desc()).all()
    return jsonify([r.to_dict() for r in records])


@bp.route('/records/<int:id>', methods=['GET'])
def get_record(id):
    record = TrainingRecord.query.get_or_404(id)
    return jsonify(record.to_dict())


@bp.route('/records', methods=['POST'])
def create_record():
    data = request.get_json()
    record = TrainingRecord(
        plan_id=data.get('plan_id'),
        profile_id=data.get('profile_id'),
        record_date=datetime.strptime(data['record_date'], '%Y-%m-%d').date() if data.get('record_date') else datetime.utcnow().date(),
        actual_wear_minutes=data.get('actual_wear_minutes'),
        clarity_level=data.get('clarity_level'),
        fatigue_level=data.get('fatigue_level'),
        has_discomfort=data.get('has_discomfort', False),
        discomfort_detail=data.get('discomfort_detail'),
        howling=data.get('howling'),
        howling_detail=data.get('howling_detail'),
        related_feedback_id=data.get('related_feedback_id'),
        related_adjustment_id=data.get('related_adjustment_id'),
        related_followup_id=data.get('related_followup_id'),
        notes=data.get('notes')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@bp.route('/records/<int:id>', methods=['PUT'])
def update_record(id):
    record = TrainingRecord.query.get_or_404(id)
    data = request.get_json()
    if data.get('record_date'):
        record.record_date = datetime.strptime(data['record_date'], '%Y-%m-%d').date()
    record.actual_wear_minutes = data.get('actual_wear_minutes', record.actual_wear_minutes)
    record.clarity_level = data.get('clarity_level', record.clarity_level)
    record.fatigue_level = data.get('fatigue_level', record.fatigue_level)
    record.has_discomfort = data.get('has_discomfort', record.has_discomfort)
    record.discomfort_detail = data.get('discomfort_detail', record.discomfort_detail)
    record.howling = data.get('howling', record.howling)
    record.howling_detail = data.get('howling_detail', record.howling_detail)
    record.related_feedback_id = data.get('related_feedback_id', record.related_feedback_id)
    record.related_adjustment_id = data.get('related_adjustment_id', record.related_adjustment_id)
    record.related_followup_id = data.get('related_followup_id', record.related_followup_id)
    record.notes = data.get('notes', record.notes)
    db.session.commit()
    return jsonify(record.to_dict())


@bp.route('/records/<int:id>', methods=['DELETE'])
def delete_record(id):
    record = TrainingRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Training record deleted successfully'})
