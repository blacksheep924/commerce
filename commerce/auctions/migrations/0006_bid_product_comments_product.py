# Generated by Django 4.2.7 on 2023-12-01 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_product_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.product'),
        ),
        migrations.AddField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.product'),
        ),
    ]