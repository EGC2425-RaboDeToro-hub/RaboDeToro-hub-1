from app import db


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), nullable=False)
    usedTime = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'Forgotpassword<{self.id}>'
