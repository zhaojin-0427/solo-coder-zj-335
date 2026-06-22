from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import ServiceTicket, Consumable, Profile, SERVICE_TICKET_TYPES, SERVICE_METHODS, SERVICE_TICKET_STATUSES

bp = Blueprint('service_tickets', __name__)


@bp.route('', methods=['GET'])
def get_service_tickets():
    profile_id = request.args.get('profile_id', type=int)
    status = request.args.get('status')
    issue_type = request.args.get('issue_type')
    service_method = request.args.get('service_method')

    query = ServiceTicket.query

    if profile_id:
        query = query.filter_by(profile_id=profile_id)
    if status:
        query = query.filter_by(status=status)
    if issue_type:
        query = query.filter_by(issue_type=issue_type)
    if service_method:
        query = query.filter_by(service_method=service_method)

    tickets = query.order_by(ServiceTicket.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tickets])


@bp.route('/<int:id>', methods=['GET'])
def get_service_ticket(id):
    ticket = ServiceTicket.query.get_or_404(id)
    return jsonify(ticket.to_dict())


@bp.route('', methods=['POST'])
def create_service_ticket():
    data = request.get_json()

    if not data.get('profile_id'):
        return jsonify({'error': 'profile_id is required'}), 400
    if not data.get('issue_type'):
        return jsonify({'error': 'issue_type is required'}), 400
    if data.get('issue_type') not in SERVICE_TICKET_TYPES:
        return jsonify({'error': f'Invalid issue_type, must be one of: {SERVICE_TICKET_TYPES}'}), 400
    if data.get('service_method') and data['service_method'] not in SERVICE_METHODS:
        return jsonify({'error': f'Invalid service_method, must be one of: {SERVICE_METHODS}'}), 400
    if data.get('status') and data['status'] not in SERVICE_TICKET_STATUSES:
        return jsonify({'error': f'Invalid status, must be one of: {SERVICE_TICKET_STATUSES}'}), 400

    profile = Profile.query.get(data.get('profile_id'))
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404

    if data.get('consumable_id'):
        consumable = Consumable.query.get(data.get('consumable_id'))
        if not consumable:
            return jsonify({'error': 'Consumable not found'}), 404

    import json
    photo_urls_str = None
    if data.get('photo_urls'):
        if isinstance(data['photo_urls'], list):
            photo_urls_str = json.dumps(data['photo_urls'])
        elif isinstance(data['photo_urls'], str):
            photo_urls_str = data['photo_urls']

    appointment_time = None
    if data.get('appointment_time'):
        try:
            appointment_time = datetime.fromisoformat(data['appointment_time'].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return jsonify({'error': 'Invalid appointment_time format, use ISO format'}), 400

    ticket = ServiceTicket(
        profile_id=data.get('profile_id'),
        consumable_id=data.get('consumable_id'),
        issue_type=data.get('issue_type'),
        service_method=data.get('service_method'),
        appointment_time=appointment_time,
        handler=data.get('handler'),
        status=data.get('status', 'pending'),
        result=data.get('result'),
        description=data.get('description'),
        photo_urls=photo_urls_str
    )

    db.session.add(ticket)
    db.session.commit()
    return jsonify(ticket.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_service_ticket(id):
    ticket = ServiceTicket.query.get_or_404(id)
    data = request.get_json()

    if data.get('issue_type') and data['issue_type'] not in SERVICE_TICKET_TYPES:
        return jsonify({'error': f'Invalid issue_type, must be one of: {SERVICE_TICKET_TYPES}'}), 400
    if data.get('service_method') and data['service_method'] not in SERVICE_METHODS:
        return jsonify({'error': f'Invalid service_method, must be one of: {SERVICE_METHODS}'}), 400
    if data.get('status') and data['status'] not in SERVICE_TICKET_STATUSES:
        return jsonify({'error': f'Invalid status, must be one of: {SERVICE_TICKET_STATUSES}'}), 400

    if data.get('consumable_id'):
        consumable = Consumable.query.get(data.get('consumable_id'))
        if not consumable:
            return jsonify({'error': 'Consumable not found'}), 404

    ticket.profile_id = data.get('profile_id', ticket.profile_id)
    ticket.consumable_id = data.get('consumable_id', ticket.consumable_id)
    ticket.issue_type = data.get('issue_type', ticket.issue_type)
    ticket.service_method = data.get('service_method', ticket.service_method)
    ticket.handler = data.get('handler', ticket.handler)
    ticket.status = data.get('status', ticket.status)
    ticket.result = data.get('result', ticket.result)
    ticket.description = data.get('description', ticket.description)

    if data.get('appointment_time'):
        try:
            ticket.appointment_time = datetime.fromisoformat(data['appointment_time'].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return jsonify({'error': 'Invalid appointment_time format, use ISO format'}), 400

    if 'photo_urls' in data:
        import json
        if isinstance(data['photo_urls'], list):
            ticket.photo_urls = json.dumps(data['photo_urls'])
        elif isinstance(data['photo_urls'], str):
            ticket.photo_urls = data['photo_urls']
        elif data['photo_urls'] is None:
            ticket.photo_urls = None

    db.session.commit()
    return jsonify(ticket.to_dict())


@bp.route('/<int:id>', methods=['DELETE'])
def delete_service_ticket(id):
    ticket = ServiceTicket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Service ticket deleted successfully'})


@bp.route('/meta', methods=['GET'])
def get_meta():
    return jsonify({
        'issue_types': SERVICE_TICKET_TYPES,
        'service_methods': SERVICE_METHODS,
        'statuses': SERVICE_TICKET_STATUSES,
        'status_labels': {
            'pending': '待处理',
            'in_progress': '处理中',
            'completed': '已完成',
            'cancelled': '已取消'
        }
    })
