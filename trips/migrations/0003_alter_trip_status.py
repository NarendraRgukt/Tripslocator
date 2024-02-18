# Generated by Django 4.2.4 on 2023-08-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_alter_trip_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=models.CharField(choices=[('created', 'created'), ('started', 'started'), ('ended', 'ended')], default='created', max_length=15),
        ),
    ]
