# Generated by Django 3.2.9 on 2021-12-06 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0002_auto_20211206_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMENINO'), ('N', 'NINIOS')], max_length=1),
        ),
    ]
