from django import forms
from .models import (
    Project, City, Category, ProjectType, Tag, Amenity,
    ProjectOverview, GalleryImage, NearestArea, FloorPlan,
    ConstructionUpdate, WhyChooseUs, SpecificationCategory,
    SpecificationItem
)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProjectForm(forms.ModelForm):
    """Comprehensive single-page form for Project creation"""
    
    # Project Overview fields (inline)
    overview_title = forms.CharField(
        max_length=200,
        required=False,
        label="Overview Title",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project overview title'})
    )
    overview_description = forms.CharField(
        required=False,
        label="Overview Description",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter detailed project overview'})
    )
    
    # Gallery Images (multiple file upload)
    gallery_images = MultipleFileField(
        required=False,
        label="Gallery Images",
        help_text="Upload multiple images for project gallery"
    )
    
    # Nearest Areas
    nearest_areas = forms.CharField(
        required=False,
        label="Nearby Locations",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter nearby locations separated by commas (e.g., School - 2km, Hospital - 1km, Mall - 3km)'}),
        help_text="Enter nearby locations with distances, separated by commas"
    )
    
    # Floor Plans
    floor_plan_images = MultipleFileField(
        required=False,
        label="Floor Plan Images",
        help_text="Upload floor plan images"
    )
    
    # Construction Updates
    construction_updates = forms.CharField(
        required=False,
        label="Construction Updates",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter construction updates separated by commas'}),
        help_text="Enter construction updates, separated by commas"
    )
    
    # Why Choose Us points
    why_choose_us = forms.CharField(
        required=False,
        label="Why Choose Us Points",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter key selling points separated by commas'}),
        help_text="Enter key selling points, separated by commas"
    )
    
    class Meta:
        model = Project
        fields = [
            'name', 'project_by', 'logo', 'banner_image', 'brochure',
            'location', 'city', 'developers', 'build_up_area', 'bhk',
            'no_of_blocks', 'no_of_units', 'status', 'possession_date',
            'onwards_price', 'latitude', 'longitude', 'category',
            'project_type', 'tags', 'amenities', 'is_most_viewed',
            'trending_tag', 'is_nearby_property', 'is_recently_viewed',
            'is_hot_deal', 'is_premium_listing', 'is_editors_choice',
            'is_featured', 'is_active'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'project_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company/brand name'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'banner_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'brochure': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full address'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'developers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter developer name'}),
            'build_up_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1200 sq ft'}),
            'bhk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2, 3, 4 BHK'}),
            'no_of_blocks': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'no_of_units': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'possession_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'onwards_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001', 'placeholder': 'Enter latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001', 'placeholder': 'Enter longitude'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'project_type': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'amenities': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'trending_tag': forms.Select(attrs={'class': 'form-select'}),
            'is_most_viewed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_nearby_property': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_recently_viewed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_hot_deal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_premium_listing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_editors_choice': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values for checkboxes
        self.fields['is_active'].initial = True
        
        # Make project_type dependent on category
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['project_type'].queryset = ProjectType.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['project_type'].queryset = ProjectType.objects.none()
        else:
            self.fields['project_type'].queryset = ProjectType.objects.none()
    
    def save(self, commit=True):
        """Override save to handle related objects"""
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Save many-to-many relationships
            self.save_m2m()
            
            # Handle project overview
            if self.cleaned_data.get('overview_title') or self.cleaned_data.get('overview_description'):
                ProjectOverview.objects.update_or_create(
                    project=instance,
                    defaults={
                        'title': self.cleaned_data.get('overview_title', ''),
                        'short_description': self.cleaned_data.get('overview_description', '')
                    }
                )
            
            # Handle nearest areas
            if self.cleaned_data.get('nearest_areas'):
                # Clear existing nearest areas
                NearestArea.objects.filter(project=instance).delete()
                
                areas = [area.strip() for area in self.cleaned_data['nearest_areas'].split(',') if area.strip()]
                for i, area in enumerate(areas):
                    if ' - ' in area:
                        place, distance = area.split(' - ', 1)
                        NearestArea.objects.create(
                            project=instance,
                            place=place.strip(),
                            distance=distance.strip(),
                            order=i + 1
                        )
            
            # Handle construction updates
            if self.cleaned_data.get('construction_updates'):
                # Clear existing construction updates
                ConstructionUpdate.objects.filter(project=instance).delete()
                
                updates = [update.strip() for update in self.cleaned_data['construction_updates'].split(',') if update.strip()]
                for i, update in enumerate(updates):
                    ConstructionUpdate.objects.create(
                        project=instance,
                        update=update,
                        order=i + 1
                    )
            
            # Handle why choose us points
            if self.cleaned_data.get('why_choose_us'):
                # Clear existing why choose us points
                WhyChooseUs.objects.filter(project=instance).delete()
                
                points = [point.strip() for point in self.cleaned_data['why_choose_us'].split(',') if point.strip()]
                for i, point in enumerate(points):
                    WhyChooseUs.objects.create(
                        project=instance,
                        point=point,
                        order=i + 1
                    )
        
        return instance
