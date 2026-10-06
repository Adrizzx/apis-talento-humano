from . import db
from datetime import datetime

class Firma(db.Model):
    """Modelo de tabla Firma - Registro de asistencia y firmas"""
    __tablename__ = 'firma'
    
    id_f = db.Column(db.Integer, primary_key=True)
    fecha_firma = db.Column(db.Date, default=None, nullable=True)
    h_i_jornada = db.Column(db.Time, default=None, nullable=True)
    a_i_jornada = db.Column(db.Time, default=None, nullable=True)
    h_i_break = db.Column(db.Time, default=None, nullable=True)
    h_f_break = db.Column(db.Time, default=None, nullable=True)
    a_f_break = db.Column(db.Time, default=None, nullable=True)
    h_i_almuerzo = db.Column(db.Time, default=None, nullable=True)
    h_f_almuerzo = db.Column(db.Time, default=None, nullable=True)
    a_f_almuerzo = db.Column(db.Time, default=None, nullable=True)
    h_f_jornada = db.Column(db.Time, default=None, nullable=True)
    ci = db.Column(db.String(40), db.ForeignKey('empleado.ci'), nullable=False)
    id_t = db.Column(db.Integer, db.ForeignKey('turno.id_t'), nullable=False)
    id_b = db.Column(db.Integer, nullable=False)
    id_ba = db.Column(db.Integer, nullable=False)
    observacion = db.Column(db.String(254), default=None, nullable=True)
    
    # Relaciones
    empleado = db.relationship('Empleado', backref='firmas', lazy=True)
    turno = db.relationship('Turno', backref='firmas', lazy=True)
    
    def __repr__(self):
        return f'<Firma {self.id_f} - CI: {self.ci} - Fecha: {self.fecha_firma}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id_f': self.id_f,
            'fecha_firma': self.fecha_firma.isoformat() if self.fecha_firma else None,
            'h_i_jornada': self.h_i_jornada.isoformat() if self.h_i_jornada else None,
            'a_i_jornada': self.a_i_jornada.isoformat() if self.a_i_jornada else None,
            'h_i_break': self.h_i_break.isoformat() if self.h_i_break else None,
            'h_f_break': self.h_f_break.isoformat() if self.h_f_break else None,
            'a_f_break': self.a_f_break.isoformat() if self.a_f_break else None,
            'h_i_almuerzo': self.h_i_almuerzo.isoformat() if self.h_i_almuerzo else None,
            'h_f_almuerzo': self.h_f_almuerzo.isoformat() if self.h_f_almuerzo else None,
            'a_f_almuerzo': self.a_f_almuerzo.isoformat() if self.a_f_almuerzo else None,
            'h_f_jornada': self.h_f_jornada.isoformat() if self.h_f_jornada else None,
            'ci': self.ci,
            'id_t': self.id_t,
            'id_b': self.id_b,
            'id_ba': self.id_ba,
            'observacion': self.observacion
        }
