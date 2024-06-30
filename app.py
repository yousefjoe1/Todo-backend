from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.db import db

from routes.usersRoutes import user_route
from routes.todoRoutes import todo_route

from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///friends.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/tododb"

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)
# SQLAlchemy(app)


# import routes
# import routes

@app.route('/')
def home():
    return 'Home app.py'

app.register_blueprint(user_route)
app.register_blueprint(todo_route)

db.init_app(app)
with app.app_context():
    # db.drop_all()  # Drop existing tables (be careful!)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)