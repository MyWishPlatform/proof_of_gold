from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20210209_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fixed_btc_rate',
            field=models.DecimalField(decimal_places=8, null=True, max_digits=78),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='fixed_eth_rate',
            field=models.DecimalField(decimal_places=8, null=True, max_digits=78),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='fixed_usdc_rate',
            field=models.DecimalField(decimal_places=8, null=True, max_digits=78),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='time_to_live',
            field=models.IntegerField(default=10800),
        ),
        migrations.AlterField(
            model_name='order',
            name='received_usd_amount',
            field=models.DecimalField(decimal_places=2, null=True, max_digits=78),
        ),
        migrations.AlterField(
            model_name='order',
            name='required_usd_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=78, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.order'),
            preserve_default=False,
        ),
    ]
