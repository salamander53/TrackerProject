# Generated by Django 5.0.4 on 2024-04-24 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_device_medicine_staff_patient_dayofbirth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='sympton',
            field=models.TextField(default='none', max_length=200),
        ),
    ]