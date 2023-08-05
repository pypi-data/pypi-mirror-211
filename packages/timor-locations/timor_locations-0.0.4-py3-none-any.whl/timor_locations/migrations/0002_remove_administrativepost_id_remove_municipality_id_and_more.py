# Generated by Django 4.2.1 on 2023-05-24 13:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("timor_locations", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="administrativepost",
            name="id",
        ),
        migrations.RemoveField(
            model_name="municipality",
            name="id",
        ),
        migrations.RemoveField(
            model_name="suco",
            name="id",
        ),
        migrations.AlterField(
            model_name="administrativepost",
            name="pcode",
            field=models.IntegerField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="municipality",
            name="pcode",
            field=models.IntegerField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="suco",
            name="pcode",
            field=models.IntegerField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
