from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .serializers import UserSerializer, CitasSerializer, PerfilUsuarioSerializer, EmpleadoSerializer, SucursalSerializer, Usuario_AfiliadosSerializer, CitasSerializer, EmpleadoSerializer2
from .models import Citas, Cias, Empleado, Sucursal, Usuario_Afiliados, PerfilUsuario, User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='usuario'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='contraseña'),
        },
        required=['username', 'password']
    ),
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"error": "La ontraseña es incorrecta"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    serializer2 = PerfilUsuarioSerializer(instance=user.perfilusuario)

    return Response({"token": token.key, "user": serializer.data, "profile": serializer2.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_users(request):
    users = Citas.objects.all()
    serializer = CitasSerializer(users, many=True)
    return Response(serializer.data)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='usuario'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='contraseña'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='correo'),
            'id_cia': openapi.Schema(type=openapi.TYPE_INTEGER, description='id de la compañia'),
            'cedula': openapi.Schema(type=openapi.TYPE_STRING, description='Cedula'),
            'tipo_usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de usuario'),
            'ind_es_afiliado': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true, false'),
            'estado': openapi.Schema(type=openapi.TYPE_STRING, description='Activo, Inactivo'),
        },
        required=['username', 'password', 'email', 'id_cia', 'cedula', 'tipo_usuario', 'ind_es_afiliado', 'estado']
    ),
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        cia_instance = Cias.objects.get(id=request.data.get('id_cia'))

        profile_data = {
            'user': user.id,
            'cedula': request.data.get('cedula'),
            'tipo_usuario': request.data.get('tipo_usuario'),
            'id_cia': cia_instance.id,
        }
        profile_serializer = PerfilUsuarioSerializer(data=profile_data)

        if profile_serializer.is_valid():
            profile_serializer.save()
            
             # Comprueba si el usuario es un afiliado
            if request.data.get('ind_es_afiliado'):
                # Si el usuario es un afiliado, crea un nuevo Usuario_Afiliados
                afiliado = Usuario_Afiliados(
                    cedula=request.data.get('cedula'),
                    nombre=user.username,
                    email=user.email,
                    estado=request.data.get('estado'),
                    id_usuario=user,  # Asigna la instancia del usuario, no el ID
                    id_afiliado=user.id,  # Obtiene la instancia del usuario afiliado
                )
                afiliado.save()

            token = Token.objects.create(user=user)
            return Response({'token': token.key, "user": serializer.data, "profile": profile_serializer.data}, status=status.HTTP_201_CREATED)

        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="ID de la sucursal", type=openapi.TYPE_INTEGER)
    ],
    responses={200: SucursalSerializer(many=True), 404: 'Not Found'}
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la sucursal'),
            'direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de la sucursal'),
            'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono de la sucursal'),
        },
        required=['nombre', 'direccion', 'telefono']
    ),
    responses={201: SucursalSerializer(), 400: 'Bad Request'}
)
@swagger_auto_schema(
    method='delete',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la sucursal a eliminar (Solo usuarios Administrador)'),
        },
        required=['id']
    ),
    responses={204: 'No Content', 403: 'Forbidden', 404: 'Not Found'}
)
@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la sucursal a actualizar'),
            'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la sucursal'),
            'direccion': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección de la sucursal'),
            'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono de la sucursal'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email de la sucursal'),
            'lunes_apertura': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de apertura del lunes'),
            'lunes_cierre': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de cierre del lunes'),
            'martes_apertura': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de apertura del martes'),
            'martes_cierre': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de cierre del martes'),
            'miercoles_apertura': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de apertura del miércoles'),
            'miercoles_cierre': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de cierre del miércoles'),
            'jueves_apertura': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de apertura del jueves'),
            'jueves_cierre': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de cierre del jueves'),
            'viernes_apertura': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de apertura del viernes'),
            'viernes_cierre': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de cierre del viernes'),
            'sabado_apertura': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de apertura del sábado'),
            'sabado_cierre': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de cierre del sábado'),
            'domingo_apertura': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de apertura del domingo'),
            'domingo_cierre': openapi.Schema(type=openapi.TYPE_STRING, description='Hora de cierre del domingo'),
            'usuario_por_dia': openapi.Schema(type=openapi.TYPE_INTEGER, description='Usuarios por día'),
            'tiempo_por_usuario': openapi.Schema(type=openapi.TYPE_INTEGER, description='Tiempo por usuario'),
        },
        required=['id']
    ),
    responses={200: SucursalSerializer(), 400: 'Bad Request', 404: 'Not Found'}
)
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def branchOffices(request):
    if request.method == 'GET':
        sucursales = Sucursal.objects.all()
        serializer = SucursalSerializer(sucursales, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SucursalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            sucursal = Sucursal.objects.get(pk=request.data.get('id'))
        except Sucursal.DoesNotExist:
            return Response({'error': 'Sucursal no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        perfil = PerfilUsuario.objects.get(user=user)

        if perfil.tipo_usuario != 'Administrador':
            return Response({'error': 'No tienes permiso para actualizar esta sucursal.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = SucursalSerializer(sucursal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Sucursal actualizada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            sucursal = Sucursal.objects.get(pk=request.data.get('id'))
        except Sucursal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        perfil = PerfilUsuario.objects.get(user=user)

        if perfil.tipo_usuario == 'Administrador':
            sucursal.delete()
            return Response({'Sucursal eliminada correctamente. '}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'No tienes permiso para eliminar esta sucursal.'}, status=status.HTTP_403_FORBIDDEN)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='get',
        manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="ID del empleado", type=openapi.TYPE_INTEGER)
    ],
    responses={200: SucursalSerializer(many=True), 404: 'Not Found'}
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id_tipo_empleado': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del empleado'),
            'especialidad': openapi.Schema(type=openapi.TYPE_STRING, description='Apellido del empleado'),
            'cargo': openapi.Schema(type=openapi.TYPE_STRING, description='Cédula del empleado'),
            'activo': openapi.Schema(type=openapi.TYPE_STRING, description='Dirección del empleado'),
            'id_usuario': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono del empleado'),
            'id_sucursal': openapi.Schema(type=openapi.TYPE_STRING, description='Email del empleado'),
        },
        required=['id_tipo_empleado', 'especialidad', 'cargo', 'activo', 'id_usuario', 'id_sucursal']
    ),
    responses={201: EmpleadoSerializer(), 400: 'Bad Request'}
)
@swagger_auto_schema(
    method='delete',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del empleado a eliminar (solo pueden eliminar los usuarios Administrador)'),
        },
        required=['id']
    ),
    responses={204: 'No Content', 403: 'Forbidden', 404: 'Not Found'}
)
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Employes(request):
    if request.method == 'GET':
        empleados = Empleado.objects.all()
        serializer = EmpleadoSerializer2(empleados, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            empleado = Empleado.objects.get(pk=request.data.get('id'))
        except Empleado.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        perfil = PerfilUsuario.objects.get(user=user)

        if perfil.tipo_usuario == 'Administrador':
            empleado.delete()
            return Response({'Empleado eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'No tienes permiso para eliminar este empleado.'}, status=status.HTTP_403_FORBIDDEN)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='get',
        manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="ID del empleado", type=openapi.TYPE_INTEGER)
    ],
    responses={200: CitasSerializer(many=True), 404: 'Not Found'}
)
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'fecha_hora': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Fecha y hora de la cita'),
            'paciente_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id del usuario'),
            'medico_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del médico (empleado)'),
            'tipo_cita': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de cita (Medicina general...)'),
            'estado': openapi.Schema(type=openapi.TYPE_STRING, description='Estado (Aprobado...)'),
            'id_sucursal': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la sucursal'),
        },
        required=['fecha_hora', 'paciente_id', 'medico_id', 'tipo_cita', 'estado', 'id_sucursal']
    ),
    responses={201: 'Cita creada exitosamente', 400: 'Bad Request'}
)
@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la cita a cancelar'),
        },
        required=['id']
    ),
    responses={200: 'Cita cancelada correctamente', 403: 'Forbidden', 404: 'Not Found'}
)
@api_view(['GET', 'POST', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def NewCita(request):
    if request.method == 'GET':
        user_id = request.user.id
        citas = Citas.objects.filter(paciente_id=user_id)
        serializer = CitasSerializer(citas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CitasSerializer(data=request.data)
        if serializer.is_valid():
            cita = serializer.save()
            return Response("Su cita ha sido agendada exitosamente en la fecha {}".format(cita.fecha_hora), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        try:
            cita = Citas.objects.get(pk=request.data.get('id'))
        except Citas.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        perfil = PerfilUsuario.objects.get(user=user)

        if perfil.tipo_usuario in ['Administrador', 'Afiliado', 'Medico']:
            cita.estado = 'Cancelado'
            cita.save()
            return Response({'Cita cancelada correctamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No tienes permiso para cancelar esta cita.'}, status=status.HTTP_403_FORBIDDEN)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='get',
     manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="ID del usuario", type=openapi.TYPE_INTEGER)
    ],
    responses={200: PerfilUsuarioSerializer(many=True), 404: 'Not Found'}
)    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    profile = PerfilUsuario.objects.get(user=user)
    serializer = PerfilUsuarioSerializer(profile)
    return Response(serializer.data)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='get',
    responses={200: CitasSerializer(many=True)}
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UsuarioAfiliado(request):
    afiliados = Usuario_Afiliados.objects.all()
    serializer = Usuario_AfiliadosSerializer(afiliados, many=True)
    return Response(serializer.data)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='delete',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario a eliminar (solo pueden eliminar los usuarios Administrador)'),
        },
        required=['id']
    ),
    responses={
        204: openapi.Response(description='Usuario eliminado correctamente.'),
        403: openapi.Response(description='No tienes permiso para eliminar este usuario.'),
        404: openapi.Response(description='Usuario no encontrado.')
    }
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def DeleteUser(request):
    if request.method == 'DELETE':
        try:
            user_afiliado = User.objects.get(pk=request.data.get('id'))
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = request.user
        perfil = PerfilUsuario.objects.get(user=user)

        if perfil.tipo_usuario == 'Administrador':
            try:
                token = Token.objects.get(user=user_afiliado)
                token.delete()
            except Token.DoesNotExist:
                pass

            usuario_afiliado = Usuario_Afiliados.objects.get(id_usuario=user_afiliado)
            usuario_afiliado.delete()
            perfil_afiliado = PerfilUsuario.objects.get(user=user_afiliado)
            perfil_afiliado.delete()
            user_afiliado.delete()

            return Response({'Usuario eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'No tienes permiso para eliminar este usuario.'}, status=status.HTTP_403_FORBIDDEN)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='get',
    responses={200: CitasSerializer(many=True)}
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listar_citas(request):
    citas = Citas.objects.all().order_by('id')
    print('HERE')
    serializer = CitasSerializer(citas, many=True)
    return Response(serializer.data)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="ID del médico", type=openapi.TYPE_INTEGER)
    ],
    responses={200: CitasSerializer(many=True)}
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def citas_medico(request):
    medico = request.data.get('id')
    citas = Citas.objects.filter(medico_id=medico)
    serializer = CitasSerializer(citas, many=True)
    return Response(serializer.data)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la cita a finalizar'),
        },
        required=['id']
    ),
    responses={
        200: openapi.Response(description='Cita finalizada correctamente.'),
        404: openapi.Response(description='Cita no encontrada.')
    }
)
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def NextCita(request):
    try:
        cita = Citas.objects.get(id=request.data.get('id'))
    except Citas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    perfil = PerfilUsuario.objects.get(user=user)

    if perfil.tipo_usuario != 'Medico':
        return Response({'error': 'No tienes permiso para finalizar esta cita.'}, status=status.HTTP_403_FORBIDDEN)

    cita.estado = 'Finalizada'
    cita.save()
    return Response({'message': 'Cita finalizada correctamente.'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="ID de la sucursal", type=openapi.TYPE_INTEGER)
    ],
    responses={200: CitasSerializer(many=True), 404: 'Not Found'}
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def citas_sucursal(request):
    sucursal = request.data.get('id')
    citas = Citas.objects.filter(id_sucursal=sucursal) 
    serializer = CitasSerializer(citas, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, description="ID del usuario", type=openapi.TYPE_INTEGER)
    ],
    responses={200: CitasSerializer(many=True)}
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def citas_usuario(request):
    usuario = request.data.get('id')
    citas = Citas.objects.filter(paciente_id=usuario)
    serializer = CitasSerializer(citas, many=True)
    return Response(serializer.data)

#Linas @swagger_auto_schema son para la documentación de la API
@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(description='El usuario ha cerrado sesión correctamente.')
    }
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "El usuario ha cerrado sesión"}, status=status.HTTP_200_OK)
