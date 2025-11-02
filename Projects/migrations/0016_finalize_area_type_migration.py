# Remove old area_type_old field and finalize
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0015_migrate_area_type_data'),
    ]

    operations = [
        # Make area_type required (remove null=True, blank=True)
        migrations.AlterField(
            model_name='nearestarea',
            name='area_type',
            field=models.ForeignKey(
                help_text='Select area type',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='nearest_areas',
                to='Projects.areatype'
            ),
        ),
        
        # Remove the old CharField
        migrations.RemoveField(
            model_name='nearestarea',
            name='area_type_old',
        ),
        
        # Update NearestArea Meta options
        migrations.AlterModelOptions(
            name='nearestarea',
            options={
                'ordering': ['area_type__order', 'name'],
                'verbose_name': 'Nearest Area',
                'verbose_name_plural': 'Nearest Areas'
            },
        ),
    ]
