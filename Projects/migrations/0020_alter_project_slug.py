# Generated manually to alter slug field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0019_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(db_index=True, help_text='Auto-generated from name', max_length=250, unique=True),
        ),
    ]
