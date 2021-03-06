# Generated by Django 3.1.4 on 2021-02-02 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0009_auto_20210202_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variousparameters',
            name='big_total_amount',
        ),
        migrations.RemoveField(
            model_name='variousparameters',
            name='cameg_total_amount_served',
        ),
        migrations.RemoveField(
            model_name='variousparameters',
            name='cameg_total_amount_served_now',
        ),
        migrations.RemoveField(
            model_name='variousparameters',
            name='ih_total_amount_served',
        ),
        migrations.RemoveField(
            model_name='variousparameters',
            name='ih_total_amount_served_now',
        ),
        migrations.AddField(
            model_name='etats',
            name='amount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='etats',
            name='single_mount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='etats',
            name='total_mount',
            field=models.BooleanField(default=False),
        ),
    ]
