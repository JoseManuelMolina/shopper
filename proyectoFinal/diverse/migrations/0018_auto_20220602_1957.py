# Generated by Django 3.2.9 on 2022-06-02 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diverse', '0017_rename_totalprecio_productocarrito_preciototal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrito',
            name='cantidad',
        ),
        migrations.AddField(
            model_name='carrito',
            name='estado',
            field=models.PositiveIntegerField(choices=[(0, 'Proceso'), (1, 'Completo')], default=0, max_length=1),
        ),
    ]
