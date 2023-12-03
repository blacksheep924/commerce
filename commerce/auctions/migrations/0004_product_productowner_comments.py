# Generated by Django 4.2.7 on 2023-12-01 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid_bidder_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productOwner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentcontent', models.CharField(max_length=1000)),
                ('commentator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commentid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]