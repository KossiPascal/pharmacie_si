# Generated by Django 3.1.4 on 2021-01-29 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0003_auto_20210129_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='servedetats',
            name='type_data',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
