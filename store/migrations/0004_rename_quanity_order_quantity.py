# Generated by Django 5.0.6 on 2024-07-09 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='quanity',
            new_name='quantity',
        ),
    ]
