# Generated by Django 4.2.11 on 2024-06-05 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='products.product'),
            preserve_default=False,
        ),
    ]
