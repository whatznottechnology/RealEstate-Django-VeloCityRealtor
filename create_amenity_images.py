#!/usr/bin/env python
"""
Script to create sample Project Amenity Images
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Source.settings')
django.setup()

from Projects.models import Project, ProjectAmenityImage

def create_sample_amenity_images():
    print("🏊 Creating sample Project Amenity Images...")
    
    # Get existing projects
    projects = Project.objects.all()
    
    if not projects.exists():
        print("❌ No projects found. Please create projects first.")
        return
    
    # Sample amenity data
    amenity_data = [
        "Swimming Pool",
        "Gym & Fitness Center", 
        "Clubhouse",
        "Children's Playground",
        "Jogging Track",
        "Security & CCTV",
        "Parking Area",
        "Garden & Landscaping",
        "Community Hall",
        "Sports Court"
    ]
    
    for project in projects:
        print(f"  🏢 Adding amenity images for project: {project.name}")
        
        # Add 3-5 random amenities per project
        for i, amenity_name in enumerate(amenity_data[:5]):  # First 5 amenities
            amenity_image, created = ProjectAmenityImage.objects.get_or_create(
                project=project,
                amenity_name=amenity_name,
                defaults={
                    'is_active': True,
                }
            )
            
            if created:
                print(f"    ✅ Added amenity image: {amenity_name}")
            else:
                print(f"    ℹ️ Amenity image already exists: {amenity_name}")
    
    print("\n✅ Sample Project Amenity Images created successfully!")
    print(f"📊 Total amenity images: {ProjectAmenityImage.objects.count()}")
    print("\n🎯 You can now:")
    print("1. Go to Projects → Edit any project")
    print("2. Scroll down to the 'Amenity Images' tab")
    print("3. Add actual images for each amenity")
    print("4. Or go to Projects → Project Amenity Images to manage them separately")

if __name__ == '__main__':
    create_sample_amenity_images()
