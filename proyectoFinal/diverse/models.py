from distutils.command.upload import upload
from email.policy import default
from operator import mod
from django.db import models
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from account.models import *

# Create your models here.

def get_producto_imagenes_filepath(self, filename):
    return f'imagenes_producto/{self.sexo.tipo}/{self.categoria.nombre}/{self.subCategoria.nombre}/{self.marca.nombre}/{self.modelo.nombre}/{self.color.nombre}/'+str({self.num_ref})+'.png'

def get_more_product_images_filepath(self,filename):
    #return f'imagenes_producto/{self.producto.sexo.tipo}/{self.producto.categoria.nombre}/{self.producto.subCategoria.nombre}/{self.producto.marca.nombre}/{self.producto.modelo.nombre}/{self.producto.color.nombre}/extraimages/'
    return f'imagenes_producto/extraimages/{self.producto_numref_id}/' + filename

def get_default_imagen_producto():
    return f'imagenes_producto/imagen_producto_default.png'


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

    def __str__(self):
        return self.tipo

    class Meta:
        # managed = True
        db_table = 'diverse_sexo'

class categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre

    class Meta:
        # managed = True
        db_table = 'diverse_categoria'

class subCategoria(models.Model):

    id = models.AutoField(primary_key=True)

    categoria =  models.ForeignKey(
        'categoria', on_delete=models.CASCADE, related_name='categoria'
    )
    nombre = models.CharField(max_length=40, default='default categoria')

    def __str__(self):
        return self.nombre

    class Meta:
        # managed = True
        db_table = 'diverse_subcategoria'

class marca(models.Model):

    id = models.AutoField(primary_key=True)
#    subCategoria = models.ForeignKey(
#        'subCategoria', on_delete=models.CASCADE,
#    )
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

    class Meta:
        # managed = True
        db_table = 'diverse_marca'

class modelo(models.Model):

    id = models.AutoField(primary_key=True)
    marca = models.ForeignKey(
        'marca', on_delete=models.CASCADE,
    )
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

    class Meta:
        # managed = True
        db_table = 'diverse_modelo'

class color(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    hexcolor = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        # managed = True
        db_table = 'diverse_color'

class talla(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre

    class Meta:
        # managed = True
        db_table = 'diverse_talla'

class producto(models.Model):

    sexo =  models.ForeignKey(
        'sexo', on_delete=models.SET_NULL, null=True
    )
    categoria =  models.ForeignKey(
        'categoria', on_delete=models.SET_NULL, null=True
    )
    subCategoria =  models.ForeignKey(
        'subCategoria', on_delete=models.SET_NULL, null=True
    )
    marca =  models.ForeignKey(
        'marca', on_delete=models.SET_NULL, null=True
    )
    modelo =  models.ForeignKey(
        'modelo', on_delete=models.SET_NULL, null=True
    )
    color =  models.ForeignKey(
        'color', on_delete=models.SET_NULL, null=True
    )
    talla =  models.ForeignKey(
        'talla', on_delete=models.SET_NULL, null=True
    )
    num_ref = models.PositiveBigIntegerField(primary_key=True, null=False, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    imagen = models.ImageField(max_length=255, upload_to=get_producto_imagenes_filepath, null=True, blank=True, default=get_default_imagen_producto())

    def __str__(self):
        return str(self.num_ref)

    class Meta:
        # managed = True
        db_table = 'diverse_producto'

    def get_imagen_producto_filename(self):
        return str(self.imagen)[str(self.imagen).index(f'media/imagen/{self.sexo}/{self.categoria}/{self.subCategoria}/{self.marca}/{self.modelo}/{self.color}/'):]

class imagenProducto(models.Model):
    producto_numref = models.ForeignKey(producto , related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=get_more_product_images_filepath, blank=True, null=True)

    class Meta:
        # managed = True
        db_table = 'diverse_imagenproducto'

class stock(models.Model):
    
    id = models.AutoField(primary_key=True)
    num_ref_producto =  models.ForeignKey(
        'producto', on_delete=models.CASCADE,
    )
    cantidad = models.PositiveIntegerField()

class carrito(models.Model):

    OPCIONES_ESTADO = [
        (0, 'En proceso'),
        (1, 'Completo')
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
                settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
            )
    gastosEnvio = models.PositiveIntegerField(default=10)
    precio = models.PositiveIntegerField(default=0)
    precioTotal = models.PositiveIntegerField(default=0)
    estado = models.PositiveIntegerField(choices=OPCIONES_ESTADO, default=0)

class productoCarrito(models.Model):
    carrito = models.ForeignKey(
                'carrito', on_delete=models.CASCADE
            )
    producto = models.ForeignKey(
                'producto', on_delete=models.CASCADE
            )
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.PositiveIntegerField(default=0)
    precioTotal = models.PositiveIntegerField(default=0)

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