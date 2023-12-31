# Generated by Django 4.2.3 on 2023-07-22 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoProject', '0005_remove_property_hosted_sice_property_hosted_since'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevokedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, unique=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('revoked_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
