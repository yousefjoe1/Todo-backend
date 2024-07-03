from app import db

class Todos(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    title = db.Column(db.String(100),nullable=False)
    details = db.Column(db.Text(100),nullable=False)
    done = db.Column(db.Boolean,nullable=False)
    user_id = db.Column(db.Integer,nullable =True)


    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'details': self.details,
            'done': self.done,
            'user_id': self.user_id,
        }
