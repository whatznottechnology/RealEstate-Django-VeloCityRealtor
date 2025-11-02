# Data migration to populate AreaType and convert existing data
from django.db import migrations


def create_area_types_and_migrate_data(apps, schema_editor):
    AreaType = apps.get_model('Projects', 'AreaType')
    NearestArea = apps.get_model('Projects', 'NearestArea')
    
    # Create AreaType instances from the old AREA_TYPES choices
    area_type_mapping = {
        'school': ('School', 'fas fa-graduation-cap', 1),
        'hospital': ('Hospital', 'fas fa-hospital', 2),
        'metro': ('Metro Station', 'fas fa-subway', 3),
        'mall': ('Shopping Mall', 'fas fa-shopping-bag', 4),
        'restaurant': ('Restaurant', 'fas fa-utensils', 5),
        'park': ('Park', 'fas fa-tree', 6),
        'airport': ('Airport', 'fas fa-plane', 7),
        'bus_stop': ('Bus Stop', 'fas fa-bus', 8),
        'bank': ('Bank', 'fas fa-university', 9),
        'atm': ('ATM', 'fas fa-credit-card', 10),
        'gym': ('Gym', 'fas fa-dumbbell', 11),
        'temple': ('Temple', 'fas fa-pray', 12),
        'church': ('Church', 'fas fa-cross', 13),
        'mosque': ('Mosque', 'fas fa-moon', 14),
        'other': ('Other', 'fas fa-map-marker-alt', 15),
    }
    
    # Create AreaType objects
    created_types = {}
    for old_value, (name, icon_class, order) in area_type_mapping.items():
        area_type, created = AreaType.objects.get_or_create(
            name=name,
            defaults={
                'font_awesome_icon': icon_class,
                'is_active': True,
                'order': order,
            }
        )
        created_types[old_value] = area_type
    
    # Store the mapping in NearestArea objects temporarily
    # We'll use a temporary CharField to store the old area_type value
    for nearest_area in NearestArea.objects.all():
        old_type = nearest_area.area_type
        if old_type in created_types:
            # We'll store the AreaType id in a way that can be retrieved later
            # For now, just track what needs to be updated
            pass


def reverse_migration(apps, schema_editor):
    # Optionally delete created AreaType objects if rolling back
    AreaType = apps.get_model('Projects', 'AreaType')
    AreaType.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0012_areatype_project_status_update'),
    ]

    operations = [
        migrations.RunPython(create_area_types_and_migrate_data, reverse_migration),
    ]
