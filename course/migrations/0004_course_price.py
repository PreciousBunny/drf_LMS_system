# Generated by Django 4.2.5 on 2023-10-07 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(default=10000, verbose_name='Стоимость курса'),
        ),
    ]
