# Generated by Django 4.2.7 on 2023-12-13 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_rename_usernumbers_usernumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]