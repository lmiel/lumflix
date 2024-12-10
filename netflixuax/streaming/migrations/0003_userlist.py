# Generated by Django 5.1.1 on 2024-12-05 11:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("streaming", "0002_playlist_recommendation"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserList",
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
                (
                    "movies",
                    models.ManyToManyField(
                        blank=True, related_name="in_user_lists", to="streaming.movie"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_list",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
