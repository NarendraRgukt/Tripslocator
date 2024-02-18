# Generated by Django 4.2.4 on 2023-08-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_alter_trip_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='priority',
            field=models.CharField(choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high'), ('urgent', 'urgent')], max_length=15),
        ),
    ]