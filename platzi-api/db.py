from bson.json_util import dumps, ObjectId
from flask import current_app
from pymongo import MongoClient, DESCENDING
from werkzeug.local import LocalProxy


# configurating the conection with the database
def get_db():
    platzi_db = current_app.config['PLATZI_DB_URI']
    print(current_app.config['PLATZI_DB_URI'])
    client = MongoClient(platzi_db)
    return client.platzi


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def test_connection():
    return dumps(db.collection_names())


def collection_stats(collection_nombre):
    return dumps(db.command('collstats', collection_nombre))

# -----------------carreer-------------------------
def create_carreer(json):
    return str(db.carreras.insert_one(json).inserted_id)


def get_carreer_by_id(carrera_id):
    return dumps(db.carreras.find_one({'_id': ObjectId(carrera_id)}))


def update_carreer(carrera):
    # this function updates the name and description of  a carreer
    return dumps(db.carreras.update_one({'_id': ObjectId(carrera['_id'])},{ '$set' :{ 'nombre': carrera['nombre'] , 'descripcion': carrera['descripcion']}}).modified_count)


def delete_carreer_by_id(carrera_id):
    return str(db.carreras.delete_one({'_id': ObjectId(carrera_id)}).deleted_count)

# getting 5 carreer usings operators
def get_carreers(skip, limit):
    return dumps(db.carreras.find({}).skip(int(skip)).limit(int(limit)))

# adding a course into the carreers' array
def add_course(json):
    course = get_course_by_id_proyection(json['id_curso'], proyection={'nombre':1})
    return str(db.carreras.update_one({'_id': ObjectId(json['id_carrera'])}, {'$addToSet': {'cursos': course}}).modified_count)

#deleting a course from the carreers' array
def delete_course_from_carreer(json):
    return str(db.carreras.update_one({'_id':ObjectId(json['id_carrera'])},{'$pull': {'cursos': {'_id': ObjectId(json['id_curso'])}}}).modified_count)

# -----------------Cursos-------------------------

#create course
def create_course(json):
    return str(db.cursos.insert_one(json).inserted_id)

#get a course by id
def get_course_by_id(course_id):
    return dumps(db.cursos.find_one({'_id': ObjectId(course_id)}))

#updateing a course
def update_course(course):
    return str(db.cursos.update_one({'_id':ObjectId(course['_id'])},{'$set':{'nombre':course['nombre'],
                                                                             'descripcion': course['descripcion'],
                                                                             'clases':course['clases']}}).modified_count)

#deleting a course by its id 
def delete_course_by_id(course_id):
    return str(db.cursos.delete_one({'_id':ObjectId(course_id)}).deleted_count)

#get a course by id proyeccion
def get_course_by_id_proyection(course_id, proyection=None):
    return db.cursos.find_one({'_id':ObjectId(course_id)}, proyection)

#get course by name
def get_course_by_name(name):
    return dumps(db.cursos.find({'$text':{ '$search':name}}))