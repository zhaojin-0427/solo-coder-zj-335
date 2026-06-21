from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
from app import db
from app.models import Feedback, Adjustment, Followup, BatteryRecord, Profile

bp = Blueprint('statistics', __name__)

@bp.route('/discomfort-scenarios/<int:profile_id>', methods=['GET'])
def get_discomfort_scenarios(profile_id):
    feedback_list = Feedback.query.filter_by(profile_id=profile_id).all()
    
    scenario_data = defaultdict(lambda: {
        'total': 0,
        'poor_hearing': 0,
        'howling': 0,
        'discomfort': 0,
        'avg_rating': 0,
        'ratings': []
    })
    
    for f in feedback_list:
        sd = scenario_data[f.scenario]
        sd['total'] += 1
        if f.hearing_experience in ['差', '很差']:
            sd['poor_hearing'] += 1
        if f.howling in ['经常', '偶尔']:
            sd['howling'] += 1
        if f.discomfort in ['有', '严重']:
            sd['discomfort'] += 1
        if f.overall_rating:
            sd['ratings'].append(f.overall_rating)
    
    result = []
    for scenario, data in scenario_data.items():
        data['avg_rating'] = round(sum(data['ratings']) / len(data['ratings']), 1) if data['ratings'] else 0
        data['issue_count'] = data['poor_hearing'] + data['howling'] + data['discomfort']
        result.append({
            'scenario': scenario,
            **data
        })
    
    result.sort(key=lambda x: x['issue_count'], reverse=True)
    return jsonify(result)

@bp.route('/ear-difference/<int:profile_id>', methods=['GET'])
def get_ear_difference(profile_id):
    feedback_list = Feedback.query.filter_by(profile_id=profile_id).all()
    
    scenario_ratings = defaultdict(lambda: {'left': [], 'right': []})
    overall_left = []
    overall_right = []
    
    for f in feedback_list:
        if f.left_ear_rating:
            scenario_ratings[f.scenario]['left'].append(f.left_ear_rating)
            overall_left.append(f.left_ear_rating)
        if f.right_ear_rating:
            scenario_ratings[f.scenario]['right'].append(f.right_ear_rating)
            overall_right.append(f.right_ear_rating)
    
    def avg(arr):
        return round(sum(arr) / len(arr), 1) if arr else 0
    
    result = {
        'overall': {
            'left_avg': avg(overall_left),
            'right_avg': avg(overall_right),
            'difference': round(avg(overall_left) - avg(overall_right), 1),
            'left_count': len(overall_left),
            'right_count': len(overall_right)
        },
        'by_scenario': []
    }
    
    for scenario, ratings in scenario_ratings.items():
        left_avg = avg(ratings['left'])
        right_avg = avg(ratings['right'])
        result['by_scenario'].append({
            'scenario': scenario,
            'left_avg': left_avg,
            'right_avg': right_avg,
            'difference': round(left_avg - right_avg, 1),
            'left_count': len(ratings['left']),
            'right_count': len(ratings['right'])
        })
    
    return jsonify(result)

