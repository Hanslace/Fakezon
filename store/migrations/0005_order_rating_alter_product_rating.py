# Generated by Django 5.0.6 on 2024-07-09 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_quanity_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='rating',
            field=models.IntegerField(choices=[(1, 'Poor'), (2, 'Bad'), (3, 'OK'), (4, 'Good'), (5, 'Amazing'), (0, 'Not Rated')], default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(choices=[(1, 'Poor'), (2, 'Bad'), (3, 'OK'), (4, 'Good'), (5, 'Amazing'), (0, 'Not Rated')], default=0),
        ),
    ]