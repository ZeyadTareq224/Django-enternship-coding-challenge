# Generated by Django 3.1.5 on 2021-01-20 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20210120_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventsubscription',
            name='events',
        ),
        migrations.AddField(
            model_name='event',
            name='cover_img',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventsubscription',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.event'),
            preserve_default=False,
        ),
    ]
