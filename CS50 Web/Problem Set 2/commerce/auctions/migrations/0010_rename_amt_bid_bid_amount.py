# Generated by Django 4.2.11 on 2024-07-07 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0009_alter_bid_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bid",
            old_name="amt",
            new_name="bid_amount",
        ),
    ]
