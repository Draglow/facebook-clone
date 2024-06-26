# Generated by Django 5.0 on 2023-12-27 17:55

import django.db.models.deletion
import shortuuid.django_fields
import userauths.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "pid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefghijklmnopqrstuvwxyz",
                        length=7,
                        max_length=25,
                        prefix="",
                    ),
                ),
                (
                    "cover_image",
                    models.ImageField(
                        default="cover.jpg",
                        upload_to=userauths.models.user_directory_path,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="default.jpg",
                        upload_to=userauths.models.user_directory_path,
                    ),
                ),
                ("full_name", models.CharField(blank=True, max_length=100, null=True)),
                ("phone", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "male"), ("female", "female")],
                        default="male",
                        max_length=100,
                    ),
                ),
                (
                    "relationship",
                    models.CharField(
                        choices=[("Single", "Single"), ("Married", "Marrid")],
                        default="single",
                        max_length=100,
                    ),
                ),
                ("bio", models.CharField(blank=True, max_length=200, null=True)),
                ("about_me", models.TextField(blank=True, null=True)),
                ("counrty", models.CharField(blank=True, max_length=200, null=True)),
                ("state", models.CharField(blank=True, max_length=200, null=True)),
                ("city", models.CharField(blank=True, max_length=200, null=True)),
                ("adress", models.CharField(blank=True, max_length=200, null=True)),
                ("working_at", models.CharField(blank=True, max_length=200, null=True)),
                ("instagram", models.CharField(blank=True, max_length=200, null=True)),
                ("whatsapp", models.CharField(blank=True, max_length=200, null=True)),
                ("varified", models.BooleanField(default=False)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "blocked",
                    models.ManyToManyField(
                        blank=True, related_name="blocked", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "followers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "following",
                    models.ManyToManyField(
                        blank=True,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "friends",
                    models.ManyToManyField(
                        blank=True, related_name="friends", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
