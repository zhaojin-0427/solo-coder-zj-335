from app import db
from datetime import datetime, timedelta

CONSUMABLE_TYPES = ['耳塞', '导声管', '干燥盒', '电池', '清洁刷', '其他']
EAR_OPTIONS = ['左耳', '右耳', '双耳', '不适用']
SERVICE_TICKET_TYPES = ['耗材损坏', '佩戴不稳', '声音变闷', '清洁困难', '其他']
SERVICE_METHODS = ['上门服务', '到店服务']
SERVICE_TICKET_STATUSES = ['pending', 'in_progress', 'completed', 'cancelled']
LOW_STOCK_THRESHOLD = 3
REPLACEMENT_WARN_DAYS = 7

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
        if self.due_date and self.status not in ('completed', 'cancelled'):
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


class Consumable(db.Model):
    __tablename__ = 'consumables'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    consumable_type = db.Column(db.String(50), nullable=False)
    ear = db.Column(db.String(20))
    start_date = db.Column(db.Date)
    replacement_cycle_days = db.Column(db.Integer)
    stock_quantity = db.Column(db.Integer, default=0)
    last_replacement_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        from app import db
        profile = Profile.query.get(self.profile_id)

        next_replacement_date = None
        days_until_replacement = None
        is_overdue = False
        is_soon_due = False
        is_low_stock = self.stock_quantity is not None and self.stock_quantity <= LOW_STOCK_THRESHOLD

        if self.last_replacement_date and self.replacement_cycle_days:
            next_replacement_date = self.last_replacement_date + timedelta(days=self.replacement_cycle_days)
        elif self.start_date and self.replacement_cycle_days:
            next_replacement_date = self.start_date + timedelta(days=self.replacement_cycle_days)

        if next_replacement_date:
            today = datetime.utcnow().date()
            delta = (next_replacement_date - today).days
            days_until_replacement = delta
            is_overdue = delta < 0
            is_soon_due = 0 <= delta <= REPLACEMENT_WARN_DAYS

        status = 'normal'
        if is_overdue:
            status = 'overdue'
        elif is_soon_due:
            status = 'soon_due'
        elif is_low_stock:
            status = 'low_stock'

        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'elderly_name': profile.elderly_name if profile else None,
            'name': self.name,
            'consumable_type': self.consumable_type,
            'ear': self.ear,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'replacement_cycle_days': self.replacement_cycle_days,
            'stock_quantity': self.stock_quantity,
            'last_replacement_date': self.last_replacement_date.isoformat() if self.last_replacement_date else None,
            'next_replacement_date': next_replacement_date.isoformat() if next_replacement_date else None,
            'days_until_replacement': days_until_replacement,
            'notes': self.notes,
            'is_overdue': is_overdue,
            'is_soon_due': is_soon_due,
            'is_low_stock': is_low_stock,
            'status': status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


TRAINING_SCENARIOS = ['居家安静', '一对一对话', '家庭聚餐', '菜市场', '户外散步', '看电视', '打电话', '会议室', '其他']
TRAINING_PLAN_STATUSES = ['active', 'paused', 'completed', 'cancelled']
VOLUME_LEVELS = ['低', '中低', '中', '中高', '高']
REMINDER_FREQUENCIES = ['每天', '每2天', '每周', '每3天']
FATIGUE_LEVELS = ['无', '轻微', '一般', '明显', '严重']
CLARITY_LEVELS = ['完全听不清', '勉强听清', '部分听清', '大部分听清', '完全听清']


