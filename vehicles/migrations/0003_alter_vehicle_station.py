# Generated by Django 4.1.5 on 2023-01-17 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stations", "0001_initial"),
        ("vehicles", "0002_vehicle_station"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="station",
            field=models.OneToOneField(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stations.station",
            ),
        ),
    ]
