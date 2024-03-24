# Generated by Django 3.2 on 2024-03-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1000.0, max_digits=14, verbose_name='Amount'),
            preserve_default=False,
        ),
    ]