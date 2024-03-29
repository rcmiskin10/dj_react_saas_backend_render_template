# Generated by Django 4.2.5 on 2024-01-20 19:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landingpage", "0003_alter_newslettersignup_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialMediaLink",
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
                ("social_media_type", models.CharField(max_length=256)),
                ("social_media_mui_icon_name", models.CharField(max_length=256)),
                ("social_media_link", models.CharField(max_length=256)),
                ("order", models.PositiveIntegerField()),
            ],
        ),
        migrations.RenameModel(
            old_name="Features",
            new_name="Feature",
        ),
        migrations.RenameModel(
            old_name="HowItWorks",
            new_name="HowItWorksStep",
        ),
        migrations.RemoveField(
            model_name="landingpage",
            name="how_it_works",
        ),
        migrations.AddField(
            model_name="landingpage",
            name="how_it_works_steps",
            field=models.ManyToManyField(
                related_name="landingepage_how_it_works_steps",
                to="landingpage.howitworksstep",
            ),
        ),
        migrations.AddField(
            model_name="landingpage",
            name="social_media_links",
            field=models.ManyToManyField(
                related_name="landingepage_social_media_links",
                to="landingpage.socialmedialink",
            ),
        ),
    ]
