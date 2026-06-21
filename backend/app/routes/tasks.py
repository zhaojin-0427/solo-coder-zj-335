from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Task

bp = Blueprint('tasks', __name__)

TASK_TYPES = ['提醒佩戴', '提醒清洁耳塞', '预约复诊', '购买电池', '观察特定场景听感', '其他']
TASK_STATUSES = ['pending', 'in_progress', 'completed', 'cancelled']
TASK_PRIORITIES = ['low', 'medium', 'high', 'urgent']


@bp.route('', methods=['GET'])
def get_tasks():
    profile_id = request.args.get('profile_id', type=int)
    status = request.args.get('status')
    task_type = request.args.get('task_type')
    is_overdue = request.args.get('is_overdue', type=bool)

    query = Task.query

    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    if status:
        query = query.filter_by(status=status)
    if task_type:
        query = query.filter_by(task_type=task_type)

    tasks = query.order_by(Task.due_date.asc().nullslast(), Task.priority.desc(), Task.created_at.desc()).all()

    result = [t.to_dict() for t in tasks]

    if is_overdue is not None:
        result = [t for t in result if t['is_overdue'] == is_overdue]

    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())


@bp.route('', methods=['POST'])
def create_task():
    data = request.get_json()

    if data.get('task_type') not in TASK_TYPES:
        return jsonify({'error': 'Invalid task type'}), 400
    if data.get('status') and data['status'] not in TASK_STATUSES:
        return jsonify({'error': 'Invalid status'}), 400
    if data.get('priority') and data['priority'] not in TASK_PRIORITIES:
        return jsonify({'error': 'Invalid priority'}), 400

    task = Task(
        profile_id=data.get('profile_id'),
        title=data.get('title'),
        task_type=data.get('task_type'),
        description=data.get('description'),
        assignee=data.get('assignee'),
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None,
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'pending'),
        notes=data.get('notes'),
        related_feedback_id=data.get('related_feedback_id'),
        related_adjustment_id=data.get('related_adjustment_id'),
        related_followup_id=data.get('related_followup_id')
    )

    if task.status == 'completed':
        task.completed_at = datetime.utcnow()
        task.completion_feedback = data.get('completion_feedback')

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    if data.get('task_type') and data['task_type'] not in TASK_TYPES:
        return jsonify({'error': 'Invalid task type'}), 400
    if data.get('status') and data['status'] not in TASK_STATUSES:
        return jsonify({'error': 'Invalid status'}), 400
    if data.get('priority') and data['priority'] not in TASK_PRIORITIES:
        return jsonify({'error': 'Invalid priority'}), 400

    task.profile_id = data.get('profile_id', task.profile_id)
    task.title = data.get('title', task.title)
    task.task_type = data.get('task_type', task.task_type)
    task.description = data.get('description', task.description)
    task.assignee = data.get('assignee', task.assignee)

    if data.get('due_date'):
        task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

    task.priority = data.get('priority', task.priority)

    old_status = task.status
    task.status = data.get('status', task.status)

    if old_status != 'completed' and task.status == 'completed':
        task.completed_at = datetime.utcnow()
        task.completion_feedback = data.get('completion_feedback')
    elif task.status == 'completed':
        task.completion_feedback = data.get('completion_feedback', task.completion_feedback)
    elif old_status == 'completed' and task.status != 'completed':
        task.completed_at = None
        task.completion_feedback = None

    task.notes = data.get('notes', task.notes)
    task.related_feedback_id = data.get('related_feedback_id', task.related_feedback_id)
    task.related_adjustment_id = data.get('related_adjustment_id', task.related_adjustment_id)
    task.related_followup_id = data.get('related_followup_id', task.related_followup_id)

    db.session.commit()
    return jsonify(task.to_dict())


@bp.route('/<int:id>/complete', methods=['POST'])
def complete_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json() or {}

    task.status = 'completed'
    task.completed_at = datetime.utcnow()
    task.completion_feedback = data.get('completion_feedback')

    db.session.commit()
    return jsonify(task.to_dict())


@bp.route('/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})


@bp.route('/meta', methods=['GET'])
def get_meta():
    return jsonify({
        'task_types': TASK_TYPES,
        'statuses': TASK_STATUSES,
        'priorities': TASK_PRIORITIES,
        'status_labels': {
            'pending': '待处理',
            'in_progress': '进行中',
            'completed': '已完成',
            'cancelled': '已取消'
        },
        'priority_labels': {
            'low': '低',
            'medium': '中',
            'high': '高',
            'urgent': '紧急'
        }
    })
