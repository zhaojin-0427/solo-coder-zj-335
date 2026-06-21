from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Adjustment

bp = Blueprint('adjustments', __name__)

@bp.route('', methods=['GET'])
def get_adjustments():
    profile_id = request.args.get('profile_id', type=int)
    query = Adjustment.query
    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    adjustments = query.order_by(Adjustment.adjustment_date.desc()).all()
    return jsonify([a.to_dict() for a in adjustments])

@bp.route('/<int:id>', methods=['GET'])
def get_single_adjustment(id):
    adjustment = Adjustment.query.get_or_404(id)
    return jsonify(adjustment.to_dict())

@bp.route('', methods=['POST'])
def create_adjustment():
    data = request.get_json()
    adjustment = Adjustment(
        profile_id=data.get('profile_id'),
        adjustment_date=datetime.strptime(data['adjustment_date'], '%Y-%m-%d').date(),
        adjuster=data.get('adjuster'),
        left_ear_adjustment=data.get('left_ear_adjustment'),
        right_ear_adjustment=data.get('right_ear_adjustment'),
        program_adjustment=data.get('program_adjustment'),
        volume_adjustment=data.get('volume_adjustment'),
        feedback_suppression=data.get('feedback_suppression'),
        noise_reduction=data.get('noise_reduction'),
        other_adjustments=data.get('other_adjustments'),
        reason=data.get('reason'),
        expected_effect=data.get('expected_effect'),
        notes=data.get('notes')
    )
    db.session.add(adjustment)
    db.session.commit()
    return jsonify(adjustment.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_adjustment(id):
    adjustment = Adjustment.query.get_or_404(id)
    data = request.get_json()
    adjustment.profile_id = data.get('profile_id', adjustment.profile_id)
    if data.get('adjustment_date'):
        adjustment.adjustment_date = datetime.strptime(data['adjustment_date'], '%Y-%m-%d').date()
    adjustment.adjuster = data.get('adjuster', adjustment.adjuster)
    adjustment.left_ear_adjustment = data.get('left_ear_adjustment', adjustment.left_ear_adjustment)
    adjustment.right_ear_adjustment = data.get('right_ear_adjustment', adjustment.right_ear_adjustment)
    adjustment.program_adjustment = data.get('program_adjustment', adjustment.program_adjustment)
    adjustment.volume_adjustment = data.get('volume_adjustment', adjustment.volume_adjustment)
    adjustment.feedback_suppression = data.get('feedback_suppression', adjustment.feedback_suppression)
    adjustment.noise_reduction = data.get('noise_reduction', adjustment.noise_reduction)
    adjustment.other_adjustments = data.get('other_adjustments', adjustment.other_adjustments)
    adjustment.reason = data.get('reason', adjustment.reason)
    adjustment.expected_effect = data.get('expected_effect', adjustment.expected_effect)
    adjustment.notes = data.get('notes', adjustment.notes)
    db.session.commit()
    return jsonify(adjustment.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_adjustment(id):
    adjustment = Adjustment.query.get_or_404(id)
    db.session.delete(adjustment)
    db.session.commit()
    return jsonify({'message': 'Adjustment deleted successfully'})
