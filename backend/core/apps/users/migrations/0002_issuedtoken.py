# Generated by Django 3.2 on 2024-03-19 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssuedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('jti', models.CharField(max_length=255)),
                ('is_revoked', models.BooleanField(default=False)),
                ('expires_at', models.DateTimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issued_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Issued token',
                'verbose_name_plural': 'Issued tokens',
            },
        ),
    ]
