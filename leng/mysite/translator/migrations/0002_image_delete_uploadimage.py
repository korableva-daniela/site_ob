# Generated by Django 5.1.1 on 2024-09-21 19:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("translator", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("title", models.CharField(max_length=200)),
                ("image", models.ImageField(blank=True, upload_to="users/%Y/%m/%d/")),
            ],
        ),
        migrations.DeleteModel(
            name="UploadImage",
        ),
    ]