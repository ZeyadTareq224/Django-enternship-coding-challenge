# Generated by Django 3.1.5 on 2021-01-20 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0007_auto_20210120_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsubscribtion',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
