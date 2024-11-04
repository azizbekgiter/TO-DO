# Generated by Django 5.1.2 on 2024-10-26 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_alter_user_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_name",
            field=models.CharField(
                blank=True, default="default_user", max_length=255, unique=True
            ),
        ),
    ]