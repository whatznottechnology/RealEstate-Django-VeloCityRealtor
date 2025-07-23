from django.core.management.base import BaseCommand
from django.utils import timezone
from land_leads.models import LandRequirement
from investment_leads.models import InvestmentRequirement
from Projects.models import Project, City, Category, ProjectType, Tag, Amenity
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create demo data for all apps'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating demo data...'))
        
        # Create basic data for Projects
        self.create_cities()
        self.create_categories()
        self.create_project_types()
        self.create_tags()
        self.create_amenities()
        
        # Create demo projects
        self.create_projects()
        
        # Create demo land requirements
        self.create_land_requirements()
        
        # Create demo investment requirements
        self.create_investment_requirements()
        
        self.stdout.write(self.style.SUCCESS('Demo data created successfully!'))

    def create_cities(self):
        cities_data = [
            {'name': 'Kolkata', 'state': 'West Bengal'},
            {'name': 'Mumbai', 'state': 'Maharashtra'},
            {'name': 'Delhi', 'state': 'Delhi'},
            {'name': 'Bangalore', 'state': 'Karnataka'},
            {'name': 'Chennai', 'state': 'Tamil Nadu'},
            {'name': 'Hyderabad', 'state': 'Telangana'},
            {'name': 'Pune', 'state': 'Maharashtra'},
            {'name': 'Ahmedabad', 'state': 'Gujarat'},
        ]
        
        for city_data in cities_data:
            City.objects.get_or_create(**city_data)
        
        self.stdout.write('Cities created.')

    def create_categories(self):
        categories = ['Residential', 'Commercial', 'Industrial', 'Mixed Use']
        
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
        
        self.stdout.write('Categories created.')

    def create_project_types(self):
        project_types_data = [
            {'name': 'Apartment', 'category': 'Residential'},
            {'name': 'Villa', 'category': 'Residential'},
            {'name': 'Townhouse', 'category': 'Residential'},
            {'name': 'Office Space', 'category': 'Commercial'},
            {'name': 'Retail Store', 'category': 'Commercial'},
            {'name': 'Shopping Mall', 'category': 'Commercial'},
            {'name': 'Warehouse', 'category': 'Industrial'},
            {'name': 'Factory', 'category': 'Industrial'},
        ]
        
        for pt_data in project_types_data:
            category = Category.objects.get(name=pt_data['category'])
            ProjectType.objects.get_or_create(
                name=pt_data['name'],
                category=category
            )
        
        self.stdout.write('Project types created.')

    def create_tags(self):
        tags_data = [
            {'name': 'Trending', 'color': '#ff6b6b'},
            {'name': 'Hot Deal', 'color': '#ff9f43'},
            {'name': 'Premium', 'color': '#a55eea'},
            {'name': 'New Launch', 'color': '#26de81'},
            {'name': 'Ready to Move', 'color': '#fd79a8'},
            {'name': 'Under Construction', 'color': '#fdcb6e'},
        ]
        
        for tag_data in tags_data:
            Tag.objects.get_or_create(**tag_data)
        
        self.stdout.write('Tags created.')

    def create_amenities(self):
        amenities = [
            'Swimming Pool', 'Gym', 'Clubhouse', 'Children\'s Play Area',
            'Parking', 'Security', 'Garden', 'Jogging Track',
            'Community Hall', 'Power Backup', 'Elevator', 'Intercom',
            'Fire Safety', 'Water Supply', 'Maintenance', 'Wi-Fi'
        ]
        
        for amenity_name in amenities:
            Amenity.objects.get_or_create(name=amenity_name)
        
        self.stdout.write('Amenities created.')

    def create_projects(self):
        projects_data = [
            {
                'name': 'Sunrise Heights',
                'project_by': 'Sunrise Developers',
                'location': 'Salt Lake, Kolkata',
                'developers': 'Sunrise Developers Ltd.',
                'build_up_area': '1200-1800 sq ft',
                'bhk': '2, 3, 4 BHK',
                'no_of_blocks': 4,
                'no_of_units': 160,
                'status': 'under_construction',
                'onwards_price': Decimal('6500000'),
                'is_featured': True,
                'is_most_viewed': True,
                'trending_tag': 'just_launched',
            },
            {
                'name': 'Golden Palms',
                'project_by': 'Golden Builders',
                'location': 'Rajarhat, Kolkata',
                'developers': 'Golden Builders Pvt. Ltd.',
                'build_up_area': '900-1400 sq ft',
                'bhk': '2, 3 BHK',
                'no_of_blocks': 3,
                'no_of_units': 120,
                'status': 'ready_to_move',
                'onwards_price': Decimal('4500000'),
                'is_hot_deal': True,
                'trending_tag': 'ready_to_move',
            },
            {
                'name': 'Metro Plaza',
                'project_by': 'Metro Constructions',
                'location': 'Park Street, Kolkata',
                'developers': 'Metro Constructions',
                'build_up_area': '500-2000 sq ft',
                'bhk': 'Office Space',
                'no_of_blocks': 1,
                'no_of_units': 50,
                'status': 'under_construction',
                'onwards_price': Decimal('12000000'),
                'is_premium_listing': True,
                'trending_tag': 'premium',
            },
            {
                'name': 'Riverside Residency',
                'project_by': 'Riverside Developers',
                'location': 'Hooghly Riverfront, Kolkata',
                'developers': 'Riverside Developers',
                'build_up_area': '1500-2200 sq ft',
                'bhk': '3, 4 BHK',
                'no_of_blocks': 6,
                'no_of_units': 240,
                'status': 'upcoming',
                'onwards_price': Decimal('8500000'),
                'is_editors_choice': True,
                'trending_tag': 'ultra_luxury',
            },
            {
                'name': 'Tech Park Central',
                'project_by': 'Tech Builders',
                'location': 'Sector V, Kolkata',
                'developers': 'Tech Builders Ltd.',
                'build_up_area': '800-1600 sq ft',
                'bhk': '1, 2, 3 BHK',
                'no_of_blocks': 2,
                'no_of_units': 80,
                'status': 'ready_to_move',
                'onwards_price': Decimal('3500000'),
                'is_nearby_property': True,
                'trending_tag': 'affordable',
            },
        ]
        
        cities = list(City.objects.all())
        categories = list(Category.objects.all())
        project_types = list(ProjectType.objects.all())
        tags = list(Tag.objects.all())
        amenities = list(Amenity.objects.all())
        
        for project_data in projects_data:
            city = random.choice(cities)
            category = random.choice(categories)
            project_type = random.choice(project_types.filter(category=category)) if project_types.filter(category=category) else random.choice(project_types)
            
            project, created = Project.objects.get_or_create(
                name=project_data['name'],
                defaults={
                    **project_data,
                    'city': city,
                    'category': category,
                    'project_type': project_type,
                }
            )
            
            if created:
                # Add random tags and amenities
                project.tags.set(random.sample(tags, k=random.randint(2, 4)))
                project.amenities.set(random.sample(amenities, k=random.randint(5, 10)))
        
        self.stdout.write('Projects created.')

    def create_land_requirements(self):
        land_requirements_data = [
            {
                'name': 'Rajesh Kumar',
                'email': 'rajesh@example.com',
                'contact_number': '+91 9876543210',
                'location': 'Rajarhat, Kolkata',
                'budget': '₹15-20 Lakh',
                'area': Decimal('5.5'),
                'area_unit': 'bigha',
                'requirement_type': 'buy',
                'agreed_to_terms': True,
            },
            {
                'name': 'Priya Sharma',
                'email': 'priya.sharma@example.com',
                'contact_number': '+91 9876543211',
                'location': 'Salt Lake, Kolkata',
                'budget': '₹8-12 Lakh',
                'area': Decimal('3.2'),
                'area_unit': 'bigha',
                'requirement_type': 'buy',
                'agreed_to_terms': True,
            },
            {
                'name': 'Amit Ghosh',
                'email': 'amit.ghosh@example.com',
                'contact_number': '+91 9876543212',
                'location': 'Howrah, West Bengal',
                'budget': '₹25-35 Lakh',
                'area': Decimal('2.8'),
                'area_unit': 'acre',
                'requirement_type': 'sale',
                'agreed_to_terms': False,
            },
            {
                'name': 'Sunita Devi',
                'contact_number': '+91 9876543213',
                'location': 'Barasat, North 24 Parganas',
                'budget': '₹5-8 Lakh',
                'area': Decimal('150.0'),
                'area_unit': 'cottah',
                'requirement_type': 'joint_venture',
                'agreed_to_terms': True,
            },
            {
                'name': 'Debasis Roy',
                'email': 'debasis.roy@example.com',
                'contact_number': '+91 9876543214',
                'location': 'Durgapur, West Bengal',
                'budget': '₹40-60 Lakh',
                'area': Decimal('8.5'),
                'area_unit': 'bigha',
                'requirement_type': 'buy',
                'agreed_to_terms': True,
            },
        ]
        
        for req_data in land_requirements_data:
            LandRequirement.objects.get_or_create(
                contact_number=req_data['contact_number'],
                defaults=req_data
            )
        
        self.stdout.write('Land requirements created.')

    def create_investment_requirements(self):
        investment_requirements_data = [
            {
                'name': 'Suresh Agarwal',
                'email': 'suresh@example.com',
                'contact_number': '+91 9876543220',
                'location': 'Park Street, Kolkata',
                'budget': '₹2-3 Crore',
                'requirement_type': 'buy',
                'property_type': 'restaurant',
                'enquiry_from': 'owner',
                'property_details': 'Looking for a restaurant space in prime location with good footfall.',
                'agreed_to_terms': True,
            },
            {
                'name': 'Rakesh Jain',
                'email': 'rakesh.jain@example.com',
                'contact_number': '+91 9876543221',
                'location': 'Sector V, Kolkata',
                'budget': '₹5-8 Crore',
                'requirement_type': 'for_lease',
                'property_type': 'hotel',
                'enquiry_from': 'agent',
                'property_details': 'Premium hotel property for lease in IT hub area.',
                'agreed_to_terms': True,
            },
            {
                'name': 'Neha Gupta',
                'email': 'neha.gupta@example.com',
                'contact_number': '+91 9876543222',
                'location': 'Salt Lake, Kolkata',
                'budget': '₹1-2 Crore',
                'requirement_type': 'buy',
                'property_type': 'showroom',
                'enquiry_from': 'individual',
                'property_details': 'Showroom for automobile business in busy commercial area.',
                'agreed_to_terms': False,
            },
            {
                'name': 'Manish Patel',
                'contact_number': '+91 9876543223',
                'location': 'Rajarhat, Kolkata',
                'budget': '₹10-15 Crore',
                'requirement_type': 'sale',
                'property_type': 'petrol_pump',
                'enquiry_from': 'owner',
                'property_details': 'Existing petrol pump with good location and steady income.',
                'agreed_to_terms': True,
            },
            {
                'name': 'Anita Singh',
                'email': 'anita.singh@example.com',
                'contact_number': '+91 9876543224',
                'location': 'Howrah, West Bengal',
                'budget': '₹3-5 Crore',
                'requirement_type': 'want_lease',
                'property_type': 'banquet',
                'enquiry_from': 'agent',
                'property_details': 'Banquet hall for events and weddings with parking facility.',
                'agreed_to_terms': True,
            },
            {
                'name': 'Kiran Malhotra',
                'email': 'kiran.malhotra@example.com',
                'contact_number': '+91 9876543225',
                'location': 'New Town, Kolkata',
                'budget': '₹50 Lakh - 1 Crore',
                'requirement_type': 'buy',
                'property_type': 'bar',
                'enquiry_from': 'individual',
                'property_details': 'Bar and lounge in upscale area with modern amenities.',
                'agreed_to_terms': True,
            },
        ]
        
        for req_data in investment_requirements_data:
            InvestmentRequirement.objects.get_or_create(
                contact_number=req_data['contact_number'],
                defaults=req_data
            )
        
        self.stdout.write('Investment requirements created.')
