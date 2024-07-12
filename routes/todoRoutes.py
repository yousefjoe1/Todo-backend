from database.db import db
from flask import request, jsonify,Blueprint
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required



from models.todo import Todos
from models.users import Users


todo_route =Blueprint('todos',__name__,url_prefix='/api/')

# Get todos
@todo_route.route("/todos",methods=['GET'])
@jwt_required() 
def get_todos():

    try:

        current_user= get_jwt_identity()

        number = request.args.get('number')  # Access the 'number' parameter
        completed = request.args.get('completed')  # Access the 'number' parameter
        todos_with_auth = Todos.query.filter_by(user_id=current_user)

        if completed:
            # Filter by completed status (assuming a boolean 'done' field in your Todo model)
            try:
                completed_value = bool(completed.lower())  # Convert 'completed' to boolean (case-insensitive)
                my_todos = todos_with_auth.filter_by(done=completed_value).all()
                todo_dicts = [todo.to_json() for todo in my_todos]
                return {'result': todo_dicts}, 200
            except ValueError:
                return jsonify({'message': 'Invalid completed value: Must be "true" or "false"'}), 400


        if number:  # If a number query parameter is present
            try:
                number = int(number)  # Convert the string value to an integer
                if number <= 0:
                    return jsonify({'message': 'Invalid number: Must be positive'}), 400  # Handle invalid number
                my_todos = todos_with_auth.limit(number).all()
                todo_dicts = [todo.to_json() for todo in my_todos]
                return {'result': todo_dicts}, 200
            except ValueError:
                return jsonify({'message': 'Invalid number format: Must be an integer'}), 400  # Handle non-integer input

        else:  # If no number query parameter is provided
            my_todos = todos_with_auth.all()
            todo_dicts = [todo.to_json() for todo in my_todos]
            return {'result': todo_dicts}, 200
    except Exception as e:
        print(e)
        return {'error': e}, 422

 


# Make a todo
@todo_route.route("/todos",methods=['POST'])
@jwt_required()
def make_Todo():

    current_user= get_jwt_identity()

    try:
        data = request.json
        title = data.get('title')
        details = data.get('details')
        done = data.get('done')
        new_todo = Todos(title=title ,details=details,done=done,user_id=current_user)

        db.session.add(new_todo)
        db.session.commit()

        return {"msg":"Todo created"},201
    except Exception as e:
        print(f'error : = {e}')
        return e


@todo_route.route("/todos/<int:id>",methods=['DELETE'])
# @jwt_required()
def delete_Todo(id):
    # current_user = get_jwt_identity()

    try:
        todo = Todos.query.get(id)
        # uid = todo.to_json()['user_id']
        # if uid != current_user:
        #     return jsonify({"error": "Unauthorized deletion"}), 401

        # Delete the todo
        db.session.delete(todo)
        db.session.commit()
        deleted_todo = todo.to_json()  # Convert to JSON for response

        return jsonify({"message": f"Todo {deleted_todo} deleted successfully"}), 200
    except Exception as e:
        # Rollback the session on error
        db.session.rollback()
        print(f'Error deleting todo: {e}')  # Log the error for debugging
        return jsonify({"error": "An error occurred"}), 500


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