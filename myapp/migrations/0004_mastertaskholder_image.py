# Generated by Django 4.1.2 on 2022-10-23 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_remove_mastertaskholder_applink_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mastertaskholder",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="imageproof/"),
        ),
    ]