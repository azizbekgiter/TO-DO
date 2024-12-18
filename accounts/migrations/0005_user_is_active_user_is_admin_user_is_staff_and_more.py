# Generated by Django 5.1.2 on 2024-10-24 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_remove_user_is_active_remove_user_is_admin_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
