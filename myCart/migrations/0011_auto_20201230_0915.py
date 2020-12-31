# Generated by Django 3.1.4 on 2020-12-30 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myCart', '0010_auto_20201230_0746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='address',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='address_line_1',
            field=models.TextField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userdetails',
            name='address_line_2',
            field=models.TextField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]