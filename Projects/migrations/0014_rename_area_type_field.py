# Add temporary field to store old area_type values
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0013_populate_area_types'),
    ]

    operations = [
        # Rename the old area_type field to area_type_old temporarily
        migrations.RenameField(
            model_name='nearestarea',
            old_name='area_type',
            new_name='area_type_old',
        ),
        
        # Add new ForeignKey field for AreaType
        migrations.AddField(
            model_name='nearestarea',
            name='area_type',
            field=models.ForeignKey(
                help_text='Select area type',
                null=True,
                blank=True,
                on_delete=models.deletion.CASCADE,
                related_name='nearest_areas',
                to='Projects.areatype'
            ),
        ),
    ]
