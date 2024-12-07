
from django.contrib import admin
from django.urls import path, re_path, include
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="TurnApp Docs",
      default_version='v1',
      description="Documentacion de las peticiones y endpoints disponibles en la API de TurnApp",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('citasn', views.list_users),
    re_path('sucursales', views.branchOffices),
    re_path('citas', views.NewCita),
    re_path('empleados', views.Employes),
    re_path('perfil', views.profile),
    re_path('afiliados', views.UsuarioAfiliado),
    re_path('logout', views.logout),
    re_path('usuarios', views.DeleteUser),
    re_path('citas_medico', views.citas_medico),
    re_path('siguiente_cita', views.NextCita),
    re_path('listar_citas', views.listar_citas),
   re_path('citas_usuario', views.citas_usuario),
    re_path('citas_sucursal', views.citas_sucursal),
    path('TurnAppApiDocs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('TurnAppRedoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