class TrainingPlan(db.Model):
    __tablename__ = 'training_plans'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    goal = db.Column(db.String(200), nullable=False)
    cycle_days = db.Column(db.Integer, nullable=False)
    daily_wear_minutes = db.Column(db.Integer, nullable=False)
    training_scenario = db.Column(db.String(50), nullable=False)
    volume_level = db.Column(db.String(20), default='中')
    reminder_frequency = db.Column(db.String(20), default='每天')
    responsible_person = db.Column(db.String(100))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        profile = Profile.query.get(self.profile_id)
        today = datetime.utcnow().date()
        records = TrainingRecord.query.filter_by(plan_id=self.id).order_by(TrainingRecord.record_date.desc()).all()

        completed_days = len(records)
        total_days = self.cycle_days
        completion_rate = round((completed_days / total_days) * 100, 1) if total_days > 0 else 0

        streak = 0
        if records:
            check_date = today
            date_set = {r.record_date for r in records}
            while check_date in date_set:
                streak += 1
                check_date -= timedelta(days=1)

        recent_7 = []
        for i in range(7):
            d = today - timedelta(days=6 - i)
            rec = next((r for r in records if r.record_date == d), None)
            recent_7.append({
                'date': d.isoformat(),
                'completed': rec is not None,
                'actual_wear_minutes': rec.actual_wear_minutes if rec else None,
                'clarity_level': rec.clarity_level if rec else None,
                'fatigue_level': rec.fatigue_level if rec else None,
                'has_discomfort': rec.has_discomfort if rec else None
            })

        abnormal_alerts = []
        for r in records[:7]:
            if r.has_discomfort or r.howling or (r.fatigue_level and r.fatigue_level in ['明显', '严重']):
                alert = {'date': r.record_date.isoformat(), 'issues': []}
                if r.has_discomfort:
                    alert['issues'].append('不适')
                if r.howling:
                    alert['issues'].append(f'啸叫({r.howling})')
                if r.fatigue_level in ['明显', '严重']:
                    alert['issues'].append(f'疲劳({r.fatigue_level})')
                abnormal_alerts.append(alert)

        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'elderly_name': profile.elderly_name if profile else None,
            'goal': self.goal,
            'cycle_days': self.cycle_days,
            'daily_wear_minutes': self.daily_wear_minutes,
            'training_scenario': self.training_scenario,
            'volume_level': self.volume_level,
            'reminder_frequency': self.reminder_frequency,
            'responsible_person': self.responsible_person,
            'notes': self.notes,
            'status': self.status,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'completed_days': completed_days,
            'completion_rate': completion_rate,
            'streak_days': streak,
            'recent_7_days': recent_7,
            'abnormal_alerts': abnormal_alerts,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class TrainingRecord(db.Model):
    __tablename__ = 'training_records'

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('training_plans.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    record_date = db.Column(db.Date, nullable=False)
    actual_wear_minutes = db.Column(db.Integer)
    clarity_level = db.Column(db.String(20))
    fatigue_level = db.Column(db.String(20))
    has_discomfort = db.Column(db.Boolean, default=False)
    discomfort_detail = db.Column(db.String(200))
    howling = db.Column(db.String(20))
    howling_detail = db.Column(db.String(200))
    related_feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'))
    related_adjustment_id = db.Column(db.Integer, db.ForeignKey('adjustments.id'))
    related_followup_id = db.Column(db.Integer, db.ForeignKey('followups.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        plan = TrainingPlan.query.get(self.plan_id)
        profile = Profile.query.get(self.profile_id)
        return {
            'id': self.id,
            'plan_id': self.plan_id,
            'profile_id': self.profile_id,
            'elderly_name': profile.elderly_name if profile else None,
            'training_scenario': plan.training_scenario if plan else None,
            'record_date': self.record_date.isoformat(),
            'actual_wear_minutes': self.actual_wear_minutes,
            'clarity_level': self.clarity_level,
            'fatigue_level': self.fatigue_level,
            'has_discomfort': self.has_discomfort,
            'discomfort_detail': self.discomfort_detail,
            'howling': self.howling,
            'howling_detail': self.howling_detail,
            'related_feedback_id': self.related_feedback_id,
            'related_adjustment_id': self.related_adjustment_id,
            'related_followup_id': self.related_followup_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    consumable_id = db.Column(db.Integer, db.ForeignKey('consumables.id'))
    issue_type = db.Column(db.String(50), nullable=False)
    service_method = db.Column(db.String(50))
    appointment_time = db.Column(db.DateTime)
    handler = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    result = db.Column(db.Text)
    description = db.Column(db.Text)
    photo_urls = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        from app import db
        profile = Profile.query.get(self.profile_id)
        consumable = Consumable.query.get(self.consumable_id) if self.consumable_id else None

        photo_list = []
        if self.photo_urls:
            try:
                import json
                photo_list = json.loads(self.photo_urls)
            except (json.JSONDecodeError, TypeError):
                photo_list = [u.strip() for u in self.photo_urls.split(',') if u.strip()]

        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'elderly_name': profile.elderly_name if profile else None,
            'consumable_id': self.consumable_id,
            'consumable_name': consumable.name if consumable else None,
            'issue_type': self.issue_type,
            'service_method': self.service_method,
            'appointment_time': self.appointment_time.isoformat() if self.appointment_time else None,
            'handler': self.handler,
            'status': self.status,
            'result': self.result,
            'description': self.description,
            'photo_urls': photo_list,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
