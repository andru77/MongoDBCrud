from flask import Blueprint, request, jsonify
from flask import db
import json

bp = Blueprint('cursos', __name__, url_prefix='/cursos')


@bp.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cursos_func():
    curso_id = request.args.get('id')
    request_body = request.get_json()
    if request.method == 'POST':
        # Create a course
        return jsonify({"_id": db.create_course(request_body)})
    elif request.method == 'PUT':
        # Update name and description of the course
        return jsonify({'modified': db.update_course(request_body)})
    elif request.method == 'DELETE' and curso_id is not None:
        # Delete a course by _id
        return jsonify({'deleted:': db.delete_course_by_id(curso_id)})
    elif curso_id is not None:
        # Obtener get a course by _id
        result = db.get_course_by_id(curso_id)
        return jsonify({"clase": json.loads(result)})


@bp.route('/porNombre', methods=['POST'])
def cursos_por_nombre():
    request_body = request.get_json()
    result = db.get_course_by_name(request_body["nombre"])
    return jsonify({"courses:": json.loads(result)})


@bp.route('/stats')
def stats_collection():
    return jsonify({"collections": json.loads(db.collection_stats("cursos"))})
