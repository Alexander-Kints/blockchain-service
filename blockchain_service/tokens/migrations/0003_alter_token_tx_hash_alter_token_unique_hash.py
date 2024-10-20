# Generated by Django 5.1.2 on 2024-10-20 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0002_alter_token_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='tx_hash',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='token',
            name='unique_hash',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
