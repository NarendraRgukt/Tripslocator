# Generated by Django 4.2.4 on 2023-08-15 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0006_alter_member_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='roles.organization', unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, to='roles.role'),
            preserve_default=False,
        ),
    ]