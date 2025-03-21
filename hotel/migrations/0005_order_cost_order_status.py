# Generated by Django 5.1.3 on 2024-12-06 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Packing', 'Packing'), ('In-transit', 'Intransit'), ('Deliveres', 'Delivered')], default='Packing', max_length=50),
        ),
    ]
