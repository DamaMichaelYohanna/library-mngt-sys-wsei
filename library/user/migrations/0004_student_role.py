# Generated by Django 5.1.4 on 2024-12-11 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_librarian_deleted_student_deleted"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="role",
            field=models.CharField(default="Student", max_length=7),
        ),
    ]
