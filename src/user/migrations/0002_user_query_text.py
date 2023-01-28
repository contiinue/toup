# Generated by Django 4.1.5 on 2023-01-27 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="query_text",
            field=models.CharField(
                default="( Django OR FastAPI OR DRF OR python backend )", max_length=63
            ),
            preserve_default=False,
        ),
    ]
