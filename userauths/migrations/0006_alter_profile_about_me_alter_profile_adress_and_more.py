# Generated by Django 5.0 on 2024-03-02 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0005_alter_profile_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="about_me",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="adress",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="city",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="counrty",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="instagram",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="state",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="whatsapp",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="working_at",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
    ]