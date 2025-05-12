from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy extension
db = SQLAlchemy()

# Define database models
class TemperatureData(db.Model):
    __tablename__ = 'temperature_data'
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TemperatureData id={self.id} value={self.value} timestamp={self.timestamp}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'timestamp': self.timestamp.timestamp()
        }

class HumidityData(db.Model):
    __tablename__ = 'humidity_data'
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<HumidityData id={self.id} value={self.value} timestamp={self.timestamp}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'timestamp': self.timestamp.timestamp()
        }