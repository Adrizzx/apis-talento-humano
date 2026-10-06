from . import db

class Receso(db.Model):
    """Modelo de tabla Break (Receso) - Breaks y almuerzos"""
    __tablename__ = 'break'
    
    id_b = db.Column(db.Integer, primary_key=True)
    id_t = db.Column(db.Integer, db.ForeignKey('turno.id_t'), nullable=True)
    hora_inicio_b = db.Column(db.Time, nullable=False)
    tiempo_receso_b = db.Column(db.Time, nullable=False)
    total_b = db.Column(db.Time, nullable=False)
    nombre_b = db.Column(db.String(40), nullable=False)
    descripcion_b = db.Column(db.String(40), nullable=False)
    tipo_b = db.Column(db.String(40), nullable=False)
    
    def __repr__(self):
        return f'<Receso {self.id_b} - {self.nombre_b}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_b': self.id_b,
            'nombre_b': self.nombre_b,
            'hora_inicio_b': self.hora_inicio_b.isoformat() if self.hora_inicio_b else None,
            'tiempo_receso_b': self.tiempo_receso_b.isoformat() if self.tiempo_receso_b else None,
            'total_b': self.total_b.isoformat() if self.total_b else None,
            'descripcion_b': self.descripcion_b,
            'tipo_b': self.tipo_b
        }