@bp.route('/battery-cycle/<int:profile_id>', methods=['GET'])
def get_battery_cycle(profile_id):
    records = BatteryRecord.query.filter_by(profile_id=profile_id).order_by(BatteryRecord.change_date.asc()).all()
    
    left_data = []
    right_data = []
    
    for r in records:
        if r.usage_days:
            item = {
                'date': r.change_date.isoformat(),
                'usage_days': r.usage_days,
                'battery_type': r.battery_type,
                'battery_brand': r.battery_brand
            }
            if r.ear == '左耳':
                left_data.append(item)
            else:
                right_data.append(item)
    
    def calc_stats(data):
        if not data:
            return {'avg': 0, 'min': 0, 'max': 0, 'trend': 'stable'}
        days = [d['usage_days'] for d in data]
        avg_days = round(sum(days) / len(days), 1)
        
        trend = 'stable'
        if len(days) >= 3:
            first_half = sum(days[:len(days)//2]) / (len(days)//2)
            second_half = sum(days[len(days)//2:]) / (len(days) - len(days)//2)
            if second_half < first_half * 0.8:
                trend = 'declining'
            elif second_half > first_half * 1.2:
                trend = 'improving'
        
        return {
            'avg': avg_days,
            'min': min(days),
            'max': max(days),
            'trend': trend,
            'count': len(days)
        }
    
    return jsonify({
        'left_ear': {
            'records': left_data,
            'stats': calc_stats(left_data)
        },
        'right_ear': {
            'records': right_data,
            'stats': calc_stats(right_data)
        }
    })

@bp.route('/improvement-rate/<int:profile_id>', methods=['GET'])
def get_improvement_rate(profile_id):
    adjustments = Adjustment.query.filter_by(profile_id=profile_id).order_by(Adjustment.adjustment_date.asc()).all()
    
    result = []
    
    for adj in adjustments:
        before_date = adj.adjustment_date - timedelta(days=14)
        after_date = adj.adjustment_date + timedelta(days=14)
        
        before_feedback = Feedback.query.filter(
            Feedback.profile_id == profile_id,
            Feedback.feedback_date >= before_date,
            Feedback.feedback_date < adj.adjustment_date
        ).all()
        
        after_feedback = Feedback.query.filter(
            Feedback.profile_id == profile_id,
            Feedback.feedback_date > adj.adjustment_date,
            Feedback.feedback_date <= after_date
        ).all()
        
        followups = Followup.query.filter_by(
            profile_id=profile_id,
            adjustment_id=adj.id
        ).all()
        
        def avg_rating(feedback_list, field):
            ratings = [getattr(f, field) for f in feedback_list if getattr(f, field)]
            return round(sum(ratings) / len(ratings), 1) if ratings else 0
        
        def calc_improvement(before, after):
            if before == 0:
                return 0 if after == 0 else 100
            return round(((after - before) / before) * 100, 1)
        
        before_overall = avg_rating(before_feedback, 'overall_rating')
        after_overall = avg_rating(after_feedback, 'overall_rating')
        before_left = avg_rating(before_feedback, 'left_ear_rating')
        after_left = avg_rating(after_feedback, 'left_ear_rating')
        before_right = avg_rating(before_feedback, 'right_ear_rating')
        after_right = avg_rating(after_feedback, 'right_ear_rating')
        
        followup_ratings = [f.overall_rating for f in followups if f.overall_rating]
        followup_avg = round(sum(followup_ratings) / len(followup_ratings), 1) if followup_ratings else 0
        
        hearing_improved = sum(1 for f in followups if f.hearing_improvement in ['明显改善', '略有改善'])
        howling_improved = sum(1 for f in followups if f.howling_improvement in ['明显改善', '略有改善'])
        discomfort_improved = sum(1 for f in followups if f.discomfort_improvement in ['明显改善', '略有改善'])
        
        result.append({
            'adjustment_id': adj.id,
            'adjustment_date': adj.adjustment_date.isoformat(),
            'adjuster': adj.adjuster,
            'reason': adj.reason,
            'before': {
                'feedback_count': len(before_feedback),
                'overall_rating': before_overall,
                'left_rating': before_left,
                'right_rating': before_right
            },
            'after': {
                'feedback_count': len(after_feedback),
                'overall_rating': after_overall,
                'left_rating': after_left,
                'right_rating': after_right
            },
            'improvement': {
                'overall': calc_improvement(before_overall, after_overall),
                'left': calc_improvement(before_left, after_left),
                'right': calc_improvement(before_right, after_right)
            },
            'followup': {
                'count': len(followups),
                'avg_rating': followup_avg,
                'hearing_improvement_rate': round((hearing_improved / len(followups)) * 100, 1) if followups else 0,
                'howling_improvement_rate': round((howling_improved / len(followups)) * 100, 1) if followups else 0,
                'discomfort_improvement_rate': round((discomfort_improved / len(followups)) * 100, 1) if followups else 0
            }
        })
    
    total_improvements = [r['improvement']['overall'] for r in result if r['before']['feedback_count'] > 0 and r['after']['feedback_count'] > 0]
    avg_improvement = round(sum(total_improvements) / len(total_improvements), 1) if total_improvements else 0
    
    return jsonify({
        'adjustments': result,
        'summary': {
            'total_adjustments': len(adjustments),
            'average_improvement': avg_improvement,
            'improved_count': sum(1 for r in result if r['improvement']['overall'] > 0),
            'stable_count': sum(1 for r in result if r['improvement']['overall'] == 0),
            'declined_count': sum(1 for r in result if r['improvement']['overall'] < 0)
        }
    })

@bp.route('/overview/<int:profile_id>', methods=['GET'])
def get_overview(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    
    feedback_count = Feedback.query.filter_by(profile_id=profile_id).count()
    adjustment_count = Adjustment.query.filter_by(profile_id=profile_id).count()
    followup_count = Followup.query.filter_by(profile_id=profile_id).count()
    battery_count = BatteryRecord.query.filter_by(profile_id=profile_id).count()
    
    recent_feedback = Feedback.query.filter_by(profile_id=profile_id).order_by(Feedback.feedback_date.desc()).limit(5).all()
    recent_adjustments = Adjustment.query.filter_by(profile_id=profile_id).order_by(Adjustment.adjustment_date.desc()).limit(3).all()
    
    avg_rating = 0
    if feedback_count > 0:
        all_ratings = Feedback.query.filter_by(profile_id=profile_id).all()
        ratings = [f.overall_rating for f in all_ratings if f.overall_rating]
        avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0
    
    return jsonify({
        'profile': profile.to_dict(),
        'counts': {
            'feedback': feedback_count,
            'adjustment': adjustment_count,
            'followup': followup_count,
            'battery': battery_count
        },
        'average_rating': avg_rating,
        'recent_feedback': [f.to_dict() for f in recent_feedback],
        'recent_adjustments': [a.to_dict() for a in recent_adjustments]
    })

@bp.route('/trends/<int:profile_id>', methods=['GET'])
def get_trends(profile_id):
    days = request.args.get('days', 90, type=int)
    start_date = datetime.now().date() - timedelta(days=days)
    
    feedback_list = Feedback.query.filter(
        Feedback.profile_id == profile_id,
        Feedback.feedback_date >= start_date
    ).order_by(Feedback.feedback_date.asc()).all()
    
    daily_data = defaultdict(lambda: {
        'count': 0,
        'ratings': [],
        'left_ratings': [],
        'right_ratings': []
    })
    
    for f in feedback_list:
        date_str = f.feedback_date.isoformat()
        daily_data[date_str]['count'] += 1
        if f.overall_rating:
            daily_data[date_str]['ratings'].append(f.overall_rating)
        if f.left_ear_rating:
            daily_data[date_str]['left_ratings'].append(f.left_ear_rating)
        if f.right_ear_rating:
            daily_data[date_str]['right_ratings'].append(f.right_ear_rating)
    
    result = []
    for date_str in sorted(daily_data.keys()):
        data = daily_data[date_str]
        result.append({
            'date': date_str,
            'count': data['count'],
            'avg_rating': round(sum(data['ratings']) / len(data['ratings']), 1) if data['ratings'] else 0,
            'avg_left': round(sum(data['left_ratings']) / len(data['left_ratings']), 1) if data['left_ratings'] else 0,
            'avg_right': round(sum(data['right_ratings']) / len(data['right_ratings']), 1) if data['right_ratings'] else 0
        })
    
    return jsonify(result)
