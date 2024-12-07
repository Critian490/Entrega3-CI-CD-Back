from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Citas, PerfilUsuario, Empleado, Sucursal, Usuario_Afiliados

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password', 'first_name', 'last_name']

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['user', 'cedula', 'tipo_usuario', 'id_cia']

class CitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citas
        fields = ['id','fecha_hora','paciente_id','medico_id', 'tipo_cita','estado', 'id_sucursal']

class EmpleadoSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Empleado
        fields = ['id','id_tipo_empleado','especialidad','cargo','activo','id_usuario','id_sucursal']

class EmpleadoSerializer2(serializers.ModelSerializer):
    id_usuario = UserSerializer(read_only=True)

    class Meta:
        model = Empleado
        fields = ['id','id_tipo_empleado','especialidad','cargo','activo','id_usuario','id_sucursal', 'id_usuario']

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id','id_cia','nombre','direccion','telefono','email','lunes_apertura','lunes_cierre','martes_apertura',
                  'martes_cierre','miercoles_apertura','miercoles_cierre','jueves_apertura','jueves_cierre','viernes_apertura',
                  'viernes_cierre','sabado_apertura','sabado_cierre','domingo_apertura','domingo_cierre','usuario_por_dia','tiempo_por_usuario']   

class Usuario_AfiliadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario_Afiliados
        fields = ['id','cedula','nombre','id_usuario', 'id_afiliado','email','estado']

class CitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citas
        fields = '__all__'