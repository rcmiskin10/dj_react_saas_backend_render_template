# Generated by Django 4.2.5 on 2024-01-19 23:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landingpage", "0002_newslettersignup"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newslettersignup",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
