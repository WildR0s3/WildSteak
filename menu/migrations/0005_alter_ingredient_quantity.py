# Generated by Django 4.0.6 on 2022-08-06 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_ingredient_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.FloatField(null=True),
        ),
    ]
