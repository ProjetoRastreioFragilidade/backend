# Generated by Django 2.0.2 on 2018-02-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppsus_app', '0005_auto_20180220_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edmonton',
            name='data_inicio',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='subjetiva',
            name='data_inicio',
            field=models.DateTimeField(),
        ),
    ]
