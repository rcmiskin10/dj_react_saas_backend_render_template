# Generated by Django 4.2.5 on 2024-01-06 20:35

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="body",
            field=django_quill.fields.QuillField(),
        ),
    ]
