# Generated by Django 3.1.6 on 2021-02-04 13:58

from django.db import migrations, models
import django.db.models.deletion
import remusgold.store.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('images', models.ImageField(blank=True, upload_to=remusgold.store.utilities.get_timestamp_path)),
                ('total_supply', models.IntegerField()),
                ('ducatus_bonus', models.IntegerField()),
                ('lucky_prize', models.IntegerField()),
                ('supply', models.IntegerField()),
                ('sold', models.IntegerField()),
                ('price', models.FloatField()),
                ('description', models.CharField(max_length=1000)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.group')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('body', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.item')),
            ],
        ),
    ]
