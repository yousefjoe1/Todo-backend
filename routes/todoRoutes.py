from database.db import db
from flask import request, jsonify,Blueprint

from models.todo import Todos

todo_route =Blueprint('todos',__name__,url_prefix='/api/')

# Get todos
@todo_route.route("/todos",methods=['GET'])
def get_Todos():
    myTodos = Todos.query.all()
    todo_dicts = [todo.to_json() for todo in myTodos]
    return {'result': todo_dicts},200


# Make a todo
@todo_route.route("/todos",methods=['POST'])
def make_Todo():
    try:
        data = request.json

        title = data.get('title')
        details = data.get('details')
        done = data.get('done')

        new_todo = Todos(title=title ,details=details,done=done)

        db.session.add(new_todo)
        db.session.commit()

        return {"msg":"Todo created"},201
    except Exception as e:
        print(f'error : = {e}')
        return e


@todo_route.route("/todos/<int:id>",methods=['DELETE'])
def delete_Todo(id):
    try:

        todo = Todos.query.get(id)
        if todo is None:
            return jsonify({"error":"Not Exits"},404) # 404 mean not found
        
        db.session.delete(todo)
        db.session.commit()
        deleted_todo = todo.to_json()
        return jsonify({"msg":f"Deleted {deleted_todo} "},404) # 404 mean not found

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"an error {e}"})


@todo_route.route("/todos/<int:id>",methods=['GET'])
def get_Todo(id):
    print(id,'todo id')
    try:
        todo = Todos.query.get(id)
        if todo is None:
            return {"error":"Not Exits"},404 # 404 mean not found
        else:
            return {"msg":f"get todo","todo":todo.to_json()},200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"an error {e}"})


# Update a todo
@todo_route.route("/todos/<int:id>",methods=['PUT'])
def update_Todo(id):
    # print('update',id)
    try:
        todo = Todos.query.get(id)
        if todo is None:
            return {"error":"Not Exits"},404 # 404 mean not found
        
        data = request.json

        todo.title = data.get('title',todo.title)
        todo.details = data.get('details',todo.details)
        todo.done = data.get('done',todo.done)

        db.session.add(todo)
        db.session.commit()

        return {"msg":"Todo Updated"},201
    except Exception as e:
        print(f'error : = {e}')
        return e