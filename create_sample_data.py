#!/usr/bin/env python
"""
Script to create sample data for the Real Estate Project Management System
"""
import os
import django
from decimal import Decimal
from datetime import date, datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Source.settings')
django.setup()

from Projects.models import (
    City, Category, ProjectType, Tag, Amenity, SpecificationCategory,
    Project, ProjectOverview, NearestArea, FloorPlan, ConstructionUpdate,
    WhyChooseUs, SpecificationItem, GalleryImage, ProjectAmenityImage
)
from django.core.files import File
import random

def create_sample_data():
    print("🚀 Creating sample data for Real Estate Project Management...")

    # Load demo images from static/images/demoimages
    BASE_STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images', 'demoimages')
    demo_images = [os.path.join(BASE_STATIC, f) for f in os.listdir(BASE_STATIC) if f.lower().endswith('.jpg')]
    if not demo_images:
        print("❌ No demo images found in static/images/demoimages. Please add images before running this script.")
        return
    print(f"🖼️ Found {len(demo_images)} demo images.")
    def get_random_image():
        return random.choice(demo_images)
    
    # Create Cities
    print("📍 Creating cities...")
    cities = [
        {
            'name': 'Mumbai', 
            'state': 'Maharashtra', 
            'country': 'India',
            'description': 'Financial capital of India with premium residential and commercial projects',
            'keywords': 'Mumbai real estate, Maharashtra properties, financial district',
            'meta_title': 'Mumbai Real Estate - Premium Projects | VeloCity Realtor',
            'meta_description': 'Explore premium real estate projects in Mumbai. Find luxury apartments, commercial spaces, and investment opportunities in India\'s financial capital.'
        },
        {
            'name': 'Delhi', 
            'state': 'Delhi', 
            'country': 'India',
            'description': 'Capital city with diverse residential and commercial real estate opportunities',
            'keywords': 'Delhi real estate, NCR properties, capital city homes',
            'meta_title': 'Delhi Real Estate - Premium Properties | VeloCity Realtor',
            'meta_description': 'Discover premium real estate projects in Delhi. From luxury apartments to commercial spaces in India\'s capital city.'
        },
        {
            'name': 'Bangalore', 
            'state': 'Karnataka', 
            'country': 'India',
            'description': 'Silicon Valley of India with modern residential and IT commercial spaces',
            'keywords': 'Bangalore real estate, Karnataka properties, IT hub homes',
            'meta_title': 'Bangalore Real Estate - Tech City Properties | VeloCity Realtor',
            'meta_description': 'Find premium real estate projects in Bangalore. Modern apartments and commercial spaces in India\'s tech capital.'
        },
        {
            'name': 'Hyderabad', 
            'state': 'Telangana', 
            'country': 'India',
            'description': 'Cyberabad with emerging residential and commercial developments',
            'keywords': 'Hyderabad real estate, Telangana properties, Cyberabad homes',
            'meta_title': 'Hyderabad Real Estate - Cyberabad Properties | VeloCity Realtor',
            'meta_description': 'Explore real estate opportunities in Hyderabad. Modern residential and commercial projects in Telangana\'s tech hub.'
        },
        {
            'name': 'Chennai', 
            'state': 'Tamil Nadu', 
            'country': 'India',
            'description': 'Detroit of India with traditional and modern real estate projects',
            'keywords': 'Chennai real estate, Tamil Nadu properties, automotive city homes',
            'meta_title': 'Chennai Real Estate - Coastal Properties | VeloCity Realtor',
            'meta_description': 'Discover real estate projects in Chennai. Premium residential and commercial properties in Tamil Nadu\'s automotive hub.'
        },
    ]
    
    for city_data in cities:
        city, created = City.objects.get_or_create(
            name=city_data['name'],
            defaults=city_data
        )
        if created:
            print(f"  ✅ Created city: {city.name}")
    
    # Create Categories
    print("📂 Creating categories...")
    categories_data = [
        {
            'name': 'Residential',
            'description': 'Residential real estate projects including apartments, villas, and housing complexes',
            'keywords': 'residential properties, apartments, villas, homes for sale',
            'meta_title': 'Residential Properties - Homes & Apartments | VeloCity Realtor',
            'meta_description': 'Browse premium residential real estate projects. Find luxury apartments, villas, and homes for sale across major cities.'
        },
        {
            'name': 'Commercial',
            'description': 'Commercial real estate projects including offices, retail spaces, and business complexes',
            'keywords': 'commercial properties, office spaces, retail shops, business centers',
            'meta_title': 'Commercial Properties - Office & Retail Spaces | VeloCity Realtor',
            'meta_description': 'Explore commercial real estate opportunities. Premium office spaces, retail shops, and business centers for investment.'
        },
        {
            'name': 'Mixed Use',
            'description': 'Mixed-use developments combining residential and commercial spaces',
            'keywords': 'mixed use developments, residential commercial combo, integrated projects',
            'meta_title': 'Mixed Use Developments - Integrated Projects | VeloCity Realtor',
            'meta_description': 'Discover mixed-use developments combining residential and commercial spaces. Modern integrated real estate projects.'
        }
    ]
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'], 
            defaults=cat_data
        )
        if created:
            print(f"  ✅ Created category: {category.name}")
    
    # Create Project Types
    print("🏠 Creating project types...")
    project_types = [
        {
            'name': 'Apartment', 
            'category': 'Residential',
            'description': 'Modern apartment complexes with contemporary amenities and facilities',
            'keywords': 'apartments, flats, residential complexes, modern homes',
            'meta_title': 'Apartments for Sale - Modern Residential Complexes | VeloCity Realtor',
            'meta_description': 'Find premium apartments and flats for sale. Modern residential complexes with contemporary amenities and facilities.'
        },
        {
            'name': 'Villa', 
            'category': 'Residential',
            'description': 'Luxury independent villas with private gardens and premium amenities',
            'keywords': 'villas, independent houses, luxury homes, private gardens',
            'meta_title': 'Luxury Villas for Sale - Independent Houses | VeloCity Realtor',
            'meta_description': 'Explore luxury villas and independent houses for sale. Premium homes with private gardens and exclusive amenities.'
        },
        {
            'name': 'Penthouse', 
            'category': 'Residential',
            'description': 'Ultra-luxury penthouses with panoramic views and premium facilities',
            'keywords': 'penthouses, luxury apartments, sky homes, panoramic views',
            'meta_title': 'Luxury Penthouses for Sale - Sky Homes | VeloCity Realtor',
            'meta_description': 'Discover ultra-luxury penthouses with panoramic city views. Premium sky homes with exclusive amenities and facilities.'
        },
        {
            'name': 'Office Space', 
            'category': 'Commercial',
            'description': 'Modern office spaces and business centers with professional amenities',
            'keywords': 'office spaces, business centers, commercial properties, corporate offices',
            'meta_title': 'Office Spaces for Sale - Commercial Properties | VeloCity Realtor',
            'meta_description': 'Find premium office spaces and business centers. Modern commercial properties with professional amenities and facilities.'
        },
        {
            'name': 'Retail Space', 
            'category': 'Commercial',
            'description': 'Prime retail spaces and shops in high-traffic commercial areas',
            'keywords': 'retail spaces, shops, commercial stores, business properties',
            'meta_title': 'Retail Spaces for Sale - Commercial Shops | VeloCity Realtor',
            'meta_description': 'Explore prime retail spaces and shops for sale. Commercial properties in high-traffic areas with excellent visibility.'
        },
        {
            'name': 'Mixed Development', 
            'category': 'Mixed Use',
            'description': 'Integrated developments combining residential and commercial spaces',
            'keywords': 'mixed developments, integrated projects, residential commercial combo',
            'meta_title': 'Mixed Use Developments - Integrated Projects | VeloCity Realtor',
            'meta_description': 'Discover mixed-use developments combining residential and commercial spaces. Modern integrated real estate projects.'
        },
    ]
    
    for pt_data in project_types:
        category = Category.objects.get(name=pt_data['category'])
        project_type, created = ProjectType.objects.get_or_create(
            name=pt_data['name'],
            category=category,
            defaults={
                'description': pt_data['description'],
                'keywords': pt_data['keywords'],
                'meta_title': pt_data['meta_title'],
                'meta_description': pt_data['meta_description']
            }
        )
        if created:
            print(f"  ✅ Created project type: {project_type.name}")
    
    # Create Tags
    print("🏷️ Creating tags...")
    tags = [
        {'name': 'Trending', 'color': '#ff6b6b'},
        {'name': 'Hot Deal', 'color': '#ff4757'},
        {'name': 'Ready to Move', 'color': '#2ed573'},
        {'name': 'Just Launched', 'color': '#3742fa'},
        {'name': 'Premium', 'color': '#ffa502'},
        {'name': 'Ultra Luxury', 'color': '#ff6348'},
    ]
    
    for tag_data in tags:
        tag, created = Tag.objects.get_or_create(
            name=tag_data['name'],
            defaults=tag_data
        )
        if created:
            print(f"  ✅ Created tag: {tag.name}")
    
    # Create Amenities
    print("🏊 Creating amenities...")
    amenities_data = [
        {
            'name': 'Swimming Pool',
            'description': 'Premium swimming pool with poolside amenities and water features',
            'keywords': 'swimming pool, pool, water features, aquatic facilities',
            'meta_title': 'Swimming Pool Amenity - Premium Water Features | VeloCity Realtor',
            'meta_description': 'Enjoy premium swimming pool amenities with poolside facilities and water features in our residential projects.'
        },
        {
            'name': 'Gym',
            'description': 'Fully equipped fitness center with modern exercise equipment',
            'keywords': 'gym, fitness center, workout, exercise equipment',
            'meta_title': 'Gym Amenity - Modern Fitness Center | VeloCity Realtor',
            'meta_description': 'Stay fit with our fully equipped gym and fitness center featuring modern exercise equipment and facilities.'
        },
        {
            'name': 'Clubhouse',
            'description': 'Spacious clubhouse for social gatherings and community events',
            'keywords': 'clubhouse, community center, social events, gatherings',
            'meta_title': 'Clubhouse Amenity - Community Center | VeloCity Realtor',
            'meta_description': 'Enjoy our spacious clubhouse for social gatherings, community events, and recreational activities.'
        },
        {
            'name': 'Garden',
            'description': 'Beautifully landscaped gardens with green spaces and walking paths',
            'keywords': 'garden, landscaping, green spaces, nature, walking paths',
            'meta_title': 'Garden Amenity - Landscaped Green Spaces | VeloCity Realtor',
            'meta_description': 'Relax in our beautifully landscaped gardens with green spaces, walking paths, and natural environments.'
        },
        {
            'name': 'Security',
            'description': '24/7 security with CCTV surveillance and trained security personnel',
            'keywords': 'security, 24/7 surveillance, CCTV, safety, protection',
            'meta_title': 'Security Amenity - 24/7 Safety & Surveillance | VeloCity Realtor',
            'meta_description': 'Feel secure with our 24/7 security system featuring CCTV surveillance and trained security personnel.'
        },
        # Add more amenities with basic info
        {'name': 'Parking', 'description': 'Covered parking spaces for residents and visitors'},
        {'name': 'Power Backup', 'description': 'Uninterrupted power supply with backup generators'},
        {'name': 'Elevator', 'description': 'High-speed elevators for easy access to all floors'},
        {'name': 'Playground', 'description': 'Safe and fun playground for children'},
        {'name': 'Jogging Track', 'description': 'Dedicated jogging track for fitness enthusiasts'},
        {'name': 'Tennis Court', 'description': 'Professional tennis court for sports activities'},
        {'name': 'Basketball Court', 'description': 'Full-size basketball court for recreational games'},
        {'name': 'Meditation Center', 'description': 'Peaceful meditation center for relaxation'},
        {'name': 'Library', 'description': 'Well-stocked library for reading and study'},
        {'name': 'Banquet Hall', 'description': 'Elegant banquet hall for special events'},
        {'name': 'Conference Room', 'description': 'Professional conference room for business meetings'},
        {'name': 'Spa', 'description': 'Luxury spa for wellness and relaxation'},
        {'name': 'Sauna', 'description': 'Relaxing sauna for health and wellness'},
        {'name': 'Jacuzzi', 'description': 'Premium jacuzzi for ultimate relaxation'}
    ]
    
    for amenity_data in amenities_data:
        amenity, created = Amenity.objects.get_or_create(
            name=amenity_data['name'],
            defaults={
                'description': amenity_data.get('description', ''),
                'keywords': amenity_data.get('keywords', ''),
                'meta_title': amenity_data.get('meta_title', ''),
                'meta_description': amenity_data.get('meta_description', '')
            }
        )
        if created:
            print(f"  ✅ Created amenity: {amenity.name}")
    
    # Create Specification Categories
    print("📋 Creating specification categories...")
    spec_categories = [
        {'name': 'Flooring', 'order': 1},
        {'name': 'Kitchen', 'order': 2},
        {'name': 'Bathroom', 'order': 3},
        {'name': 'Doors & Windows', 'order': 4},
        {'name': 'Electrical', 'order': 5},
        {'name': 'Plumbing', 'order': 6},
        {'name': 'Paint & Finish', 'order': 7},
    ]
    
    for spec_data in spec_categories:
        spec_cat, created = SpecificationCategory.objects.get_or_create(
            name=spec_data['name'],
            defaults=spec_data
        )
        if created:
            print(f"  ✅ Created specification category: {spec_cat.name}")
    
    # Create Sample Projects
    print("🏢 Creating sample projects...")
    projects = [
        {
            'name': 'Luxury Heights',
            'project_by': 'Dream Builders',
            'location': 'Bandra West, Mumbai',
            'city': 'Mumbai',
            'developers': 'Dream Builders Pvt Ltd',
            'build_up_area': '1200-2500 sq ft',
            'bhk': '2, 3, 4 BHK',
            'no_of_blocks': 5,
            'no_of_units': 120,
            'status': 'under_construction',
            'possession_date': date(2025, 12, 31),
            'onwards_price': Decimal('85000000'),
            'category': 'Residential',
            'project_type': 'Apartment',
            'trending_tag': 'premium',
            'is_featured': True,
            'description': 'Luxury residential project with premium amenities and modern architecture. Located in prime area with excellent connectivity.',
            'keywords': 'luxury apartments, premium residential, modern amenities, prime location',
            'meta_title': 'Sky High Residences - Luxury Apartments in Mumbai | VeloCity Realtor',
            'meta_description': 'Experience luxury living at Sky High Residences in Mumbai. Premium apartments with modern amenities and excellent connectivity.'
        },
        {
            'name': 'Green Valley Villas',
            'project_by': 'Eco Homes',
            'location': 'Whitefield, Bangalore',
            'city': 'Bangalore',
            'developers': 'Eco Homes Development',
            'build_up_area': '3000-5000 sq ft',
            'bhk': '3, 4, 5 BHK',
            'no_of_blocks': 8,
            'no_of_units': 45,
            'status': 'ready_to_move',
            'possession_date': date(2024, 6, 30),
            'onwards_price': Decimal('12000000'),
            'category': 'Residential',
            'project_type': 'Villa',
            'trending_tag': 'ready_to_move',
            'is_hot_deal': True,
            'description': 'Premium villa project with spacious layouts and eco-friendly features. Ready to move independent villas in prime location.',
            'keywords': 'luxury villas, independent houses, eco-friendly, ready to move',
            'meta_title': 'Green Valley Villas - Premium Villas in Bangalore | VeloCity Realtor',
            'meta_description': 'Move into luxury at Green Valley Villas in Bangalore. Premium independent villas with eco-friendly features and spacious layouts.'
        },
        {
            'name': 'Tech Park Plaza',
            'project_by': 'Commercial Developers',
            'location': 'Cyber City, Hyderabad',
            'city': 'Hyderabad',
            'developers': 'Commercial Developers Ltd',
            'build_up_area': '500-10000 sq ft',
            'bhk': 'Office Spaces',
            'no_of_blocks': 3,
            'no_of_units': 200,
            'status': 'under_construction',
            'possession_date': date(2025, 9, 15),
            'onwards_price': Decimal('5000000'),
            'category': 'Commercial',
            'project_type': 'Office Space',
            'trending_tag': 'just_launched',
            'is_premium_listing': True,
            'description': 'Modern commercial complex with state-of-the-art office spaces and business facilities. Prime location in tech corridor.',
            'keywords': 'office spaces, commercial complex, tech park, business facilities',
            'meta_title': 'Tech Park Plaza - Premium Office Spaces in Hyderabad | VeloCity Realtor',
            'meta_description': 'Discover premium office spaces at Tech Park Plaza in Hyderabad. Modern commercial complex in the heart of tech corridor.'
        }
    ]
    
    for project_data in projects:
        city = City.objects.get(name=project_data['city'])
        category = Category.objects.get(name=project_data['category'])
        project_type = ProjectType.objects.get(name=project_data['project_type'])

        # Assign a random banner image for the project
        with open(get_random_image(), 'rb') as img_file:
            project_banner = File(img_file, name=os.path.basename(img_file.name))
            project_data_with_image = dict(project_data)
            project_data_with_image['banner_image'] = project_banner

            project, created = Project.objects.get_or_create(
                name=project_data['name'],
                defaults={
                    **project_data_with_image,
                    'city': city,
                    'category': category,
                    'project_type': project_type,
                }
            )

        if created:
            print(f"  ✅ Created project: {project.name}")

            # Add tags and amenities
            trending_tags = Tag.objects.filter(name__in=['Trending', 'Hot Deal'])
            project.tags.set(trending_tags)

            sample_amenities = Amenity.objects.filter(
                name__in=['Swimming Pool', 'Gym', 'Security', 'Parking', 'Garden']
            )
            project.amenities.set(sample_amenities)

            # Create Project Overview
            ProjectOverview.objects.create(
                project=project,
                title=f"Welcome to {project.name}",
                short_description=f"{project.name} offers modern living with premium amenities and excellent connectivity. Experience luxury living at its finest with world-class facilities and prime location."
            )

            # Create Nearest Areas
            nearest_areas = [
                {'name': 'Metro Station', 'area_type': 'metro', 'distance': '0.5 km'},
                {'name': 'Shopping Mall', 'area_type': 'mall', 'distance': '1.2 km'},
                {'name': 'International School', 'area_type': 'school', 'distance': '0.8 km'},
                {'name': 'Multi-Specialty Hospital', 'area_type': 'hospital', 'distance': '1.5 km'},
            ]

            for area_data in nearest_areas:
                NearestArea.objects.create(project=project, **area_data)

            # Create Gallery Images (3 per project)
            for i in range(3):
                with open(get_random_image(), 'rb') as img_file:
                    GalleryImage.objects.create(
                        project=project,
                        image=File(img_file, name=os.path.basename(img_file.name)),
                        caption=f"Gallery Image {i+1}",
                        order=i
                    )

            # Create Floor Plans (2 per project)
            if project.project_type.name == 'Apartment':
                floor_plans = [
                    {'name': '2 BHK', 'area': '1200 sq ft', 'price': Decimal('8500000')},
                    {'name': '3 BHK', 'area': '1800 sq ft', 'price': Decimal('12000000')},
                    {'name': '4 BHK', 'area': '2500 sq ft', 'price': Decimal('18000000')},
                ]
            else:
                floor_plans = [
                    {'name': 'Ground Floor', 'area': '3000 sq ft', 'price': Decimal('12000000')},
                    {'name': 'First Floor', 'area': '2500 sq ft', 'price': Decimal('10000000')},
                ]
            for i, fp_data in enumerate(floor_plans):
                with open(get_random_image(), 'rb') as img_file:
                    FloorPlan.objects.create(
                        project=project,
                        image=File(img_file, name=os.path.basename(img_file.name)),
                        order=i,
                        **fp_data
                    )

            # Create Construction Updates (2 per project)
            for i in range(2):
                with open(get_random_image(), 'rb') as img_file:
                    ConstructionUpdate.objects.create(
                        project=project,
                        image=File(img_file, name=os.path.basename(img_file.name)),
                        title=f"Update {i+1}",
                        description=f"Construction update {i+1} for {project.name}",
                        update_date=date.today(),
                        order=i
                    )

            # Create Project Amenity Images (2 per project)
            amenity_names = ['Swimming Pool', 'Gym', 'Clubhouse', 'Garden']
            for i, amenity_name in enumerate(random.sample(amenity_names, 2)):
                with open(get_random_image(), 'rb') as img_file:
                    ProjectAmenityImage.objects.create(
                        project=project,
                        amenity_name=amenity_name,
                        image=File(img_file, name=os.path.basename(img_file.name)),
                        is_active=True
                    )

            # Create Why Choose Us
            why_choose_us = [
                {'title': 'Prime Location', 'description': 'Located in the heart of the city with excellent connectivity.', 'icon': 'fas fa-map-marker-alt'},
                {'title': 'Modern Amenities', 'description': 'World-class facilities and amenities for comfortable living.', 'icon': 'fas fa-swimming-pool'},
                {'title': 'Quality Construction', 'description': 'Built with premium materials and superior craftsmanship.', 'icon': 'fas fa-hammer'},
                {'title': 'Green Environment', 'description': 'Eco-friendly design with lush green landscapes.', 'icon': 'fas fa-leaf'},
            ]

            for wcu_data in why_choose_us:
                WhyChooseUs.objects.create(project=project, **wcu_data)

            # Create Specification Items
            flooring_cat = SpecificationCategory.objects.get(name='Flooring')
            kitchen_cat = SpecificationCategory.objects.get(name='Kitchen')

            SpecificationItem.objects.create(
                project=project,
                category=flooring_cat,
                name='Living Room',
                description='Premium vitrified tiles with anti-skid finish'
            )

            SpecificationItem.objects.create(
                project=project,
                category=kitchen_cat,
                name='Kitchen Counter',
                description='Granite countertop with stainless steel sink'
            )
    
    print("✅ Sample data created successfully!")
    print("\n🎉 You can now access the admin panel at: http://127.0.0.1:8000/admin/")
    print("👤 Username: admin")
    print("🔑 Password: admin123")

if __name__ == '__main__':
    create_sample_data()
