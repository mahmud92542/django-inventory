# Generated by Django 3.1.2 on 2020-10-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmanagement', '0003_stockhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='issue_price',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]