from . import ma
from marshmallow import fields

class FirmaSchema(ma.Schema):
    # Información del empleado (nested)
    empleado = fields.Nested('EmpleadoSchema', only=['ci', 'nombres', 'apellidos'])
    turno = fields.Nested('TurnoSchema', only=['id_t', 'nombre_t'])
    
    class Meta:
        fields = (
            'id_f', 'fecha_firma', 
            'h_i_jornada', 'a_i_jornada',
            'h_i_break', 'h_f_break', 'a_f_break',
            'h_i_almuerzo', 'h_f_almuerzo', 'a_f_almuerzo',
            'h_f_jornada', 'ci', 'id_t', 'id_b', 'id_ba',
            'observacion', 'empleado', 'turno'
        )

class EmpleadoSchema(ma.Schema):
    class Meta:
        fields = ('ci', 'nombres', 'apellidos', 'id_t', 'id_b', 'id_ba')

class TurnoSchema(ma.Schema):
    class Meta:
        fields = ('id_t', 'nombre_t', 'hora_inicio_t', 'hora_fin_t')

# Instancias para serialización
firma_schema = FirmaSchema()
firmas_schema = FirmaSchema(many=True)
