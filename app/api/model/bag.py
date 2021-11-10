from app.api.db import db
from app.api.model.cuboid import Cuboid


class Bag(db.Model):
    __tablename__ = "bags"

    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=True)
    cuboids = db.relationship(Cuboid, backref="bag")
