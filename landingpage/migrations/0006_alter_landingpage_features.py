# Generated by Django 4.2.5 on 2024-01-20 19:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landingpage", "0005_alter_landingpage_how_it_works_steps_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="landingpage",
            name="features",
            field=models.ManyToManyField(
                related_name="landingpage_features", to="landingpage.feature"
            ),
        ),
    ]
