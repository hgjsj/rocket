# Generated by Django 3.0.3 on 2020-02-25 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_estate_api', '0003_auto_20200224_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='execution_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
