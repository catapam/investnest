# Generated by Django 5.1 on 2024-08-27 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "portfolio",
            "0005_alter_portfolio_color_alter_portfolio_description_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="asset",
            name="price",
        ),
        migrations.RemoveField(
            model_name="asset",
            name="purchased_at",
        ),
        migrations.RemoveField(
            model_name="asset",
            name="quantity",
        ),
        migrations.AddField(
            model_name="asset",
            name="live_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[("buy", "Buy"), ("sell", "Sell")], max_length=4
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("long", "Long"), ("short", "Short")], max_length=5
                    ),
                ),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="portfolio.asset",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
    ]
