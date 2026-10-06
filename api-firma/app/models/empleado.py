from . import db

class Empleado(db.Model):
    """Modelo de tabla Empleado - Información del personal"""
    __tablename__ = 'empleado'
    
    ci = db.Column(db.String(40), primary_key=True)
    id_a = db.Column(db.Integer, db.ForeignKey('area.id_a'), nullable=True)
    id_t = db.Column(db.Integer, db.ForeignKey('turno.id_t'), nullable=True)
    id_b = db.Column(db.Integer, nullable=True)
    id_ba = db.Column(db.Integer, nullable=True)
    nombres = db.Column(db.String(40), nullable=False)
    apellidos = db.Column(db.String(40), nullable=False)
    direccion = db.Column(db.String(254), nullable=False)
    telefonos = db.Column(db.String(254), nullable=False)
    correo = db.Column(db.String(40), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    fecha_contrato = db.Column(db.Date, nullable=False)
    salario = db.Column(db.Numeric(10, 2), nullable=False)
    clave = db.Column(db.String(254), nullable=True)
    
    def __repr__(self):
        return f'<Empleado {self.ci} - {self.nombres} {self.apellidos}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'ci': self.ci,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'id_t': self.id_t,
            'id_b': self.id_b,
            'id_ba': self.id_ba
        }
