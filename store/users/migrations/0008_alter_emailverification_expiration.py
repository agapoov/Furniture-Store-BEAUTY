# Generated by Django 4.0 on 2024-10-04 12:10

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_emailverification_expiration_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 5, 12, 10, 12, 376249, tzinfo=utc)),
        ),
    ]
