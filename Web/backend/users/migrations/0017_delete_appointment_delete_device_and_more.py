# Generated by Django 5.0.4 on 2024-11-17 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0016_rename_symptom_appointment_diagnosis"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Appointment",
        ),
        migrations.DeleteModel(
            name="Device",
        ),
        migrations.DeleteModel(
            name="MaintainAndRepair",
        ),
        migrations.DeleteModel(
            name="Medicine",
        ),
        migrations.DeleteModel(
            name="Patient",
        ),
        migrations.DeleteModel(
            name="Schedule",
        ),
        migrations.DeleteModel(
            name="Staff",
        ),
    ]
