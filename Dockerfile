# Usar una imagen base de Python 3
FROM python:3

# Establecer un directorio de trabajo
WORKDIR /usr/src/app

# Copiar los archivos de requisitos al directorio de trabajo
COPY requirements.txt ./

# Instalar los requisitos usando pip
RUN pip install --no-cache-dir -r requirements.txt

#environment variables
ENV DB_ENGINE django.db.backends.postgresql
ENV DB_NAME turnapp
ENV DB_USER userpruebas
ENV DB_PASSWORD UserDevelopmentSQL.2024*
ENV DB_HOST 34.42.21.228

# Copiar el resto de los archivos del proyecto al directorio de trabajo
COPY . .

# Exponer el puerto 8080
EXPOSE 8080

# Establecer la variable de entorno DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=server.settings

# Ejecutar el comando para iniciar el servidor Django en el puerto 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]