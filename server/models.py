from django.db import models
from django.contrib.auth.models import User

class Cias(models.Model):   
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    logo = models.CharField(max_length=255)
    sitio_web = models.CharField(max_length=255)
    tamanio_cia = models.CharField(max_length=20)
    industria = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=100)
    class Meta:
        db_table = 'Cias'
    
#TODO: añadir la relacion con la tabla de usuarios en el campo de usuario_por_dia
class Sucursal(models.Model):
    id = models.AutoField(primary_key=True)
    id_cia = models.ForeignKey(Cias, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    lunes_apertura = models.TimeField()
    lunes_cierre = models.TimeField()
    martes_apertura = models.TimeField()
    martes_cierre = models.TimeField()
    miercoles_apertura = models.TimeField()
    miercoles_cierre = models.TimeField()
    jueves_apertura = models.TimeField()
    jueves_cierre = models.TimeField()
    viernes_apertura = models.TimeField()
    viernes_cierre = models.TimeField()
    sabado_apertura = models.TimeField()
    sabado_cierre = models.TimeField()
    domingo_apertura = models.TimeField()
    domingo_cierre = models.TimeField()
    usuario_por_dia = models.IntegerField()
    tiempo_por_usuario = models.IntegerField()
    class Meta:
        db_table = 'Sucursal'

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    cedula = models.CharField(max_length=100)
    tipo_usuario = models.CharField(max_length=100)
    id_cia = models.ForeignKey(Cias, on_delete=models.CASCADE)
    ind_es_afiliado = models.BooleanField(null=True)
    class Meta:
        db_table = 'PerfilUsuario'

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    id_tipo_empleado = models.IntegerField()
    especialidad = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    activo = models.BooleanField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_sucursal = models.IntegerField()
    class Meta:
        db_table = 'Empleado'

class Citas(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField()
    paciente_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas_paciente')
    medico_id = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='citas_medico')
    tipo_cita = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=100)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'Cita'

class Usuario_Afiliados(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_afiliado = models.IntegerField()
    class Meta:
        db_table = 'Usuario_Afiliados'