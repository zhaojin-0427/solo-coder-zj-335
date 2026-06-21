from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Feedback

bp = Blueprint('feedback', __name__)

@bp.route('', methods=['GET'])
def get_feedback():
    profile_id = request.args.get('profile_id', type=int)
    scenario = request.args.get('scenario')
    query = Feedback.query
    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    if scenario:
        query = query.filter_by(scenario=scenario)
    feedback_list = query.order_by(Feedback.feedback_date.desc()).all()
    return jsonify([f.to_dict() for f in feedback_list])

@bp.route('/<int:id>', methods=['GET'])
def get_single_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    return jsonify(feedback.to_dict())

@bp.route('', methods=['POST'])
def create_feedback():
    data = request.get_json()
    feedback = Feedback(
        profile_id=data.get('profile_id'),
        feedback_date=datetime.strptime(data['feedback_date'], '%Y-%m-%d').date(),
        scenario=data.get('scenario'),
        scenario_detail=data.get('scenario_detail'),
        duration_minutes=data.get('duration_minutes'),
        hearing_experience=data.get('hearing_experience'),
        hearing_experience_detail=data.get('hearing_experience_detail'),
        howling=data.get('howling'),
        howling_detail=data.get('howling_detail'),
        discomfort=data.get('discomfort'),
        discomfort_detail=data.get('discomfort_detail'),
        left_ear_rating=data.get('left_ear_rating'),
        right_ear_rating=data.get('right_ear_rating'),
        overall_rating=data.get('overall_rating'),
        notes=data.get('notes')
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify(feedback.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    data = request.get_json()
    feedback.profile_id = data.get('profile_id', feedback.profile_id)
    if data.get('feedback_date'):
        feedback.feedback_date = datetime.strptime(data['feedback_date'], '%Y-%m-%d').date()
    feedback.scenario = data.get('scenario', feedback.scenario)
    feedback.scenario_detail = data.get('scenario_detail', feedback.scenario_detail)
    feedback.duration_minutes = data.get('duration_minutes', feedback.duration_minutes)
    feedback.hearing_experience = data.get('hearing_experience', feedback.hearing_experience)
    feedback.hearing_experience_detail = data.get('hearing_experience_detail', feedback.hearing_experience_detail)
    feedback.howling = data.get('howling', feedback.howling)
    feedback.howling_detail = data.get('howling_detail', feedback.howling_detail)
    feedback.discomfort = data.get('discomfort', feedback.discomfort)
    feedback.discomfort_detail = data.get('discomfort_detail', feedback.discomfort_detail)
    feedback.left_ear_rating = data.get('left_ear_rating', feedback.left_ear_rating)
    feedback.right_ear_rating = data.get('right_ear_rating', feedback.right_ear_rating)
    feedback.overall_rating = data.get('overall_rating', feedback.overall_rating)
    feedback.notes = data.get('notes', feedback.notes)
    db.session.commit()
    return jsonify(feedback.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback deleted successfully'})

@bp.route('/suggestions/<int:profile_id>', methods=['GET'])
def get_suggestions(profile_id):
    feedback_list = Feedback.query.filter_by(profile_id=profile_id).all()
    suggestions = []
    
    scenario_stats = {}
    for f in feedback_list:
        if f.scenario not in scenario_stats:
            scenario_stats[f.scenario] = {'count': 0, 'poor_hearing': 0, 'howling': 0, 'discomfort': 0, 'ratings': []}
        scenario_stats[f.scenario]['count'] += 1
        if f.hearing_experience in ['差', '很差']:
            scenario_stats[f.scenario]['poor_hearing'] += 1
        if f.howling in ['经常', '偶尔']:
            scenario_stats[f.scenario]['howling'] += 1
        if f.discomfort in ['有', '严重']:
            scenario_stats[f.scenario]['discomfort'] += 1
        if f.overall_rating:
            scenario_stats[f.scenario]['ratings'].append(f.overall_rating)
    
    for scenario, stats in scenario_stats.items():
        if stats['count'] >= 2:
            avg_rating = sum(stats['ratings']) / len(stats['ratings']) if stats['ratings'] else 0
            issues = []
            if stats['poor_hearing'] >= 1:
                issues.append(f'听力效果不佳（{stats["poor_hearing"]}次）')
            if stats['howling'] >= 1:
                issues.append(f'存在啸叫问题（{stats["howling"]}次）')
            if stats['discomfort'] >= 1:
                issues.append(f'有不适反应（{stats["discomfort"]}次）')
            
            if issues:
                suggestion = {
                    'scenario': scenario,
                    'feedback_count': stats['count'],
                    'average_rating': round(avg_rating, 1),
                    'issues': issues,
                    'recommendations': generate_recommendations(scenario, stats)
                }
                suggestions.append(suggestion)
    
    suggestions.sort(key=lambda x: len(x['issues']), reverse=True)
    return jsonify(suggestions)

def generate_recommendations(scenario, stats):
    recs = []
    if scenario == '菜市场':
        if stats['howling'] > 0:
            recs.append('建议开启降噪模式，降低环境噪音干扰')
        if stats['poor_hearing'] > 0:
            recs.append('建议调整言语聚焦功能，优先放大前方语音')
    elif scenario == '家庭聚餐':
        if stats['poor_hearing'] > 0:
            recs.append('建议开启多人对话模式，增强周围语音收集')
        if stats['howling'] > 0:
            recs.append('建议降低整体音量，检查耳塞是否佩戴到位')
    elif scenario == '看电视':
        if stats['poor_hearing'] > 0:
            recs.append('建议开启电视音频直连功能，减少环境干扰')
        if stats['discomfort'] > 0:
            recs.append('建议调整高音/低音平衡，避免声音过于尖锐')
    elif scenario == '户外散步':
        if stats['howling'] > 0:
            recs.append('建议开启风噪声抑制功能')
        if stats['poor_hearing'] > 0:
            recs.append('建议调整户外模式，增强方向性语音接收')
    else:
        recs.append('建议咨询验配师，根据具体情况调整参数')
    
    if stats['discomfort'] > 0:
        recs.append('建议检查耳道情况，确保助听器佩戴舒适')
    
    return recs
