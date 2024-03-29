# Generated by Django 4.2.5 on 2024-01-20 19:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landingpage", "0004_socialmedialink_rename_features_feature_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="landingpage",
            name="how_it_works_steps",
            field=models.ManyToManyField(
                related_name="landingpage_how_it_works_steps",
                to="landingpage.howitworksstep",
            ),
        ),
        migrations.AlterField(
            model_name="landingpage",
            name="social_media_links",
            field=models.ManyToManyField(
                related_name="landingpage_social_media_links",
                to="landingpage.socialmedialink",
            ),
        ),
    ]
