from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
from app import db
from app.models import Feedback, Adjustment, Followup, BatteryRecord, Profile, Task

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
        if f.howling in ['偶尔', '经常', '严重']:
            sd['howling'] += 1
        if f.discomfort in ['轻微', '有', '严重']:
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
        if r.usage_days is not None and r.usage_days > 0:
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


WARN_DAYS_BEFORE = 3
ABNORMAL_LOW_DAYS = 3
ABNORMAL_HIGH_RATIO = 2.0


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

    usage_records = [r for r in records_asc if r.usage_days is not None and r.usage_days > 0]
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


@bp.route('/battery-warnings', methods=['GET'])
def get_battery_warnings():
    today = datetime.now().date()
    profiles = Profile.query.all()

    overdue_list = []
    soon_due_list = []
    abnormal_list = []
    normal_count = 0
    no_data_count = 0
    has_abnormal_count = 0

    for profile in profiles:
        records = BatteryRecord.query.filter_by(
            profile_id=profile.id
        ).order_by(BatteryRecord.change_date.asc()).all()

        left_records = [r for r in records if r.ear == '左耳']
        right_records = [r for r in records if r.ear == '右耳']

        left_metrics = _calc_ear_metrics(left_records, today)
        right_metrics = _calc_ear_metrics(right_records, today)

        all_abnormal = left_metrics['abnormal_cycles'] + right_metrics['abnormal_cycles']
        has_abnormal = len(all_abnormal) > 0

        global_status = 'normal'
        if left_metrics['status'] == 'overdue' or right_metrics['status'] == 'overdue':
            global_status = 'overdue'
        elif left_metrics['status'] == 'soon_due' or right_metrics['status'] == 'soon_due':
            global_status = 'soon_due'
        elif left_metrics['status'] == 'no_data' and right_metrics['status'] == 'no_data':
            global_status = 'no_data'

        profile_summary = {
            'profile_id': profile.id,
            'elderly_name': profile.elderly_name,
            'contact_person': profile.contact_person,
            'contact_phone': profile.contact_phone,
            'fitting_store': profile.fitting_store,
            'status': global_status,
            'left_ear': {
                'status': left_metrics['status'],
                'last_change_date': left_metrics['last_change_date'],
                'next_expected_date': left_metrics['next_expected_date'],
                'overdue_days': left_metrics['overdue_days'],
                'avg_cycle_days': left_metrics['avg_cycle_days'],
                'abnormal_cycles': left_metrics['abnormal_cycles']
            },
            'right_ear': {
                'status': right_metrics['status'],
                'last_change_date': right_metrics['last_change_date'],
                'next_expected_date': right_metrics['next_expected_date'],
                'overdue_days': right_metrics['overdue_days'],
                'avg_cycle_days': right_metrics['avg_cycle_days'],
                'abnormal_cycles': right_metrics['abnormal_cycles']
            },
            'abnormal_cycles': all_abnormal
        }

        if global_status == 'overdue':
            overdue_list.append(profile_summary)
        elif global_status == 'soon_due':
            soon_due_list.append(profile_summary)
        elif global_status == 'normal':
            normal_count += 1
        elif global_status == 'no_data':
            no_data_count += 1

        if has_abnormal:
            has_abnormal_count += 1
            abnormal_list.append(profile_summary)

    overdue_list.sort(key=lambda p: max(p['left_ear']['overdue_days'], p['right_ear']['overdue_days']), reverse=True)
    abnormal_list.sort(key=lambda p: len(p['abnormal_cycles']), reverse=True)

    return jsonify({
        'today': today.isoformat(),
        'warn_days_before': WARN_DAYS_BEFORE,
        'summary': {
            'total_profiles': len(profiles),
            'overdue_count': len(overdue_list),
            'soon_due_count': len(soon_due_list),
            'abnormal_count': has_abnormal_count,
            'normal_count': normal_count,
            'no_data_count': no_data_count
        },
        'overdue': overdue_list,
        'soon_due': soon_due_list,
        'abnormal': abnormal_list
    })


