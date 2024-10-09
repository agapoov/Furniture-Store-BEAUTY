# Generated by Django 4.0 on 2024-10-04 10:39

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_emailverification_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 5, 10, 39, 10, 562136, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
