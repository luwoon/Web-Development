# Generated by Django 4.2.11 on 2024-07-06 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_bid_comment_delete_bids_delete_comments_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="comment",
            field=models.CharField(default="", max_length=500),
        ),
        migrations.AlterField(
            model_name="listing",
            name="details",
            field=models.CharField(default="", max_length=1000),
        ),
    ]
