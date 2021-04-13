# Generated by Django 3.1 on 2021-04-12 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=100)),
                ('plural', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=5)),
                ('symbol_native', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='IPLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, default=None, null=True, verbose_name='URL address')),
                ('ip', models.GenericIPAddressField(verbose_name='IP address')),
                ('type', models.CharField(choices=[('ipv4', 'Ip V4'), ('ipv6', 'Ip V6')], default='ipv4', max_length=4, verbose_name='IP type: ipv4 or ipv6')),
                ('latitude', models.DecimalField(blank=True, decimal_places=13, default=None, max_digits=15, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=13, default=None, max_digits=15, null=True)),
                ('currency', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.currency')),
            ],
        ),
    ]
