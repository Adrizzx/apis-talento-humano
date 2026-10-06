from . import db

class Turno(db.Model):
    """Modelo de tabla Turno - Horarios de trabajo"""
    __tablename__ = 'turno'
    
    id_t = db.Column(db.Integer, primary_key=True)
    hora_inicio_t = db.Column(db.Time, nullable=False)
    hora_fin_t = db.Column(db.Time, nullable=False)
    total_t = db.Column(db.Time, nullable=False)
    nombre_t = db.Column(db.String(40), nullable=False)
    descripcion_t = db.Column(db.String(40), nullable=False)
    tipo_t = db.Column(db.String(40), nullable=False)
    
    def __repr__(self):
        return f'<Turno {self.id_t} - {self.nombre_t}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_t': self.id_t,
            'nombre_t': self.nombre_t,
            'hora_inicio_t': self.hora_inicio_t.isoformat() if self.hora_inicio_t else None,
            'hora_fin_t': self.hora_fin_t.isoformat() if self.hora_fin_t else None,
            'total_t': self.total_t.isoformat() if self.total_t else None,
            'descripcion_t': self.descripcion_t,
            'tipo_t': self.tipo_t
        }
