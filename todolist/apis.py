from flask import Blueprint, request
from marshmallow import Schema, fields, ValidationError, validates
from db import db
import jwt
import os
from todolist.model import Todo

todo_blueprint = Blueprint('todo', __name__)

class TodoSchema(Schema):
    user_id = fields.Integer(required=False)
    todo = fields.String(required=True)
    status = fields.String(required=True)

@todo_blueprint.route('/create', methods=['POST'])
def create_todo():
    token = request.headers.get('Authorization')
    if not token:
        return {"error": "Token is missing"}, 401

    try:
        secret_key = os.getenv('SECRET_KEY')
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}, 401

    data = request.get_json()
    schema = TodoSchema()

    data.setdefault('status', 'incomplete')

    try:
        data['user_id'] = user_id
        data = schema.load(data)
    except ValidationError as err:
        return {"error": err.messages}, 400

    new_todo = Todo(user_id=user_id, todo=data['todo'], status=data['status'])
    db.session.add(new_todo)
    db.session.commit()

    return {
        'id': new_todo.id,
        'todo': new_todo.todo,
        'user_id': new_todo.user_id,
        'status': new_todo.status
    }