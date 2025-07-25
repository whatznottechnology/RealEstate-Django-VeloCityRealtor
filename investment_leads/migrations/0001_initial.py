# Generated by Django 5.0.2 on 2025-07-07 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_number', models.CharField(max_length=20)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('budget', models.CharField(max_length=100)),
                ('requirement_type', models.CharField(choices=[('buy', 'Buy'), ('sale', 'Sale'), ('want_lease', 'Want Lease'), ('for_lease', 'For Lease')], max_length=20)),
                ('property_type', models.CharField(choices=[('hotel', 'Hotel'), ('restaurant', 'Restaurant'), ('bar', 'Bar'), ('banquet', 'Banquet'), ('petrol_pump', 'Petrol Pump'), ('land', 'Land'), ('showroom', 'Showroom')], max_length=20)),
                ('enquiry_from', models.CharField(choices=[('agent', 'Agent'), ('owner', 'Owner'), ('individual', 'Individual')], max_length=20)),
                ('property_details', models.TextField(blank=True, null=True)),
                ('agreed_to_terms', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Investment Requirement',
                'verbose_name_plural': 'Investment Requirements',
                'ordering': ['-created_at'],
            },
        ),
    ]
