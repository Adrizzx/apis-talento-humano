from . import db

class Area(db.Model):
    """Modelo de tabla Area - Áreas de trabajo"""
    __tablename__ = 'area'
    
    id_a = db.Column(db.Integer, primary_key=True)
    nombre_a = db.Column(db.String(40), nullable=False)
    descripcion_a = db.Column(db.String(254), nullable=True)
    
    def __repr__(self):
        return f'<Area {self.id_a} - {self.nombre_a}>'
