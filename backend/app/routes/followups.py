from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Followup

bp = Blueprint('followups', __name__)

@bp.route('', methods=['GET'])
def get_followups():
    profile_id = request.args.get('profile_id', type=int)
    adjustment_id = request.args.get('adjustment_id', type=int)
    query = Followup.query
    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    if adjustment_id:
        query = query.filter_by(adjustment_id=adjustment_id)
    followups = query.order_by(Followup.followup_date.desc()).all()
    return jsonify([f.to_dict() for f in followups])

@bp.route('/<int:id>', methods=['GET'])
def get_single_followup(id):
    followup = Followup.query.get_or_404(id)
    return jsonify(followup.to_dict())

@bp.route('', methods=['POST'])
def create_followup():
    data = request.get_json()
    followup = Followup(
        profile_id=data.get('profile_id'),
        adjustment_id=data.get('adjustment_id'),
        followup_date=datetime.strptime(data['followup_date'], '%Y-%m-%d').date(),
        followup_type=data.get('followup_type'),
        hearing_improvement=data.get('hearing_improvement'),
        howling_improvement=data.get('howling_improvement'),
        discomfort_improvement=data.get('discomfort_improvement'),
        adaptation_status=data.get('adaptation_status'),
        daily_usage_hours=data.get('daily_usage_hours'),
        left_ear_rating=data.get('left_ear_rating'),
        right_ear_rating=data.get('right_ear_rating'),
        overall_rating=data.get('overall_rating'),
        issues_remaining=data.get('issues_remaining'),
        suggestions=data.get('suggestions'),
        next_followup_date=datetime.strptime(data['next_followup_date'], '%Y-%m-%d').date() if data.get('next_followup_date') else None,
        notes=data.get('notes')
    )
    db.session.add(followup)
    db.session.commit()
    return jsonify(followup.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_followup(id):
    followup = Followup.query.get_or_404(id)
    data = request.get_json()
    followup.profile_id = data.get('profile_id', followup.profile_id)
    followup.adjustment_id = data.get('adjustment_id', followup.adjustment_id)
    if data.get('followup_date'):
        followup.followup_date = datetime.strptime(data['followup_date'], '%Y-%m-%d').date()
    followup.followup_type = data.get('followup_type', followup.followup_type)
    followup.hearing_improvement = data.get('hearing_improvement', followup.hearing_improvement)
    followup.howling_improvement = data.get('howling_improvement', followup.howling_improvement)
    followup.discomfort_improvement = data.get('discomfort_improvement', followup.discomfort_improvement)
    followup.adaptation_status = data.get('adaptation_status', followup.adaptation_status)
    followup.daily_usage_hours = data.get('daily_usage_hours', followup.daily_usage_hours)
    followup.left_ear_rating = data.get('left_ear_rating', followup.left_ear_rating)
    followup.right_ear_rating = data.get('right_ear_rating', followup.right_ear_rating)
    followup.overall_rating = data.get('overall_rating', followup.overall_rating)
    followup.issues_remaining = data.get('issues_remaining', followup.issues_remaining)
    followup.suggestions = data.get('suggestions', followup.suggestions)
    if data.get('next_followup_date'):
        followup.next_followup_date = datetime.strptime(data['next_followup_date'], '%Y-%m-%d').date()
    followup.notes = data.get('notes', followup.notes)
    db.session.commit()
    return jsonify(followup.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_followup(id):
    followup = Followup.query.get_or_404(id)
    db.session.delete(followup)
    db.session.commit()
    return jsonify({'message': 'Followup deleted successfully'})
