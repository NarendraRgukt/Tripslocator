# Generated by Django 4.2.4 on 2023-08-10 09:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0004_alter_member_organization_alter_member_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
