from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

import datetime

# Crear nuevo usuario.

# Crear nuevo superusuario

class ControladorUsuarios(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("El usuario debe de tener un email.")
        if not username:
            raise ValueError("El usuario debe de tener un nombre de usuario.")
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superusuario = True
        user.save(using=self._db)
        return user

# User modelo

def get_imagen_perfil_filepath(self, filename):
    return f'{self.pk} - {self.username}/{"imagen_perfil.png"}'

def get_default_imagen_perfil():
    return f'imagen_perfil_default.png'

class Account(AbstractBaseUser):

    GENERO_HOMBRE = 0
    GENERO_MUJER = 1
    GENERO_OPCIONES = [(GENERO_HOMBRE, 'Hombre'), (GENERO_MUJER, 'Mujer')]

    id                  = models.AutoField(primary_key=True)
    email               = models.EmailField(verbose_name="email", max_length=100, unique=True)
    username            = models.CharField(max_length=50, unique=True)
    telefono            = models.PositiveIntegerField(null=True, blank=True)
    nombre              = models.CharField(max_length=20, null=True, blank=True)
    apellidos           = models.CharField(max_length=60, null=True, blank=True)
    fechaNacimiento     = models.DateField(null=False, blank=False, default=datetime.date.today)
    genero              = models.IntegerField(choices=GENERO_OPCIONES, null=False, blank=False, default=0)
    fecha_union         = models.DateTimeField(verbose_name="fecha union", auto_now_add=True)
    ultima_conexion     = models.DateTimeField(verbose_name="ultima conexion", auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_usuario          = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superusuario     = models.BooleanField(default=False)
    imagen_perfil       = models.ImageField(max_length=255, upload_to=get_imagen_perfil_filepath, null=True, blank=True, default=get_default_imagen_perfil())
    hide_email          = models.BooleanField(default=False)

    objects = ControladorUsuarios()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_imagen_perfil_filename(self):
        return str(self.imagen_perfil)[str(self.imagen_perfil).index(f'media/imagenes_perfil/{self.pk} - {self.username}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class direccion(models.Model):

    id                  = models.AutoField(primary_key=True)
    usuario             = models.ForeignKey(
                            'Account', on_delete=models.CASCADE
                        )
    nombre              = models.CharField(max_length=20)
    apellidos           = models.CharField(max_length=60)
    direccion           = models.CharField(max_length=100)
    direccion2          = models.CharField(max_length=50, null=True, blank=True)
    pais                = models.CharField(max_length=60)
    provincia           = models.CharField(max_length=60)
    localidad           = models.CharField(max_length=60)
    codigoPostal        = models.PositiveIntegerField()
    direccion_pref      = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['id', 'usuario', 'nombre', 'apellidos', 'direccion', 'pais', 'provincia', 'localidad', 'codigoPostal']

    def __str__(self):
        return self.id

class metodosPago(models.Model):

    id                  = models.AutoField(primary_key=True)
    usuario             = models.ForeignKey(
                            'Account', on_delete=models.CASCADE
                        )
    metodo_pref         = models.BooleanField(default=False)

    def __str__(self):
        return self.id
