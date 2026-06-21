from app import db
from datetime import datetime

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    elderly_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    hearing_aid_model_left = db.Column(db.String(100))
    hearing_aid_model_right = db.Column(db.String(100))
    ear_config_left = db.Column(db.String(200))
    ear_config_right = db.Column(db.String(200))
    fitting_date = db.Column(db.Date)
    fitting_store = db.Column(db.String(200))
    audiologist = db.Column(db.String(100))
    common_scenarios = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'elderly_name': self.elderly_name,
            'age': self.age,
            'gender': self.gender,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'hearing_aid_model_left': self.hearing_aid_model_left,
            'hearing_aid_model_right': self.hearing_aid_model_right,
            'ear_config_left': self.ear_config_left,
            'ear_config_right': self.ear_config_right,
            'fitting_date': self.fitting_date.isoformat() if self.fitting_date else None,
            'fitting_store': self.fitting_store,
            'audiologist': self.audiologist,
            'common_scenarios': self.common_scenarios,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    feedback_date = db.Column(db.Date, nullable=False)
    scenario = db.Column(db.String(50), nullable=False)
    scenario_detail = db.Column(db.String(200))
    duration_minutes = db.Column(db.Integer)
    hearing_experience = db.Column(db.String(20))
    hearing_experience_detail = db.Column(db.Text)
    howling = db.Column(db.String(20))
    howling_detail = db.Column(db.Text)
    discomfort = db.Column(db.String(20))
    discomfort_detail = db.Column(db.Text)
    left_ear_rating = db.Column(db.Integer)
    right_ear_rating = db.Column(db.Integer)
    overall_rating = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'feedback_date': self.feedback_date.isoformat(),
            'scenario': self.scenario,
            'scenario_detail': self.scenario_detail,
            'duration_minutes': self.duration_minutes,
            'hearing_experience': self.hearing_experience,
            'hearing_experience_detail': self.hearing_experience_detail,
            'howling': self.howling,
            'howling_detail': self.howling_detail,
            'discomfort': self.discomfort,
            'discomfort_detail': self.discomfort_detail,
            'left_ear_rating': self.left_ear_rating,
            'right_ear_rating': self.right_ear_rating,
            'overall_rating': self.overall_rating,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

class Adjustment(db.Model):
    __tablename__ = 'adjustments'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    adjustment_date = db.Column(db.Date, nullable=False)
    adjuster = db.Column(db.String(100))
    left_ear_adjustment = db.Column(db.Text)
    right_ear_adjustment = db.Column(db.Text)
    program_adjustment = db.Column(db.Text)
    volume_adjustment = db.Column(db.String(200))
    feedback_suppression = db.Column(db.String(200))
    noise_reduction = db.Column(db.String(200))
    other_adjustments = db.Column(db.Text)
    reason = db.Column(db.Text)
    expected_effect = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'adjustment_date': self.adjustment_date.isoformat(),
            'adjuster': self.adjuster,
            'left_ear_adjustment': self.left_ear_adjustment,
            'right_ear_adjustment': self.right_ear_adjustment,
            'program_adjustment': self.program_adjustment,
            'volume_adjustment': self.volume_adjustment,
            'feedback_suppression': self.feedback_suppression,
            'noise_reduction': self.noise_reduction,
            'other_adjustments': self.other_adjustments,
            'reason': self.reason,
            'expected_effect': self.expected_effect,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

class Followup(db.Model):
    __tablename__ = 'followups'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    adjustment_id = db.Column(db.Integer, db.ForeignKey('adjustments.id'))
    followup_date = db.Column(db.Date, nullable=False)
    followup_type = db.Column(db.String(50))
    hearing_improvement = db.Column(db.String(20))
    howling_improvement = db.Column(db.String(20))
    discomfort_improvement = db.Column(db.String(20))
    adaptation_status = db.Column(db.String(50))
    daily_usage_hours = db.Column(db.Float)
    left_ear_rating = db.Column(db.Integer)
    right_ear_rating = db.Column(db.Integer)
    overall_rating = db.Column(db.Integer)
    issues_remaining = db.Column(db.Text)
    suggestions = db.Column(db.Text)
    next_followup_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'adjustment_id': self.adjustment_id,
            'followup_date': self.followup_date.isoformat(),
            'followup_type': self.followup_type,
            'hearing_improvement': self.hearing_improvement,
            'howling_improvement': self.howling_improvement,
            'discomfort_improvement': self.discomfort_improvement,
            'adaptation_status': self.adaptation_status,
            'daily_usage_hours': self.daily_usage_hours,
            'left_ear_rating': self.left_ear_rating,
            'right_ear_rating': self.right_ear_rating,
            'overall_rating': self.overall_rating,
            'issues_remaining': self.issues_remaining,
            'suggestions': self.suggestions,
            'next_followup_date': self.next_followup_date.isoformat() if self.next_followup_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

class BatteryRecord(db.Model):
    __tablename__ = 'battery_records'
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    change_date = db.Column(db.Date, nullable=False)
    ear = db.Column(db.String(10), nullable=False)
    battery_type = db.Column(db.String(50))
    battery_brand = db.Column(db.String(100))
    last_change_date = db.Column(db.Date)
    usage_days = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        safe_usage_days = self.usage_days if (self.usage_days is not None and self.usage_days > 0) else None
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'change_date': self.change_date.isoformat(),
            'ear': self.ear,
            'battery_type': self.battery_type,
            'battery_brand': self.battery_brand,
            'last_change_date': self.last_change_date.isoformat() if (self.last_change_date and safe_usage_days) else None,
            'usage_days': safe_usage_days,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    assignee = db.Column(db.String(100))
    due_date = db.Column(db.Date)
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    completion_feedback = db.Column(db.Text)
    completed_at = db.Column(db.DateTime)

    related_feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'))
    related_adjustment_id = db.Column(db.Integer, db.ForeignKey('adjustments.id'))
    related_followup_id = db.Column(db.Integer, db.ForeignKey('followups.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        from app import db
        profile = Profile.query.get(self.profile_id)
        is_overdue = False
        days_until_due = None
        if self.due_date and self.status != 'completed':
            today = datetime.utcnow().date()
            delta = (self.due_date - today).days
            days_until_due = delta
            is_overdue = delta < 0

        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'elderly_name': profile.elderly_name if profile else None,
            'title': self.title,
            'task_type': self.task_type,
            'description': self.description,
            'assignee': self.assignee,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'status': self.status,
            'notes': self.notes,
            'completion_feedback': self.completion_feedback,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'related_feedback_id': self.related_feedback_id,
            'related_adjustment_id': self.related_adjustment_id,
            'related_followup_id': self.related_followup_id,
            'is_overdue': is_overdue,
            'days_until_due': days_until_due,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
