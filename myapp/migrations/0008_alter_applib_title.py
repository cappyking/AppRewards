# Generated by Django 4.1.2 on 2022-10-31 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0007_alter_applib_applink"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applib",
            name="title",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
