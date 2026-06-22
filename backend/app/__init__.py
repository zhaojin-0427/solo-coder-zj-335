from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def _repair_negative_usage_days(app):
    from app.models import BatteryRecord
    with app.app_context():
        invalid_records = BatteryRecord.query.filter(
            (BatteryRecord.usage_days < 0) | (BatteryRecord.usage_days == 0)
        ).all()
        if invalid_records:
            for r in invalid_records:
                r.usage_days = None
                r.last_change_date = None
            db.session.commit()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hearing_aid.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from app.routes import profiles, feedback, adjustments, followups, statistics, batteries, tasks, consumables, service_tickets, training
    app.register_blueprint(profiles.bp, url_prefix='/api/profiles')
    app.register_blueprint(feedback.bp, url_prefix='/api/feedback')
    app.register_blueprint(adjustments.bp, url_prefix='/api/adjustments')
    app.register_blueprint(followups.bp, url_prefix='/api/followups')
    app.register_blueprint(statistics.bp, url_prefix='/api/statistics')
    app.register_blueprint(batteries.bp, url_prefix='/api/batteries')
    app.register_blueprint(tasks.bp, url_prefix='/api/tasks')
    app.register_blueprint(consumables.bp, url_prefix='/api/consumables')
    app.register_blueprint(service_tickets.bp, url_prefix='/api/service-tickets')
    app.register_blueprint(training.bp, url_prefix='/api/training')
    
    with app.app_context():
        db.create_all()
    
    _repair_negative_usage_days(app)
    
    return app
