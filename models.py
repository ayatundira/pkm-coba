
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Shows(db.Model):
    __tablename__ = 'SHOWS'
    
    show_id = db.Column('show_id', db.String, primary_key=True)
    name = db.Column('name', db.String)
    overview = db.Column('overview', db.String)
    adult = db.Column('adult', db.Boolean)
    in_production = db.Column('in_production', db.Boolean)
    original_name = db.Column('original_name', db.String)
    popularity = db.Column('popularity', db.Float)
    tagline = db.Column('tagline', db.String)
    episode_run_time = db.Column('episode_run_time', db.Integer)
    status_id = db.Column('status_id', db.Integer, db.ForeignKey('STATUS.status_id'))
    type_id = db.Column('type_id', db.String, db.ForeignKey('TYPES.type_id'))