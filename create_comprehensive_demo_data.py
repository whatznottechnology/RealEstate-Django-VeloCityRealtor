#!/usr/bin/env python
"""
Comprehensive Demo Data Creation Script for Real Estate Django Project
This script creates realistic demo data for all models with full details.
"""

import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Source.settings')
django.setup()

from Projects.models import (
    City, Category, ProjectType, Tag, Amenity, Project, 
    ProjectOverview, GalleryImage, NearestArea, FloorPlan, 
    ConstructionUpdate, WhyChooseUs, SpecificationCategory, 
    SpecificationItem, ProjectAmenityImage
)
from blogs.models import Blog, Tag as BlogTag
from career.models import Career
from investment_leads.models import InvestmentRequirement
from land_leads.models import LandRequirement
from theme.models import SiteConfig

def create_cities():
    """Create comprehensive city data"""
    print("Creating Cities...")
    
    cities_data = [
        {
            'name': 'Mumbai', 
            'state': 'Maharashtra', 
            'country': 'India',
            'description': 'Financial capital of India with premium real estate opportunities',
            'keywords': 'mumbai, maharashtra, real estate, properties, apartments',
            'meta_title': 'Real Estate Properties in Mumbai, Maharashtra',
            'meta_description': 'Find premium real estate properties in Mumbai. Residential and commercial projects in the financial capital of India.',
            'is_active': True
        },
        {
            'name': 'Delhi', 
            'state': 'Delhi', 
            'country': 'India',
            'description': 'Capital city with diverse residential and commercial properties',
            'keywords': 'delhi, ncr, real estate, properties, apartments, commercial',
            'meta_title': 'Properties in Delhi NCR - Real Estate Investment',
            'meta_description': 'Explore real estate opportunities in Delhi NCR. Premium residential and commercial properties.',
            'is_active': True
        },
        {
            'name': 'Bangalore', 
            'state': 'Karnataka', 
            'country': 'India',
            'description': 'IT capital with modern residential and commercial developments',
            'keywords': 'bangalore, karnataka, it city, real estate, tech hub',
            'meta_title': 'Real Estate in Bangalore - IT City Properties',
            'meta_description': 'Investment opportunities in Bangalore real estate. Modern residential and commercial properties in IT capital.',
            'is_active': True
        },
        {
            'name': 'Hyderabad', 
            'state': 'Telangana', 
            'country': 'India',
            'description': 'Emerging tech hub with excellent infrastructure and growth potential',
            'keywords': 'hyderabad, telangana, hitech city, real estate, cyberabad',
            'meta_title': 'Hyderabad Real Estate - Cyberabad Properties',
            'meta_description': 'Discover prime real estate in Hyderabad. Modern projects in Cyberabad and HITEC City.',
            'is_active': True
        },
        {
            'name': 'Chennai', 
            'state': 'Tamil Nadu', 
            'country': 'India',
            'description': 'Cultural capital with growing real estate market',
            'keywords': 'chennai, tamil nadu, real estate, properties, apartments',
            'meta_title': 'Chennai Real Estate Properties - Tamil Nadu',
            'meta_description': 'Explore real estate opportunities in Chennai. Residential and commercial properties in Tamil Nadu.',
            'is_active': True
        },
        {
            'name': 'Pune', 
            'state': 'Maharashtra', 
            'country': 'India',
            'description': 'Educational and IT hub with excellent connectivity',
            'keywords': 'pune, maharashtra, educational hub, real estate, it sector',
            'meta_title': 'Pune Real Estate - Educational & IT Hub Properties',
            'meta_description': 'Investment opportunities in Pune real estate. Properties in educational and IT hub of Maharashtra.',
            'is_active': True
        },
        {
            'name': 'Kolkata', 
            'state': 'West Bengal', 
            'country': 'India',
            'description': 'Cultural heritage city with affordable real estate options',
            'keywords': 'kolkata, west bengal, cultural city, real estate, heritage',
            'meta_title': 'Kolkata Real Estate - Cultural City Properties',
            'meta_description': 'Affordable real estate options in Kolkata. Cultural heritage properties in West Bengal.',
            'is_active': True
        },
        {
            'name': 'Ahmedabad', 
            'state': 'Gujarat', 
            'country': 'India',
            'description': 'Commercial capital of Gujarat with rapid development',
            'keywords': 'ahmedabad, gujarat, commercial capital, real estate, development',
            'meta_title': 'Ahmedabad Real Estate - Gujarat Commercial Hub',
            'meta_description': 'Real estate investment in Ahmedabad. Commercial and residential properties in Gujarat.',
            'is_active': True
        }
    ]
    
    cities = []
    for city_data in cities_data:
        city, created = City.objects.get_or_create(
            name=city_data['name'],
            state=city_data['state'],
            defaults=city_data
        )
        cities.append(city)
        if created:
            print(f"✅ Created city: {city.name}")
    
    return cities

