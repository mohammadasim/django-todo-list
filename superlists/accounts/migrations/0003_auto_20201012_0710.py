# Generated by Django 3.1 on 2020-10-12 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201012_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='uid',
            field=models.CharField(max_length=10),
        ),
    ]
