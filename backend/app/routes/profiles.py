from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Profile

bp = Blueprint('profiles', __name__)

@bp.route('', methods=['GET'])
def get_profiles():
    profiles = Profile.query.order_by(Profile.created_at.desc()).all()
    return jsonify([p.to_dict() for p in profiles])

@bp.route('/<int:id>', methods=['GET'])
def get_profile(id):
    profile = Profile.query.get_or_404(id)
    return jsonify(profile.to_dict())

@bp.route('', methods=['POST'])
def create_profile():
    data = request.get_json()
    profile = Profile(
        elderly_name=data.get('elderly_name'),
        age=data.get('age'),
        gender=data.get('gender'),
        contact_person=data.get('contact_person'),
        contact_phone=data.get('contact_phone'),
        hearing_aid_model_left=data.get('hearing_aid_model_left'),
        hearing_aid_model_right=data.get('hearing_aid_model_right'),
        ear_config_left=data.get('ear_config_left'),
        ear_config_right=data.get('ear_config_right'),
        fitting_date=datetime.strptime(data['fitting_date'], '%Y-%m-%d').date() if data.get('fitting_date') else None,
        fitting_store=data.get('fitting_store'),
        audiologist=data.get('audiologist'),
        common_scenarios=data.get('common_scenarios'),
        notes=data.get('notes')
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify(profile.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_profile(id):
    profile = Profile.query.get_or_404(id)
    data = request.get_json()
    profile.elderly_name = data.get('elderly_name', profile.elderly_name)
    profile.age = data.get('age', profile.age)
    profile.gender = data.get('gender', profile.gender)
    profile.contact_person = data.get('contact_person', profile.contact_person)
    profile.contact_phone = data.get('contact_phone', profile.contact_phone)
    profile.hearing_aid_model_left = data.get('hearing_aid_model_left', profile.hearing_aid_model_left)
    profile.hearing_aid_model_right = data.get('hearing_aid_model_right', profile.hearing_aid_model_right)
    profile.ear_config_left = data.get('ear_config_left', profile.ear_config_left)
    profile.ear_config_right = data.get('ear_config_right', profile.ear_config_right)
    if data.get('fitting_date'):
        profile.fitting_date = datetime.strptime(data['fitting_date'], '%Y-%m-%d').date()
    profile.fitting_store = data.get('fitting_store', profile.fitting_store)
    profile.audiologist = data.get('audiologist', profile.audiologist)
    profile.common_scenarios = data.get('common_scenarios', profile.common_scenarios)
    profile.notes = data.get('notes', profile.notes)
    db.session.commit()
    return jsonify(profile.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_profile(id):
    profile = Profile.query.get_or_404(id)
    db.session.delete(profile)
    db.session.commit()
    return jsonify({'message': 'Profile deleted successfully'})