@bp.route('/task-overview', methods=['GET'])
def get_task_overview():
    today = datetime.now().date()

    all_tasks = Task.query.all()
    total = len(all_tasks)

    completed_count = sum(1 for t in all_tasks if t.status == 'completed')
    pending_count = sum(1 for t in all_tasks if t.status == 'pending')
    in_progress_count = sum(1 for t in all_tasks if t.status == 'in_progress')
    cancelled_count = sum(1 for t in all_tasks if t.status == 'cancelled')

    overdue_count = 0
    for t in all_tasks:
        if t.due_date and t.status != 'completed' and t.due_date < today:
            overdue_count += 1

    soon_due_count = 0
    for t in all_tasks:
        if t.due_date and t.status != 'completed':
            delta = (t.due_date - today).days
            if 0 <= delta <= 3:
                soon_due_count += 1

    completion_rate = round((completed_count / total * 100), 1) if total > 0 else 0

    type_distribution = defaultdict(int)
    for t in all_tasks:
        type_distribution[t.task_type] += 1

    type_data = []
    for task_type, count in type_distribution.items():
        type_data.append({
            'type': task_type,
            'count': count,
            'percentage': round((count / total * 100), 1) if total > 0 else 0
        })
    type_data.sort(key=lambda x: x['count'], reverse=True)

    profile_tasks = defaultdict(lambda: {
        'profile_id': None,
        'elderly_name': None,
        'total': 0,
        'pending': 0,
        'in_progress': 0,
        'completed': 0,
        'overdue': 0,
        'soon_due': 0
    })

    for t in all_tasks:
        profile = Profile.query.get(t.profile_id)
        if not profile:
            continue
        pt = profile_tasks[t.profile_id]
        pt['profile_id'] = t.profile_id
        pt['elderly_name'] = profile.elderly_name
        pt['total'] += 1
        if t.status == 'pending':
            pt['pending'] += 1
        elif t.status == 'in_progress':
            pt['in_progress'] += 1
        elif t.status == 'completed':
            pt['completed'] += 1

        if t.due_date and t.status != 'completed':
            delta = (t.due_date - today).days
            if delta < 0:
                pt['overdue'] += 1
            elif delta <= 3:
                pt['soon_due'] += 1

    by_profile = list(profile_tasks.values())
    by_profile.sort(key=lambda x: (x['overdue'] + x['pending']), reverse=True)

    return jsonify({
        'today': today.isoformat(),
        'summary': {
            'total': total,
            'completed': completed_count,
            'pending': pending_count,
            'in_progress': in_progress_count,
            'cancelled': cancelled_count,
            'overdue': overdue_count,
            'soon_due': soon_due_count,
            'completion_rate': completion_rate
        },
        'type_distribution': type_data,
        'by_profile': by_profile
    })


@bp.route('/task-summary/<int:profile_id>', methods=['GET'])
def get_task_summary(profile_id):
    today = datetime.now().date()
    tasks = Task.query.filter_by(profile_id=profile_id).all()

    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == 'completed')
    pending = sum(1 for t in tasks if t.status == 'pending')
    in_progress = sum(1 for t in tasks if t.status == 'in_progress')

    overdue = 0
    soon_due = 0
    for t in tasks:
        if t.due_date and t.status != 'completed':
            delta = (t.due_date - today).days
            if delta < 0:
                overdue += 1
            elif delta <= 3:
                soon_due += 1

    completion_rate = round((completed / total * 100), 1) if total > 0 else 0

    recent_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)[:5]

    return jsonify({
        'profile_id': profile_id,
        'summary': {
            'total': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'overdue': overdue,
            'soon_due': soon_due,
            'completion_rate': completion_rate
        },
        'recent_tasks': [t.to_dict() for t in recent_tasks]
    })
