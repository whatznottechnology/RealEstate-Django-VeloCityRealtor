# Generated migration with data migration for AreaType
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0011_remove_projectreview_reviewer_email_and_more'),
    ]

    operations = [
        # Create AreaType model
        migrations.CreateModel(
            name='AreaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. School, Hospital, Metro Station', max_length=100, unique=True)),
                ('icon', models.ImageField(blank=True, help_text='Area type icon', null=True, upload_to='area_types/icons/')),
                ('font_awesome_icon', models.CharField(blank=True, help_text='Font Awesome icon class (e.g., fas fa-school)', max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Area Type',
                'verbose_name_plural': 'Area Types',
                'ordering': ['order', 'name'],
            },
        ),
        
        # Update Project status field
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[
                ('ready_to_move', 'Ready to Move'), 
                ('under_construction', 'Under Construction'), 
                ('upcoming_project', 'Upcoming Project'), 
                ('possession_soon', 'Possession Soon'), 
                ('sold_out', 'Sold Out'), 
                ('new_launched', 'New Launched')
            ], default='under_construction', max_length=20, null=True),
        ),
        
        # Update NearestArea icon help text
        migrations.AlterField(
            model_name='nearestarea',
            name='icon',
            field=models.ImageField(blank=True, help_text='Location type icon (optional, overrides area type icon)', null=True, upload_to='locations/icons/'),
        ),
    ]
