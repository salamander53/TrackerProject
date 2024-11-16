# Generated by Django 5.0.4 on 2024-11-16 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Torrent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('announce', models.URLField()),
                ('file_length', models.BigIntegerField()),
                ('piece_length', models.IntegerField()),
                ('pieces', models.TextField()),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
