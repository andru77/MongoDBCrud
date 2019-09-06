from flask import Blueprint, request, jsonify
from flask import db
import json

bp = Blueprint('carreras', __name__, url_prefix='/carreras')


@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def carreras_func():
    carrera_id = request.args.get('id')
    skip = request.args.get('skip')
    limit = request.args.get('limit')

    request_body = request.get_json()
    if request.method == 'POST':
        # Creating a carreer
        return jsonify({'_id': db.create_carreer(request_body)})
    elif request.method == 'PUT':
        # Updating name and description of the carreer
        return jsonify({'modified': db.update_carreer(request_body)})
    elif request.method == 'DELETE' and carrera_id is not None:
        # Deleting a carreer by  _id
        return jsonify({'deleted': db.delete_carreer_by_id(carrera_id)})
    elif carrera_id is not None:
        # Get carreer by _id
        result = db.consultar_carrera_por_id(carrera_id)
        return jsonify({'carreer': json.loads(result)})
    else:
        # Obtener carreras
        skip = (skip, 0)[skip is None]
        limit = (limit, 10)[limit is None]
        result = db.get_carreers(skip, limit)
        return jsonify({'carreers': json.loads(result)})


@bp.route('/agregar-curso', methods=['PUT', 'DELETE'])
def agregar_curso():
    request_body = request.get_json()
    if request.method == 'PUT':
        return jsonify({'modified': json.loads(db.add_course(request_body))})
    elif request.method == 'DELETE':
        return jsonify({'deleted': json.loads(db.delete_course_from_carreer(request_body))})


@bp.route('/test')
def test_connection():
    return jsonify({'collections': json.loads(db.test_connection())})
