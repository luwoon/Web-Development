# Generated by Django 4.2.11 on 2024-07-14 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0014_listing_winning_bid_listing_winning_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]