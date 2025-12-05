from django.db import models
from django.contrib.auth.models import AbstractUser

# apps/auth_app/models.py (AL INICIO DEL ARCHIVO, después de los imports)
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, fechanacimiento=None, **extra_fields): 
        if not email:
            raise ValueError('El email debe ser configurado')
        if not fechanacimiento: 
            raise ValueError('La fecha de nacimiento es obligatoria.')

        email = self.normalize_email(email)
        user = self.model(email=email, fechanacimiento=fechanacimiento, **extra_fields) 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, fechanacimiento=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if 'username' in extra_fields:
            extra_fields.pop('username')
        
        return self.create_user(email, password, fechanacimiento, **extra_fields)



class Genero(models.Model):
    genero_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=30)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'genero'

class Ubicacion(models.Model):
    ubicacion_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'ubicacion'


class Programa(models.Model):
    programa_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=60)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'programa'

class Usuario(AbstractUser):
    usuario_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    genero = models.ForeignKey(Genero, models.DO_NOTHING, blank=True, null=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    fechanacimiento = models.DateField(blank=True)
    email = models.CharField(unique=True, max_length=60)
    contrasena = models.CharField(max_length=255)
    numerotelefono = models.CharField(blank=True,max_length=15)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    fecharegistro = models.DateTimeField(blank=True, null=True)
    estadocuenta = models.CharField(max_length=1, blank=True, null=True)
    tyc = models.BooleanField(blank=True, null=True)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    class Meta:
        db_table = 'usuario'

    @property
    def first_name(self):
        return self.nombres

    @first_name.setter
    def first_name(self, value):
        self.nombres = value

    @property
    def last_name(self):
        return self.apellidos

    @last_name.setter
    def last_name(self, value):
        self.apellidos = value

    @property
    def password(self):
        return self.contrasena

    @password.setter
    def password(self, value):
        self.contrasena = value

    @property
    def id(self):
        return self.usuario_id

    def get_full_name(self):
        return f"{self.nombres} {self.apellidos}"

    def get_short_name(self):
        return self.nombres



