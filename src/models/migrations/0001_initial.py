# Generated by Django 4.1.5 on 2023-01-25 14:01

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vacancy",
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
                ("company_name", models.CharField(max_length=128)),
                ("name", models.CharField(max_length=127)),
                ("experience", models.CharField(max_length=63)),
                ("city", models.CharField(max_length=63)),
                ("alternate_url", models.CharField(max_length=63)),
                ("schedule", models.CharField(max_length=63)),
                ("contact_email", models.EmailField(max_length=254, null=True)),
                (
                    "contacts_phones",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, null=True, region=None
                    ),
                ),
                ("is_request", models.BooleanField(default=False)),
            ],
        ),
    ]
