# Generated by Django 5.0.4 on 2024-05-04 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_patient_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='symptom',
        ),
        migrations.AddField(
            model_name='appointment',
            name='symptom',
            field=models.TextField(default='none', max_length=200),
        ),
    ]