# Generated by Django 5.1 on 2024-09-22 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0004_remove_asset_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="name",
            field=models.CharField(max_length=8),
        ),
    ]
