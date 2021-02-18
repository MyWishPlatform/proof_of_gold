# Generated by Django 3.1.6 on 2021-02-17 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge_id', models.IntegerField(unique=True)),
                ('status', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=10)),
                ('amount', models.IntegerField()),
                ('hash', models.CharField(max_length=100)),
                ('redirect_url', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='QuantumAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.IntegerField()),
                ('address', models.CharField(max_length=50)),
                ('access_token', models.TextField(null=True)),
                ('token_type', models.CharField(max_length=20, null=True)),
                ('token_expires_at', models.BigIntegerField(null=True)),
            ],
        ),
    ]
