from app import db


class Fakenodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doi = db.Column(db.String(255), unique=True, nullable=False)
    dep_metadata = db.Column(db.JSON, nullable=True)

    def __init__(self, doi, dep_metadata):
        self.doi = doi
        self.metadata = dep_metadata

    def __repr__(self):
        return f"<Fakenodo(id={self.id}, doi={self.doi})>"
