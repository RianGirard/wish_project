# Generated by Django 2.2 on 2021-06-22 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='granted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