def create_categories():
    """Create property categories"""
    print("Creating Categories...")
    
    categories_data = [
        {
            'name': 'Residential',
            'description': 'Residential properties including apartments, villas, and homes',
            'keywords': 'residential, apartments, villas, homes, living spaces',
            'meta_title': 'Residential Properties - Apartments & Villas',
            'meta_description': 'Find your dream residential property. Apartments, villas, and homes in prime locations.'
        },
        {
            'name': 'Commercial',
            'description': 'Commercial properties including offices, retail spaces, and business centers',
            'keywords': 'commercial, offices, retail, business centers, workspace',
            'meta_title': 'Commercial Properties - Offices & Retail Spaces',
            'meta_description': 'Premium commercial properties for business. Office spaces and retail locations.'
        },
        {
            'name': 'Mixed Development',
            'description': 'Mixed-use developments combining residential and commercial spaces',
            'keywords': 'mixed development, integrated township, residential commercial',
            'meta_title': 'Mixed Development Projects - Integrated Townships',
            'meta_description': 'Integrated townships with residential and commercial spaces in one location.'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories.append(category)
        if created:
            print(f"✅ Created category: {category.name}")
    
    return categories

def create_project_types(categories):
    """Create project types for each category"""
    print("Creating Project Types...")
    
    project_types_data = [
        # Residential Types
        {'name': 'Luxury Apartments', 'category': 'Residential'},
        {'name': 'Premium Villas', 'category': 'Residential'},
        {'name': 'Budget Apartments', 'category': 'Residential'},
        {'name': 'Duplex Homes', 'category': 'Residential'},
        {'name': 'Penthouse', 'category': 'Residential'},
        {'name': 'Studio Apartments', 'category': 'Residential'},
        {'name': 'Row Houses', 'category': 'Residential'},
        
        # Commercial Types
        {'name': 'Office Spaces', 'category': 'Commercial'},
        {'name': 'Retail Shops', 'category': 'Commercial'},
        {'name': 'Business Centers', 'category': 'Commercial'},
        {'name': 'IT Parks', 'category': 'Commercial'},
        {'name': 'Warehouses', 'category': 'Commercial'},
        {'name': 'Shopping Malls', 'category': 'Commercial'},
        
        # Mixed Development Types
        {'name': 'Integrated Township', 'category': 'Mixed Development'},
        {'name': 'Smart City Projects', 'category': 'Mixed Development'},
        {'name': 'Lifestyle Communities', 'category': 'Mixed Development'},
    ]
    
    category_map = {cat.name: cat for cat in categories}
    project_types = []
    
    for pt_data in project_types_data:
        category = category_map[pt_data['category']]
        project_type, created = ProjectType.objects.get_or_create(
            name=pt_data['name'],
            category=category,
            defaults={
                'description': f'{pt_data["name"]} in {category.name} category',
                'keywords': f'{pt_data["name"].lower()}, {category.name.lower()}, real estate',
                'meta_title': f'{pt_data["name"]} - {category.name} Properties',
                'meta_description': f'Explore {pt_data["name"]} projects. Premium {category.name.lower()} properties.'
            }
        )
        project_types.append(project_type)
        if created:
            print(f"✅ Created project type: {project_type.name}")
    
    return project_types

def create_tags():
    """Create property tags"""
    print("Creating Tags...")
    
    tags_data = [
        {'name': 'Trending', 'color': '#ff6b6b'},
        {'name': 'Hot Deal', 'color': '#ff9f43'},
        {'name': 'Premium', 'color': '#3742fa'},
        {'name': 'Luxury', 'color': '#8e44ad'},
        {'name': 'Ready to Move', 'color': '#2ed573'},
        {'name': 'Under Construction', 'color': '#ffa502'},
        {'name': 'New Launch', 'color': '#5f27cd'},
        {'name': 'Limited Offer', 'color': '#e74c3c'},
        {'name': 'Best Value', 'color': '#00a8ff'},
        {'name': 'Investment Grade', 'color': '#2f3542'},
    ]
    
    tags = []
    for tag_data in tags_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_data['name'],
            defaults=tag_data
        )
        tags.append(tag)
        if created:
            print(f"✅ Created tag: {tag.name}")
    
    return tags

def create_amenities():
    """Create comprehensive amenities"""
    print("Creating Amenities...")
    
    amenities_data = [
        {
            'name': 'Swimming Pool',
            'font_awesome_icon': 'fas fa-swimmer',
            'description': 'Olympic-size swimming pool with separate kids pool',
            'keywords': 'swimming pool, pool, water sports, recreation',
            'meta_title': 'Swimming Pool Amenity - Resort Style Living',
            'meta_description': 'Enjoy resort-style living with premium swimming pool facilities.'
        },
        {
            'name': 'Fitness Center',
            'font_awesome_icon': 'fas fa-dumbbell',
            'description': 'Fully equipped modern gymnasium with latest equipment',
            'keywords': 'gym, fitness, workout, health, exercise',
            'meta_title': 'Fitness Center - Modern Gym Facilities',
            'meta_description': 'Stay fit with state-of-the-art gym and fitness facilities.'
        },
        {
            'name': 'Clubhouse',
            'font_awesome_icon': 'fas fa-building',
            'description': 'Premium clubhouse for community gatherings and events',
            'keywords': 'clubhouse, community center, events, gatherings',
            'meta_title': 'Clubhouse Amenity - Community Living',
            'meta_description': 'Premium clubhouse facilities for community events and social gatherings.'
        },
        {
            'name': 'Children Play Area',
            'font_awesome_icon': 'fas fa-child',
            'description': 'Safe and fun play area designed for children',
            'keywords': 'kids play area, children playground, family friendly',
            'meta_title': 'Kids Play Area - Family Friendly Living',
            'meta_description': 'Safe and engaging play areas designed specially for children.'
        },
        {
            'name': 'Landscaped Gardens',
            'font_awesome_icon': 'fas fa-leaf',
            'description': 'Beautifully landscaped gardens and green spaces',
            'keywords': 'garden, landscaping, green spaces, nature',
            'meta_title': 'Landscaped Gardens - Green Living Spaces',
            'meta_description': 'Beautiful landscaped gardens and green spaces for peaceful living.'
        },
        {
            'name': '24/7 Security',
            'font_awesome_icon': 'fas fa-shield-alt',
            'description': 'Round-the-clock security with CCTV surveillance',
            'keywords': 'security, safety, cctv, surveillance, protection',
            'meta_title': '24/7 Security - Safe Living Environment',
            'meta_description': 'Complete security with 24/7 surveillance and professional security staff.'
        },
        {
            'name': 'Car Parking',
            'font_awesome_icon': 'fas fa-car',
            'description': 'Covered and open parking spaces for residents',
            'keywords': 'parking, car parking, vehicle parking, covered parking',
            'meta_title': 'Car Parking Facilities - Convenient Parking',
            'meta_description': 'Ample covered and open parking spaces for residents and visitors.'
        },
        {
            'name': 'Power Backup',
            'font_awesome_icon': 'fas fa-bolt',
            'description': '100% power backup for uninterrupted electricity',
            'keywords': 'power backup, generator, electricity, uninterrupted power',
            'meta_title': 'Power Backup - Uninterrupted Electricity',
            'meta_description': 'Complete power backup solutions for uninterrupted electricity supply.'
        },
        {
            'name': 'Elevator',
            'font_awesome_icon': 'fas fa-elevator',
            'description': 'High-speed elevators in all residential blocks',
            'keywords': 'elevator, lift, vertical transportation, modern amenities',
            'meta_title': 'Elevator Facilities - Modern Convenience',
            'meta_description': 'High-speed elevators providing convenient vertical transportation.'
        },
        {
            'name': 'Intercom',
            'font_awesome_icon': 'fas fa-phone',
            'description': 'Video intercom system for enhanced security',
            'keywords': 'intercom, video calling, communication, security',
            'meta_title': 'Intercom System - Enhanced Communication',
            'meta_description': 'Modern video intercom system for secure and convenient communication.'
        },
        {
            'name': 'Jogging Track',
            'font_awesome_icon': 'fas fa-running',
            'description': 'Dedicated jogging track for fitness enthusiasts',
            'keywords': 'jogging track, running, fitness, exercise, health',
            'meta_title': 'Jogging Track - Fitness & Health',
            'meta_description': 'Dedicated jogging track for daily fitness and health activities.'
        },
        {
            'name': 'Tennis Court',
            'font_awesome_icon': 'fas fa-table-tennis',
            'description': 'Professional tennis court for sports activities',
            'keywords': 'tennis court, sports, recreation, tennis, games',
            'meta_title': 'Tennis Court - Sports & Recreation',
            'meta_description': 'Professional tennis court facilities for sports and recreation.'
        },
        {
            'name': 'Basketball Court',
            'font_awesome_icon': 'fas fa-basketball-ball',
            'description': 'Full-size basketball court for team sports',
            'keywords': 'basketball court, sports, recreation, team sports',
            'meta_title': 'Basketball Court - Team Sports Facility',
            'meta_description': 'Full-size basketball court for team sports and recreation activities.'
        },
        {
            'name': 'Spa & Wellness',
            'font_awesome_icon': 'fas fa-spa',
            'description': 'Luxury spa and wellness center for relaxation',
            'keywords': 'spa, wellness, relaxation, massage, therapy',
            'meta_title': 'Spa & Wellness Center - Luxury Relaxation',
            'meta_description': 'Luxury spa and wellness facilities for complete relaxation and rejuvenation.'
        },
        {
            'name': 'Library',
            'font_awesome_icon': 'fas fa-book',
            'description': 'Well-stocked library for reading and study',
            'keywords': 'library, books, reading, study, knowledge',
            'meta_title': 'Library Facility - Reading & Study Space',
            'meta_description': 'Well-equipped library with extensive collection for reading and study.'
        }
    ]
    
    amenities = []
    for amenity_data in amenities_data:
        amenity, created = Amenity.objects.get_or_create(
            name=amenity_data['name'],
            defaults=amenity_data
        )
        amenities.append(amenity)
        if created:
            print(f"✅ Created amenity: {amenity.name}")
    
    return amenities

def create_specification_categories():
    """Create specification categories"""
    print("Creating Specification Categories...")
    
    spec_categories = [
        {'name': 'Flooring', 'order': 1},
        {'name': 'Kitchen', 'order': 2},
        {'name': 'Bathroom', 'order': 3},
        {'name': 'Doors & Windows', 'order': 4},
        {'name': 'Electrical', 'order': 5},
        {'name': 'Plumbing', 'order': 6},
        {'name': 'Safety & Security', 'order': 7},
        {'name': 'Painting', 'order': 8},
    ]
    
    categories = []
    for cat_data in spec_categories:
        category, created = SpecificationCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories.append(category)
        if created:
            print(f"✅ Created specification category: {category.name}")
    
    return categories

def create_comprehensive_projects(cities, categories, project_types, tags, amenities):
    """Create comprehensive project data with all details"""
    print("Creating Comprehensive Projects...")
    
    projects_data = [
        {
            'name': 'Azure Heights Premium',
            'project_by': 'Prestige Group',
            'location': 'Bandra West, Mumbai',
            'city': 'Mumbai',
            'developers': 'Prestige Group',
            'build_up_area': '1200-3500 sq ft',
            'total_area': '8.5 Acres',
            'bhk': '2, 3, 4 BHK',
            'no_of_blocks': 4,
            'tower_count': 4,
            'no_of_units': 320,
            'rera_number': 'P51700000123',
            'status': 'under_construction',
            'possession_date': date(2025, 12, 31),
            'onwards_price': Decimal('12500000'),
            'contact_phone': '+91 9876543210',
            'contact_email': 'sales@azureheights.com',
            'sales_office_address': 'Plot No. 45, Bandra West, Mumbai - 400050',
            'latitude': Decimal('19.0596'),
            'longitude': Decimal('72.8295'),
            'category': 'Residential',
            'project_type': 'Luxury Apartments',
            'tags': ['Premium', 'Trending', 'Under Construction'],
            'amenities': ['Swimming Pool', 'Fitness Center', 'Clubhouse', '24/7 Security', 'Car Parking'],
            'trending_tag': 'premium',
            'is_most_viewed': True,
            'is_featured': True,
            'is_hot_deal': True,
            'description': 'Azure Heights Premium offers luxury living in the heart of Mumbai with world-class amenities and stunning city views.',
            'keywords': 'luxury apartments mumbai, bandra west properties, premium residential',
            'meta_title': 'Azure Heights Premium - Luxury Apartments in Bandra West Mumbai',
            'meta_description': 'Discover luxury living at Azure Heights Premium in Bandra West. Premium 2, 3, 4 BHK apartments with world-class amenities.',
            'overview_title': 'Experience Luxury Living in Mumbai',
            'overview_description': 'Azure Heights Premium redefines luxury living with its sophisticated design, premium amenities, and prime location in Bandra West. Experience unparalleled comfort and convenience in the heart of Mumbai.'
        },
        {
            'name': 'Green Valley Residences',
            'project_by': 'DLF Limited',
            'location': 'Sector 18, Noida',
            'city': 'Delhi',
            'developers': 'DLF Limited',
            'build_up_area': '900-2200 sq ft',
            'total_area': '12.3 Acres',
            'bhk': '1, 2, 3 BHK',
            'no_of_blocks': 6,
            'tower_count': 6,
            'no_of_units': 485,
            'rera_number': 'UPRERAPRJ123456',
            'status': 'ready_to_move',
            'possession_date': date(2024, 6, 30),
            'onwards_price': Decimal('6500000'),
            'contact_phone': '+91 9876543211',
            'contact_email': 'info@greenvalley.com',
            'sales_office_address': 'Plot No. 18-A, Sector 18, Noida - 201301',
            'latitude': Decimal('28.5355'),
            'longitude': Decimal('77.3910'),
            'category': 'Residential',
            'project_type': 'Budget Apartments',
            'tags': ['Ready to Move', 'Best Value', 'Investment Grade'],
            'amenities': ['Landscaped Gardens', 'Children Play Area', 'Car Parking', 'Power Backup', 'Elevator'],
            'trending_tag': 'ready_to_move',
            'is_most_viewed': False,
            'is_featured': True,
            'is_nearby_property': True,
            'description': 'Green Valley Residences offers affordable luxury in Noida with excellent connectivity and modern amenities.',
            'keywords': 'affordable apartments noida, ready to move flats, budget housing',
            'meta_title': 'Green Valley Residences - Ready to Move Apartments in Noida',
            'meta_description': 'Move into your dream home at Green Valley Residences Noida. Ready to move 1, 2, 3 BHK apartments with modern amenities.',
            'overview_title': 'Ready to Move Homes in Prime Noida Location',
            'overview_description': 'Green Valley Residences offers ready-to-move affordable luxury apartments in the heart of Noida with excellent connectivity to Delhi and other NCR cities.'
        },
        {
            'name': 'TechCity Corporate Hub',
            'project_by': 'Brigade Group',
            'location': 'Electronic City, Bangalore',
            'city': 'Bangalore',
            'developers': 'Brigade Group',
            'build_up_area': '500-5000 sq ft',
            'total_area': '15.2 Acres',
            'bhk': 'Office Spaces',
            'no_of_blocks': 3,
            'tower_count': 3,
            'no_of_units': 250,
            'rera_number': 'PRM/KA/RERA/123456',
            'status': 'under_construction',
            'possession_date': date(2026, 3, 31),
            'onwards_price': Decimal('8500000'),
            'contact_phone': '+91 9876543212',
            'contact_email': 'leasing@techcity.com',
            'sales_office_address': 'Electronic City Phase 1, Bangalore - 560100',
            'latitude': Decimal('12.8456'),
            'longitude': Decimal('77.6603'),
            'category': 'Commercial',
            'project_type': 'IT Parks',
            'tags': ['New Launch', 'Premium', 'Investment Grade'],
            'amenities': ['Business Centers', '24/7 Security', 'Car Parking', 'Power Backup', 'Elevator'],
            'trending_tag': 'just_launched',
            'is_most_viewed': True,
            'is_featured': True,
            'is_premium_listing': True,
            'description': 'TechCity Corporate Hub is a premium IT park in Electronic City designed for modern businesses.',
            'keywords': 'it park bangalore, office space electronic city, commercial property',
            'meta_title': 'TechCity Corporate Hub - Premium IT Park in Electronic City Bangalore',
            'meta_description': 'Invest in TechCity Corporate Hub, a premium IT park in Electronic City. Modern office spaces for growing businesses.',
            'overview_title': 'Modern Corporate Spaces in IT Hub',
            'overview_description': 'TechCity Corporate Hub offers state-of-the-art office spaces in Electronic City, Bangalore\'s premier IT destination. Perfect for startups and established businesses.'
        },
        {
            'name': 'Royal Gardens Villa Estate',
            'project_by': 'Godrej Properties',
            'location': 'Kondapur, Hyderabad',
            'city': 'Hyderabad',
            'developers': 'Godrej Properties',
            'build_up_area': '2500-4500 sq ft',
            'total_area': '25.7 Acres',
            'bhk': '3, 4, 5 BHK Villas',
            'no_of_blocks': 1,
            'tower_count': 0,
            'no_of_units': 156,
            'rera_number': 'P02400000456',
            'status': 'under_construction',
            'possession_date': date(2025, 9, 30),
            'onwards_price': Decimal('18500000'),
            'contact_phone': '+91 9876543213',
            'contact_email': 'villas@royalgardens.com',
            'sales_office_address': 'Survey No. 123, Kondapur, Hyderabad - 500084',
            'latitude': Decimal('17.4569'),
            'longitude': Decimal('78.3677'),
            'category': 'Residential',
            'project_type': 'Premium Villas',
            'tags': ['Luxury', 'Premium', 'Limited Offer'],
            'amenities': ['Swimming Pool', 'Tennis Court', 'Clubhouse', 'Landscaped Gardens', 'Spa & Wellness'],
            'trending_tag': 'ultra_luxury',
            'is_most_viewed': True,
            'is_featured': True,
            'is_editors_choice': True,
            'description': 'Royal Gardens Villa Estate offers ultra-luxury independent villas in the prestigious Kondapur area.',
            'keywords': 'luxury villas hyderabad, kondapur properties, independent houses',
            'meta_title': 'Royal Gardens Villa Estate - Luxury Villas in Kondapur Hyderabad',
            'meta_description': 'Experience luxury at Royal Gardens Villa Estate. Premium 3, 4, 5 BHK independent villas in Kondapur, Hyderabad.',
            'overview_title': 'Ultra-Luxury Independent Villas',
            'overview_description': 'Royal Gardens Villa Estate presents an exclusive collection of ultra-luxury independent villas in Kondapur, designed for those who appreciate the finest things in life.'
        },
        {
            'name': 'Sunshine Apartments',
            'project_by': 'Tata Housing',
            'location': 'OMR, Chennai',
            'city': 'Chennai',
            'developers': 'Tata Housing',
            'build_up_area': '800-1800 sq ft',
            'total_area': '6.8 Acres',
            'bhk': '1, 2, 3 BHK',
            'no_of_blocks': 5,
            'tower_count': 5,
            'no_of_units': 380,
            'rera_number': 'TN/04/Building/456789',
            'status': 'ready_to_move',
            'possession_date': date(2024, 3, 31),
            'onwards_price': Decimal('4500000'),
            'contact_phone': '+91 9876543214',
            'contact_email': 'sales@sunshine.com',
            'sales_office_address': 'OMR Road, Perungudi, Chennai - 600096',
            'latitude': Decimal('12.9601'),
            'longitude': Decimal('80.2206'),
            'category': 'Residential',
            'project_type': 'Budget Apartments',
            'tags': ['Ready to Move', 'Best Value', 'Hot Deal'],
            'amenities': ['Swimming Pool', 'Children Play Area', 'Fitness Center', 'Car Parking', 'Intercom'],
            'trending_tag': 'affordable',
            'is_most_viewed': False,
            'is_featured': False,
            'is_hot_deal': True,
            'description': 'Sunshine Apartments offers value-for-money homes in Chennai with excellent connectivity to IT corridors.',
            'keywords': 'apartments chennai omr, affordable flats, ready possession',
            'meta_title': 'Sunshine Apartments - Affordable Flats on OMR Chennai',
            'meta_description': 'Find your perfect home at Sunshine Apartments on OMR. Ready to move 1, 2, 3 BHK apartments at affordable prices.',
            'overview_title': 'Affordable Homes with Premium Amenities',
            'overview_description': 'Sunshine Apartments on OMR offers the perfect blend of affordability and comfort with ready-to-move homes and excellent connectivity to Chennai\'s IT hubs.'
        },
        {
            'name': 'Elegant Towers',
            'project_by': 'Mahindra Lifespace',
            'location': 'Hinjewadi, Pune',
            'city': 'Pune',
            'developers': 'Mahindra Lifespace',
            'build_up_area': '650-1500 sq ft',
            'total_area': '4.2 Acres',
            'bhk': '1, 2, 3 BHK',
            'no_of_blocks': 3,
            'tower_count': 3,
            'no_of_units': 285,
            'rera_number': 'P52100012345',
            'status': 'under_construction',
            'possession_date': date(2025, 8, 31),
            'onwards_price': Decimal('5500000'),
            'contact_phone': '+91 9876543215',
            'contact_email': 'info@eleganttowers.com',
            'sales_office_address': 'Hinjewadi Phase 1, Pune - 411057',
            'latitude': Decimal('18.5912'),
            'longitude': Decimal('73.7389'),
            'category': 'Residential',
            'project_type': 'Luxury Apartments',
            'tags': ['Trending', 'Under Construction', 'Investment Grade'],
            'amenities': ['Jogging Track', 'Basketball Court', 'Library', 'Landscaped Gardens', 'Power Backup'],
            'trending_tag': 'just_launched',
            'is_most_viewed': True,
            'is_featured': True,
            'is_recently_viewed': True,
            'description': 'Elegant Towers in Hinjewadi offers modern living with proximity to major IT companies and excellent infrastructure.',
            'keywords': 'apartments pune hinjewadi, it hub flats, modern amenities',
            'meta_title': 'Elegant Towers - Modern Apartments in Hinjewadi Pune',
            'meta_description': 'Discover modern living at Elegant Towers Hinjewadi. Well-designed 1, 2, 3 BHK apartments near IT hubs.',
            'overview_title': 'Modern Living in IT Hub',
            'overview_description': 'Elegant Towers offers contemporary living spaces in Hinjewadi, Pune\'s premier IT destination, with easy access to major companies and urban conveniences.'
        }
    ]
    
    # Create mapping dictionaries
    city_map = {city.name: city for city in cities}
    category_map = {cat.name: cat for cat in categories}
    project_type_map = {pt.name: pt for pt in project_types}
    tag_map = {tag.name: tag for tag in tags}
    amenity_map = {amenity.name: amenity for amenity in amenities}
    
    projects = []
    for project_data in projects_data:
        # Extract and remove complex fields
        city_name = project_data.pop('city')
        category_name = project_data.pop('category')
        project_type_name = project_data.pop('project_type')
        tag_names = project_data.pop('tags', [])
        amenity_names = project_data.pop('amenities', [])
        overview_title = project_data.pop('overview_title', '')
        overview_description = project_data.pop('overview_description', '')
        
        # Create project
        project, created = Project.objects.get_or_create(
            name=project_data['name'],
            defaults={
                **project_data,
                'city': city_map[city_name],
                'category': category_map[category_name],
                'project_type': project_type_map[project_type_name],
            }
        )
        
        if created:
            print(f"✅ Created project: {project.name}")
            
            # Add tags
            for tag_name in tag_names:
                if tag_name in tag_map:
                    project.tags.add(tag_map[tag_name])
            
            # Add amenities
            for amenity_name in amenity_names:
                if amenity_name in amenity_map:
                    project.amenities.add(amenity_map[amenity_name])
            
            # Create project overview
            if overview_title or overview_description:
                ProjectOverview.objects.create(
                    project=project,
                    title=overview_title,
                    short_description=overview_description
                )
                print(f"  ✅ Created overview for: {project.name}")
        
        projects.append(project)
    
    return projects

def create_detailed_project_data(projects, amenities):
    """Add detailed data to projects"""
    print("Adding detailed project data...")
    
    # Sample nearby areas
    nearby_areas_data = [
        {'name': 'International School', 'area_type': 'school', 'distance': '500m'},
        {'name': 'Apollo Hospital', 'area_type': 'hospital', 'distance': '1.2km'},
        {'name': 'Metro Station', 'area_type': 'metro', 'distance': '800m'},
        {'name': 'Phoenix Mall', 'area_type': 'mall', 'distance': '2km'},
        {'name': 'Central Park', 'area_type': 'park', 'distance': '300m'},
        {'name': 'HDFC Bank', 'area_type': 'bank', 'distance': '400m'},
        {'name': 'Gold\'s Gym', 'area_type': 'gym', 'distance': '600m'},
    ]
    
    # Sample floor plans
    floor_plans_data = [
        {'name': '2BHK East Facing', 'area': '1200 sq ft', 'price': Decimal('8500000')},
        {'name': '3BHK West Facing', 'area': '1650 sq ft', 'price': Decimal('12500000')},
        {'name': '4BHK Corner Unit', 'area': '2200 sq ft', 'price': Decimal('18500000')},
    ]
    
    # Sample why choose us points
    why_choose_data = [
        {'title': 'Prime Location', 'description': 'Located in the heart of the city with excellent connectivity', 'icon': 'fas fa-map-marker-alt'},
        {'title': 'World-Class Amenities', 'description': 'Premium amenities designed for modern lifestyle', 'icon': 'fas fa-star'},
        {'title': 'Trusted Developer', 'description': 'Built by renowned developers with proven track record', 'icon': 'fas fa-award'},
        {'title': 'Investment Value', 'description': 'Excellent appreciation potential and rental yields', 'icon': 'fas fa-chart-line'},
    ]
    
    # Sample specifications
    spec_data = [
        {'category': 'Flooring', 'items': [
            {'name': 'Living & Dining', 'description': 'Premium vitrified tiles'},
            {'name': 'Bedrooms', 'description': 'Laminated wooden flooring'},
            {'name': 'Kitchen', 'description': 'Anti-skid ceramic tiles'},
            {'name': 'Bathrooms', 'description': 'Anti-skid ceramic tiles'},
        ]},
        {'category': 'Kitchen', 'items': [
            {'name': 'Cabinets', 'description': 'Modular kitchen with granite countertop'},
            {'name': 'Appliances', 'description': 'Provision for chimney and hob'},
            {'name': 'Sink', 'description': 'Stainless steel sink with faucet'},
        ]},
        {'category': 'Bathroom', 'items': [
            {'name': 'Fixtures', 'description': 'Premium CP fittings'},
            {'name': 'Sanitary', 'description': 'Branded sanitary ware'},
            {'name': 'Hot Water', 'description': 'Solar water heating system'},
        ]},
    ]
    
    spec_categories = create_specification_categories()
    spec_category_map = {cat.name: cat for cat in spec_categories}
    
    for project in projects[:3]:  # Add details to first 3 projects
        print(f"Adding details to: {project.name}")
        
        # Add nearby areas
        for i, area_data in enumerate(nearby_areas_data[:5]):  # Add 5 areas per project
            NearestArea.objects.get_or_create(
                project=project,
                name=area_data['name'],
                area_type=area_data['area_type'],
                defaults={'distance': area_data['distance']}
            )
        
        # Add floor plans
        for i, plan_data in enumerate(floor_plans_data):
            FloorPlan.objects.get_or_create(
                project=project,
                name=plan_data['name'],
                defaults={
                    'area': plan_data['area'],
                    'price': plan_data['price'],
                    'order': i
                }
            )
        
        # Add why choose us points
        for i, why_data in enumerate(why_choose_data):
            WhyChooseUs.objects.get_or_create(
                project=project,
                title=why_data['title'],
                defaults={
                    'description': why_data['description'],
                    'icon': why_data['icon'],
                    'order': i
                }
            )
        
        # Add specifications
        for spec_cat_data in spec_data:
            if spec_cat_data['category'] in spec_category_map:
                category = spec_category_map[spec_cat_data['category']]
                for item_data in spec_cat_data['items']:
                    SpecificationItem.objects.get_or_create(
                        project=project,
                        category=category,
                        name=item_data['name'],
                        defaults={'description': item_data['description']}
                    )
        
        # Add construction updates
        for i in range(3):
            update_date = date.today() - timedelta(days=30 * (i + 1))
            ConstructionUpdate.objects.get_or_create(
                project=project,
                update_date=update_date,
                defaults={
                    'title': f'Construction Progress - Month {3-i}',
                    'description': f'Construction update for {project.name} showing excellent progress.',
                    'order': i
                }
            )

def create_blog_content():
    """Create blog content"""
    print("Creating Blog Content...")
    
    # Create blog tags
    blog_tags_data = [
        'Real Estate', 'Investment', 'Home Buying', 'Property Tips', 
        'Market Trends', 'Luxury Homes', 'Commercial Property'
    ]
    
    blog_tags = []
    for tag_name in blog_tags_data:
        tag, created = BlogTag.objects.get_or_create(name=tag_name)
        blog_tags.append(tag)
        if created:
            print(f"✅ Created blog tag: {tag.name}")
    
    # Create blogs
    blogs_data = [
        {
            'title': 'Top 10 Tips for First-Time Home Buyers in 2025',
            'content': '''<p>Buying your first home is an exciting milestone, but it can also be overwhelming. Here are the top 10 tips to help you navigate the home buying process successfully:</p>
            
            <h3>1. Determine Your Budget</h3>
            <p>Before you start looking at properties, it's crucial to understand what you can afford. Consider your income, expenses, and savings to determine a realistic budget.</p>
            
            <h3>2. Get Pre-approved for a Loan</h3>
            <p>Getting pre-approved shows sellers that you're serious and gives you a clear picture of your buying power.</p>
            
            <h3>3. Research Neighborhoods</h3>
            <p>Location is everything in real estate. Research different neighborhoods, considering factors like schools, amenities, and future development plans.</p>''',
            'meta_title': 'Top 10 Tips for First-Time Home Buyers in 2025 - Complete Guide',
            'meta_description': 'Essential tips for first-time home buyers in 2025. Learn about budgeting, loan approval, and choosing the right property.',
            'tags': ['Home Buying', 'Property Tips']
        },
        {
            'title': 'Real Estate Investment Opportunities in Tier 2 Cities',
            'content': '''<p>While metro cities have traditionally been the focus of real estate investment, Tier 2 cities are emerging as attractive investment destinations. Here's why:</p>
            
            <h3>Growing Infrastructure</h3>
            <p>Government initiatives and private investments are rapidly improving infrastructure in Tier 2 cities, making them more attractive for both residents and businesses.</p>
            
            <h3>Affordable Property Prices</h3>
            <p>Property prices in Tier 2 cities are significantly lower than metro cities, offering better value for money and higher rental yields.</p>
            
            <h3>Employment Opportunities</h3>
            <p>Many companies are expanding to Tier 2 cities, creating employment opportunities and driving demand for quality housing.</p>''',
            'meta_title': 'Real Estate Investment in Tier 2 Cities - Opportunities & Benefits',
            'meta_description': 'Explore real estate investment opportunities in Tier 2 cities. Discover why these markets offer excellent potential for investors.',
            'tags': ['Investment', 'Market Trends']
        },
        {
            'title': 'Luxury Real Estate Market Trends 2025',
            'content': '''<p>The luxury real estate market continues to evolve with changing buyer preferences and new trends. Here's what's shaping the market in 2025:</p>
            
            <h3>Sustainable Luxury</h3>
            <p>High-net-worth individuals are increasingly seeking properties that combine luxury with sustainability. Green buildings and eco-friendly features are in high demand.</p>
            
            <h3>Smart Home Technology</h3>
            <p>Luxury buyers expect state-of-the-art smart home technology, from automated lighting and climate control to advanced security systems.</p>
            
            <h3>Wellness-Focused Amenities</h3>
            <p>Post-pandemic preferences have shifted towards wellness-focused amenities like spa facilities, meditation spaces, and air purification systems.</p>''',
            'meta_title': 'Luxury Real Estate Market Trends 2025 - What High-End Buyers Want',
            'meta_description': 'Latest trends in luxury real estate for 2025. Discover what high-end buyers are looking for in premium properties.',
            'tags': ['Luxury Homes', 'Market Trends']
        }
    ]
    
    tag_map = {tag.name: tag for tag in blog_tags}
    
    for blog_data in blogs_data:
        tag_names = blog_data.pop('tags', [])
        
        blog, created = Blog.objects.get_or_create(
            title=blog_data['title'],
            defaults=blog_data
        )
        
        if created:
            print(f"✅ Created blog: {blog.title}")
            
            # Add tags
            for tag_name in tag_names:
                if tag_name in tag_map:
                    blog.tags.add(tag_map[tag_name])

def create_career_opportunities():
    """Create career opportunities"""
    print("Creating Career Opportunities...")
    
    careers_data = [
        {
            'title': 'Senior Sales Manager - Residential Properties',
            'location': 'Mumbai, Maharashtra',
            'description': '''We are looking for an experienced Senior Sales Manager to lead our residential property sales team. The ideal candidate will have 5+ years of experience in real estate sales and a proven track record of achieving targets.

Responsibilities:
• Lead and manage the sales team
• Develop sales strategies and marketing plans
• Build relationships with potential clients
• Achieve monthly and quarterly sales targets
• Provide market insights and feedback

Requirements:
• Bachelor's degree in Business, Marketing, or related field
• 5+ years of experience in real estate sales
• Strong leadership and communication skills
• Knowledge of local real estate market
• Proven track record of achieving sales targets''',
        },
        {
            'title': 'Digital Marketing Specialist',
            'location': 'Bangalore, Karnataka',
            'description': '''Join our dynamic marketing team as a Digital Marketing Specialist. You'll be responsible for developing and executing digital marketing campaigns to promote our real estate projects.

Responsibilities:
• Develop and implement digital marketing strategies
• Manage social media platforms and content
• Create and optimize digital advertising campaigns
• Analyze campaign performance and provide insights
• Collaborate with design and content teams

Requirements:
• Bachelor's degree in Marketing, Communications, or related field
• 2+ years of experience in digital marketing
• Proficiency in Google Ads, Facebook Ads, and analytics tools
• Strong analytical and creative thinking skills
• Knowledge of real estate marketing preferred''',
        },
        {
            'title': 'Project Manager - Construction',
            'location': 'Delhi NCR',
            'description': '''We are seeking an experienced Project Manager to oversee our construction projects from inception to completion. The role requires strong project management skills and construction industry knowledge.

Responsibilities:
• Plan, execute, and monitor construction projects
• Coordinate with contractors, suppliers, and stakeholders
• Ensure projects are completed on time and within budget
• Maintain quality standards and safety protocols
• Prepare project reports and documentation

Requirements:
• Bachelor's degree in Civil Engineering or Construction Management
• 7+ years of experience in construction project management
• PMP certification preferred
• Strong leadership and communication skills
• Knowledge of construction regulations and safety standards''',
        }
    ]
    
    for career_data in careers_data:
        career, created = Career.objects.get_or_create(
            title=career_data['title'],
            defaults=career_data
        )
        
        if created:
            print(f"✅ Created career: {career.title}")

def create_sample_leads():
    """Create sample leads for testing"""
    print("Creating Sample Leads...")
    
    # Investment leads
    investment_leads_data = [
        {
            'name': 'Rajesh Kumar',
            'email': 'rajesh.kumar@example.com',
            'contact_number': '+91 9876543210',
            'location': 'Mumbai',
            'budget': '₹50-75 Lakhs',
            'requirement_type': 'residential',
            'how_did_you_know': 'google',
            'agreed_to_terms': True
        },
        {
            'name': 'Priya Sharma',
            'email': 'priya.sharma@example.com',
            'contact_number': '+91 9876543211',
            'location': 'Bangalore',
            'budget': '₹1-2 Crores',
            'requirement_type': 'commercial',
            'how_did_you_know': 'referral',
            'agreed_to_terms': True
        },
        {
            'name': 'Sunil Gupta',
            'email': 'sunil.gupta@example.com',
            'contact_number': '+91 9876543212',
            'location': 'Delhi',
            'budget': '₹80 Lakhs - ₹1 Crore',
            'requirement_type': 'residential',
            'how_did_you_know': 'facebook',
            'agreed_to_terms': True
        }
    ]
    
    for lead_data in investment_leads_data:
        lead, created = InvestmentRequirement.objects.get_or_create(
            email=lead_data['email'],
            defaults=lead_data
        )
        
        if created:
            print(f"✅ Created investment lead: {lead.name}")
    
    # Land leads
    land_leads_data = [
        {
            'name': 'Amit Patel',
            'email': 'amit.patel@example.com',
            'contact_number': '+91 9876543213',
            'location': 'Ahmedabad',
            'budget': '₹80-120 Lakhs',
            'area': Decimal('1.5'),
            'area_unit': 'acre',
            'requirement_type': 'buy',
            'status': 'new',
            'agreed_to_terms': True
        },
        {
            'name': 'Suresh Reddy',
            'email': 'suresh.reddy@example.com',
            'contact_number': '+91 9876543214',
            'location': 'Hyderabad',
            'budget': '₹30-50 Lakhs',
            'area': Decimal('0.25'),
            'area_unit': 'acre',
            'requirement_type': 'buy',
            'status': 'new',
            'agreed_to_terms': True
        },
        {
            'name': 'Kavita Singh',
            'email': 'kavita.singh@example.com',
            'contact_number': '+91 9876543215',
            'location': 'Pune',
            'budget': '₹2-3 Crores',
            'area': Decimal('5.0'),
            'area_unit': 'acre',
            'requirement_type': 'joint_venture',
            'status': 'new',
            'agreed_to_terms': True
        }
    ]
    
    for lead_data in land_leads_data:
        lead, created = LandRequirement.objects.get_or_create(
            email=lead_data['email'],
            defaults=lead_data
        )
        
        if created:
            print(f"✅ Created land lead: {lead.name}")

def main():
    """Main function to create all demo data"""
    print("🚀 Starting Comprehensive Demo Data Creation...")
    print("=" * 60)
    
    try:
        # Create basic data
        cities = create_cities()
        categories = create_categories()
        project_types = create_project_types(categories)
        tags = create_tags()
        amenities = create_amenities()
        
        # Create comprehensive projects
        projects = create_comprehensive_projects(cities, categories, project_types, tags, amenities)
        
        # Add detailed project data
        create_detailed_project_data(projects, amenities)
        
        # Create content
        create_blog_content()
        create_career_opportunities()
        create_sample_leads()
        
        print("=" * 60)
        print("✅ DEMO DATA CREATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Summary:")
        print(f"📍 Cities: {len(cities)}")
        print(f"📂 Categories: {len(categories)}")
        print(f"🏢 Project Types: {len(project_types)}")
        print(f"🏷️ Tags: {len(tags)}")
        print(f"🏊 Amenities: {len(amenities)}")
        print(f"🏗️ Projects: {len(projects)}")
        print(f"📝 Blogs: {Blog.objects.count()}")
        print(f"💼 Careers: {Career.objects.count()}")
        print("=" * 60)
        print("🎉 Your Django Real Estate application is now ready with comprehensive demo data!")
        print("👤 Admin Login: admin / 123 (or your chosen password)")
        print("🌐 Run 'python manage.py runserver' to start the application")
        
    except Exception as e:
        print(f"❌ Error creating demo data: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
