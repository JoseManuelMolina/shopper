# Generated by Django 3.2.9 on 2022-06-01 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverse', '0016_productocarrito_precio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productocarrito',
            old_name='totalPrecio',
            new_name='precioTotal',
        ),
    ]
