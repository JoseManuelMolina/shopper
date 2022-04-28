from email.policy import default
from operator import mod
from django.db import models
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class sexo(models.Model):

    HOMBRE = 'H'
    MUJER = 'M'
    NIÑO = 'NO'
    NIÑA = 'NA'

    OPCIONES_SEXO = [
        (HOMBRE, 'Hombre'),
        (MUJER, 'Mujer'),
        (NIÑO, 'Niño'),
        (NIÑA, 'Niña'),
    ]

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=2, choices=OPCIONES_SEXO)

class categoria(models.Model):
    id = models.AutoField(primary_key=True)
 #   sexo = models.ForeignKey(
 #       'sexo', on_delete=models.CASCADE,
 #   )
    nombre = models.CharField(max_length=40)

class subCategoria(models.Model):

    id = models.AutoField(primary_key=True)

    categoria =  models.ForeignKey(
        'categoria', on_delete=models.CASCADE, related_name='categoria'
    )
    nombre = models.CharField(max_length=40, default='default categoria')

class marca(models.Model):

    id = models.AutoField(primary_key=True)
#    subCategoria = models.ForeignKey(
#        'subCategoria', on_delete=models.CASCADE,
#    )
    nombre = models.CharField(max_length=60)

class modelo(models.Model):

    id = models.AutoField(primary_key=True)
    marca = models.ForeignKey(
        'marca', on_delete=models.CASCADE,
    )
    nombre = models.CharField(max_length=60)

class color(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)

class talla(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)

class producto(models.Model):

    sexo =  models.ForeignKey(
        'sexo', on_delete=models.CASCADE,
    )
    categoria =  models.ForeignKey(
        'categoria', on_delete=models.CASCADE,
    )
    subCategoria =  models.ForeignKey(
        'subCategoria', on_delete=models.CASCADE,
    )
    marca =  models.ForeignKey(
        'marca', on_delete=models.CASCADE,
    )
    modelo =  models.ForeignKey(
        'modelo', on_delete=models.CASCADE,
    )
    color =  models.ForeignKey(
        'color', on_delete=models.CASCADE,
    )
    talla =  models.ForeignKey(
        'talla', on_delete=models.CASCADE,
    )
    num_ref = models.PositiveBigIntegerField(primary_key=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    imagen = models.ImageField(upload_to = 'media/productos', blank=True, null=True)

class stock(models.Model):
    
    id = models.AutoField(primary_key=True)
    num_ref_producto =  models.ForeignKey(
        'producto', on_delete=models.CASCADE,
    )
    cantidad = models.PositiveIntegerField()

class pedido(models.Model):
    
    PENDIENTE = 'PEND'
    PAGADO = 'PAGD'
    ENVIADO = 'ENVI'
    RECIBIDO = 'RECB'
    CANCELADO = 'CANC'
    DEVUELTO = 'DELV'

    OPCIONES_ESTADO = [
        (PENDIENTE, 'Pendiente'),
        (PAGADO, 'Pagado'),
        (ENVIADO, 'Enviado'),
        (RECIBIDO, 'Recibido'),
        (CANCELADO, 'Cancelado'),
        (DEVUELTO, 'Devuelto'),
    ]

    id = models.AutoField(primary_key=True)
    id_cliente =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    estado = models.CharField(max_length=4, choices=OPCIONES_ESTADO, default=PENDIENTE)
    fecha = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

class productos_pedido(models.Model):
    
    id_pedido = models.ForeignKey(
        'pedido', on_delete=models.CASCADE,
    )
    num_ref_producto = models.ForeignKey(
        'producto', on_delete=models.CASCADE,
    )
    cantidad = models.PositiveIntegerField(validators=[MaxValueValidator(999)])
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    descuento = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])