# Generated by Django 3.0.9 on 2020-10-21 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_message1_read_by_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message1',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]