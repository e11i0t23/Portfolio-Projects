# Generated by Django 4.1.7 on 2023-03-06 17:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_2_commerce', '0002_alter_auction_enddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='endDate',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 13, 17, 24, 28, 595400, tzinfo=datetime.timezone.utc)),
        ),
    ]