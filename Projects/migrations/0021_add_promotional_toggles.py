# Generated migration for new promotional toggles

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0020_alter_project_slug'),
    ]

    operations = [
        # Add new promotional toggle fields
        migrations.AddField(
            model_name='project',
            name='promo_hot_deals',
            field=models.BooleanField(default=False, help_text='Show in Hot Deals section', verbose_name='Hot Deals'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_premium_projects',
            field=models.BooleanField(default=False, help_text='Show in Premium Projects section', verbose_name='Premium Projects'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_residential_projects',
            field=models.BooleanField(default=False, help_text='Show in Residential Projects section', verbose_name='Residential Projects'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_commercial_projects',
            field=models.BooleanField(default=False, help_text='Show in Commercial Projects section', verbose_name='Commercial Projects'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_trending_projects',
            field=models.BooleanField(default=False, help_text='Show in Trending Projects section', verbose_name='Trending Projects'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_most_viewed',
            field=models.BooleanField(default=False, help_text='Show in Most Viewed section', verbose_name='Most Viewed'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_recently_viewed',
            field=models.BooleanField(default=False, help_text='Show in Recently Viewed section', verbose_name='Recently Viewed'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_for_sale',
            field=models.BooleanField(default=False, help_text='Show in Properties for Sale section', verbose_name='Properties for Sale'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_for_rent',
            field=models.BooleanField(default=False, help_text='Show in Properties for Rent section', verbose_name='Properties for Rent'),
        ),
        migrations.AddField(
            model_name='project',
            name='promo_for_lease',
            field=models.BooleanField(default=False, help_text='Show in Properties for Lease section', verbose_name='Properties for Lease'),
        ),
        
        # Add index for better query performance on promotional toggles
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['promo_hot_deals', 'is_active'], name='idx_hot_deals_active'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['promo_premium_projects', 'is_active'], name='idx_premium_active'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['promo_trending_projects', 'is_active'], name='idx_trending_active'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['promo_most_viewed', 'is_active'], name='idx_mostviewed_active'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['promo_for_sale', 'is_active'], name='idx_forsale_active'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['promo_for_rent', 'is_active'], name='idx_forrent_active'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['promo_for_lease', 'is_active'], name='idx_forlease_active'),
        ),
    ]
