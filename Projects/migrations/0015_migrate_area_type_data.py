# Migrate data from old CharField to new ForeignKey
from django.db import migrations
import django.db.models.deletion


def migrate_area_type_data(apps, schema_editor):
    AreaType = apps.get_model('Projects', 'AreaType')
    NearestArea = apps.get_model('Projects', 'NearestArea')
    
    # Mapping from old CharField values to new AreaType names
    area_type_mapping = {
        'school': 'School',
        'hospital': 'Hospital',
        'metro': 'Metro Station',
        'mall': 'Shopping Mall',
        'restaurant': 'Restaurant',
        'park': 'Park',
        'airport': 'Airport',
        'bus_stop': 'Bus Stop',
        'bank': 'Bank',
        'atm': 'ATM',
        'gym': 'Gym',
        'temple': 'Temple',
        'church': 'Church',
        'mosque': 'Mosque',
        'other': 'Other',
    }
    
    # Update each NearestArea with the corresponding AreaType
    for nearest_area in NearestArea.objects.all():
        old_type = nearest_area.area_type_old
        if old_type in area_type_mapping:
            new_type_name = area_type_mapping[old_type]
            try:
                area_type = AreaType.objects.get(name=new_type_name)
                nearest_area.area_type = area_type
                nearest_area.save()
            except AreaType.DoesNotExist:
                # If for some reason the AreaType doesn't exist, skip this record
                print(f"Warning: AreaType '{new_type_name}' not found for NearestArea {nearest_area.id}")


def reverse_migration(apps, schema_editor):
    # Reverse: copy ForeignKey back to CharField
    NearestArea = apps.get_model('Projects', 'NearestArea')
    
    reverse_mapping = {
        'School': 'school',
        'Hospital': 'hospital',
        'Metro Station': 'metro',
        'Shopping Mall': 'mall',
        'Restaurant': 'restaurant',
        'Park': 'park',
        'Airport': 'airport',
        'Bus Stop': 'bus_stop',
        'Bank': 'bank',
        'ATM': 'atm',
        'Gym': 'gym',
        'Temple': 'temple',
        'Church': 'church',
        'Mosque': 'mosque',
        'Other': 'other',
    }
    
    for nearest_area in NearestArea.objects.all():
        if nearest_area.area_type:
            old_value = reverse_mapping.get(nearest_area.area_type.name, 'other')
            nearest_area.area_type_old = old_value
            nearest_area.save()


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0014_rename_area_type_field'),
    ]

    operations = [
        migrations.RunPython(migrate_area_type_data, reverse_migration),
    ]
