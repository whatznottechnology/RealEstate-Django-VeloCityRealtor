#!/usr/bin/env python
"""
Create ONE Complete Project with ALL Fields Properly Filled
This will clean the database and create a single comprehensive project for testing.
"""

import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta

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
from django.contrib.auth.models import User

def clean_database():
    """Clean all existing data"""
    print("🧹 Cleaning Database...")
    
    # Delete all data in proper order
    ProjectAmenityImage.objects.all().delete()
    SpecificationItem.objects.all().delete()
    SpecificationCategory.objects.all().delete()
    WhyChooseUs.objects.all().delete()
    ConstructionUpdate.objects.all().delete()
    FloorPlan.objects.all().delete()
    NearestArea.objects.all().delete()
    GalleryImage.objects.all().delete()
    ProjectOverview.objects.all().delete()
    Project.objects.all().delete()
    
    ProjectType.objects.all().delete()
    Category.objects.all().delete()
    City.objects.all().delete()
    Tag.objects.all().delete()
    Amenity.objects.all().delete()
    
    Blog.objects.all().delete()
    BlogTag.objects.all().delete()
    Career.objects.all().delete()
    InvestmentRequirement.objects.all().delete()
    LandRequirement.objects.all().delete()
    
    print("✅ Database cleaned successfully!")

def create_basic_data():
    """Create basic required data"""
    print("📝 Creating Basic Data...")
    
    # Create City
    city = City.objects.create(
        name='Mumbai',
        state='Maharashtra',
        country='India',
        description='Financial capital of India with premium real estate opportunities and excellent infrastructure. Known for its vibrant culture, business opportunities, and world-class amenities.',
        keywords='mumbai, maharashtra, real estate, properties, apartments, financial capital, premium location',
        meta_title='Real Estate Properties in Mumbai, Maharashtra - Premium Locations',
        meta_description='Find premium real estate properties in Mumbai, the financial capital of India. Residential and commercial projects with world-class amenities and excellent connectivity.',
        is_active=True
    )
    print(f"✅ Created city: {city.name}")
    
    # Create Category
    category = Category.objects.create(
        name='Residential',
        description='Premium residential properties including luxury apartments, villas, and integrated townships designed for modern living with world-class amenities and excellent connectivity.',
        keywords='residential, apartments, villas, homes, luxury living, premium properties',
        meta_title='Residential Properties - Luxury Apartments & Premium Villas',
        meta_description='Discover premium residential properties including luxury apartments and villas. Modern homes with world-class amenities in prime locations.'
    )
    print(f"✅ Created category: {category.name}")
    
    # Create Project Type
    project_type = ProjectType.objects.create(
        name='Luxury Apartments',
        category=category,
        description='Ultra-luxury apartments designed for sophisticated living with premium finishes, modern amenities, and strategic locations offering excellent connectivity and lifestyle benefits.',
        keywords='luxury apartments, premium flats, high-end residential, sophisticated living',
        meta_title='Luxury Apartments - Premium Residential Properties',
        meta_description='Experience sophisticated living in our luxury apartments. Premium residential properties with world-class amenities and modern design.'
    )
    print(f"✅ Created project type: {project_type.name}")
    
    # Create Tags
    tags_data = [
        {'name': 'Premium', 'color': '#3742fa'},
        {'name': 'Luxury', 'color': '#8e44ad'},
        {'name': 'Trending', 'color': '#ff6b6b'},
        {'name': 'Under Construction', 'color': '#ffa502'},
        {'name': 'Investment Grade', 'color': '#2f3542'},
    ]
    
    tags = []
    for tag_data in tags_data:
        tag = Tag.objects.create(**tag_data)
        tags.append(tag)
        print(f"✅ Created tag: {tag.name}")
    
    # Create Amenities
    amenities_data = [
        {
            'name': 'Swimming Pool',
            'font_awesome_icon': 'fas fa-swimmer',
            'description': 'Olympic-size swimming pool with separate kids pool, pool deck, and professional lifeguard services',
            'keywords': 'swimming pool, pool, water sports, recreation, olympic size',
            'meta_title': 'Swimming Pool Amenity - Resort Style Living',
            'meta_description': 'Enjoy resort-style living with our premium Olympic-size swimming pool facilities including kids pool and professional services.'
        },
        {
            'name': 'Fitness Center',
            'font_awesome_icon': 'fas fa-dumbbell',
            'description': 'State-of-the-art fitness center with latest equipment, personal trainers, and separate areas for cardio and strength training',
            'keywords': 'gym, fitness, workout, health, exercise, personal trainer',
            'meta_title': 'Fitness Center - Modern Gym Facilities',
            'meta_description': 'Stay fit with our state-of-the-art fitness center featuring latest equipment and professional personal training services.'
        },
        {
            'name': 'Clubhouse',
            'font_awesome_icon': 'fas fa-building',
            'description': 'Premium clubhouse with party halls, meeting rooms, library, indoor games, and business center facilities',
            'keywords': 'clubhouse, community center, events, gatherings, party hall',
            'meta_title': 'Clubhouse Amenity - Community Living',
            'meta_description': 'Premium clubhouse facilities for community events, business meetings, and social gatherings with modern amenities.'
        },
        {
            'name': 'Landscaped Gardens',
            'font_awesome_icon': 'fas fa-leaf',
            'description': 'Beautifully landscaped gardens with walking paths, meditation areas, and variety of flora designed by landscape architects',
            'keywords': 'garden, landscaping, green spaces, nature, meditation, walking',
            'meta_title': 'Landscaped Gardens - Green Living Spaces',
            'meta_description': 'Beautiful landscaped gardens with walking paths and meditation areas designed for peaceful and green living.'
        },
        {
            'name': '24/7 Security',
            'font_awesome_icon': 'fas fa-shield-alt',
            'description': 'Round-the-clock multi-tier security with trained guards, CCTV surveillance, access control, and emergency response',
            'keywords': 'security, safety, cctv, surveillance, protection, emergency',
            'meta_title': '24/7 Security - Safe Living Environment',
            'meta_description': 'Complete security with 24/7 surveillance, trained security staff, and modern access control systems for safe living.'
        },
        {
            'name': 'Car Parking',
            'font_awesome_icon': 'fas fa-car',
            'description': 'Multi-level covered parking with designated spaces, visitor parking, EV charging stations, and valet services',
            'keywords': 'parking, car parking, vehicle parking, covered parking, EV charging',
            'meta_title': 'Car Parking Facilities - Convenient Parking Solutions',
            'meta_description': 'Comprehensive parking solutions with covered spaces, visitor parking, and modern EV charging facilities.'
        },
    ]
    
    amenities = []
    for amenity_data in amenities_data:
        amenity = Amenity.objects.create(**amenity_data)
        amenities.append(amenity)
        print(f"✅ Created amenity: {amenity.name}")
    
    # Create Specification Categories
    spec_categories_data = [
        {'name': 'Flooring', 'order': 1},
        {'name': 'Kitchen', 'order': 2},
        {'name': 'Bathroom', 'order': 3},
        {'name': 'Doors & Windows', 'order': 4},
        {'name': 'Electrical', 'order': 5},
        {'name': 'Plumbing', 'order': 6},
        {'name': 'Safety & Security', 'order': 7},
        {'name': 'Painting', 'order': 8},
    ]
    
    spec_categories = []
    for spec_data in spec_categories_data:
        spec_category = SpecificationCategory.objects.create(**spec_data)
        spec_categories.append(spec_category)
        print(f"✅ Created specification category: {spec_category.name}")
    
    return {
        'city': city,
        'category': category,
        'project_type': project_type,
        'tags': tags,
        'amenities': amenities,
        'spec_categories': spec_categories
    }

def create_complete_project(basic_data):
    """Create one complete project with all fields"""
    print("🏗️ Creating Complete Project...")
    
    # Create the main project
    project = Project.objects.create(
        name='Azure Heights Premium',
        project_by='Prestige Group',
        location='Bandra West, Mumbai',
        city=basic_data['city'],
        category=basic_data['category'],
        project_type=basic_data['project_type'],
        developers='Prestige Group - Leading real estate developer with 30+ years of experience',
        build_up_area='1200-3500 sq ft',
        total_area='8.5 Acres',
        bhk='2, 3, 4 BHK',
        no_of_blocks=4,
        tower_count=4,
        no_of_units=320,
        rera_number='P51700000123',
        status='under_construction',
        possession_date=date(2025, 12, 31),
        onwards_price=Decimal('12500000'),
        contact_phone='+91 9876543210',
        contact_email='sales@azureheights.com',
        sales_office_address='Plot No. 45, Linking Road, Bandra West, Mumbai - 400050, Maharashtra, India',
        latitude=Decimal('19.0596'),
        longitude=Decimal('72.8295'),
        trending_tag='premium',
        is_most_viewed=True,
        is_featured=True,
        is_hot_deal=True,
        is_premium_listing=True,
        is_editors_choice=True,
        description='''Azure Heights Premium represents the pinnacle of luxury living in Mumbai's prestigious Bandra West. This architectural masterpiece combines contemporary design with traditional elegance, offering spacious 2, 3, and 4 BHK apartments with stunning city and sea views.

Located in the heart of Bandra West, residents enjoy unparalleled connectivity to business districts, entertainment hubs, and transportation networks. The project features world-class amenities including an Olympic-size swimming pool, state-of-the-art fitness center, premium clubhouse, and beautifully landscaped gardens.

With meticulous attention to detail and premium finishes throughout, Azure Heights Premium sets new standards for luxury residential living in Mumbai. Experience the perfect blend of comfort, convenience, and sophistication in one of Mumbai's most sought-after locations.''',
        keywords='azure heights, luxury apartments mumbai, bandra west properties, premium residential, prestige group, sea view apartments, luxury living mumbai',
        meta_title='Azure Heights Premium - Luxury 2,3,4 BHK Apartments in Bandra West Mumbai by Prestige Group',
        meta_description='Discover ultimate luxury at Azure Heights Premium in Bandra West. Premium 2,3,4 BHK apartments by Prestige Group with world-class amenities, sea views, and excellent connectivity. RERA: P51700000123'
    )
    
    # Add tags
    for tag in basic_data['tags']:
        project.tags.add(tag)
    
    # Add amenities
    for amenity in basic_data['amenities']:
        project.amenities.add(amenity)
    
    print(f"✅ Created project: {project.name}")
    
    # Create Project Overview
    overview = ProjectOverview.objects.create(
        project=project,
        title='Experience Luxury Living in Mumbai\'s Premier Location',
        short_description='''Azure Heights Premium redefines luxury living with its sophisticated design, premium amenities, and prime location in Bandra West. Experience unparalleled comfort and convenience in the heart of Mumbai's most prestigious neighborhood.'''
    )
    print(f"✅ Created project overview")
    
    # Create Nearest Areas
    nearest_areas_data = [
        {'name': 'Bandra Railway Station', 'area_type': 'metro', 'distance': '1.2 km'},
        {'name': 'Bandra-Kurla Complex (BKC)', 'area_type': 'other', 'distance': '3.5 km'},
        {'name': 'Linking Road Shopping Street', 'area_type': 'mall', 'distance': '800 m'},
        {'name': 'Lilavati Hospital', 'area_type': 'hospital', 'distance': '1.8 km'},
        {'name': 'American School of Bombay', 'area_type': 'school', 'distance': '2.1 km'},
        {'name': 'Palladium Mall', 'area_type': 'mall', 'distance': '2.8 km'},
        {'name': 'Bandra Bandstand Promenade', 'area_type': 'park', 'distance': '1.5 km'},
        {'name': 'Mumbai International Airport', 'area_type': 'airport', 'distance': '8.2 km'},
        {'name': 'Bandra-Worli Sea Link', 'area_type': 'other', 'distance': '2.3 km'},
        {'name': 'Mount Mary Church', 'area_type': 'church', 'distance': '1.1 km'},
    ]
    
    for area_data in nearest_areas_data:
        NearestArea.objects.create(
            project=project,
            **area_data
        )
    print(f"✅ Created {len(nearest_areas_data)} nearest areas")
    
    # Create Floor Plans
    floor_plans_data = [
        {
            'name': '2 BHK East Facing Premium',
            'area': '1200 sq ft',
            'price': Decimal('12500000'),
            'order': 1
        },
        {
            'name': '3 BHK West Facing Deluxe',
            'area': '1650 sq ft',
            'price': Decimal('18500000'),
            'order': 2
        },
        {
            'name': '3 BHK Corner Unit Premium',
            'area': '1850 sq ft',
            'price': Decimal('22500000'),
            'order': 3
        },
        {
            'name': '4 BHK Penthouse Style',
            'area': '2800 sq ft',
            'price': Decimal('35000000'),
            'order': 4
        },
        {
            'name': '4 BHK Duplex Premium',
            'area': '3500 sq ft',
            'price': Decimal('45000000'),
            'order': 5
        },
    ]
    
    for plan_data in floor_plans_data:
        FloorPlan.objects.create(
            project=project,
            **plan_data
        )
    print(f"✅ Created {len(floor_plans_data)} floor plans")
    
    # Create Why Choose Us points
    why_choose_data = [
        {
            'title': 'Prime Bandra West Location',
            'description': 'Located in Mumbai\'s most prestigious neighborhood with excellent connectivity to business districts, shopping, and entertainment hubs',
            'icon': 'fas fa-map-marker-alt',
            'order': 1
        },
        {
            'title': 'Trusted Developer - Prestige Group',
            'description': '30+ years of real estate excellence with over 250 completed projects and reputation for quality construction and timely delivery',
            'icon': 'fas fa-award',
            'order': 2
        },
        {
            'title': 'World-Class Amenities',
            'description': 'Resort-style amenities including Olympic-size pool, fitness center, clubhouse, and landscaped gardens for luxury living',
            'icon': 'fas fa-star',
            'order': 3
        },
        {
            'title': 'Excellent Investment Potential',
            'description': 'Prime location ensures strong appreciation potential and rental yields with Mumbai\'s growing real estate market',
            'icon': 'fas fa-chart-line',
            'order': 4
        },
        {
            'title': 'Premium Specifications',
            'description': 'High-quality finishes, branded fittings, modern kitchen, and luxury bathroom amenities throughout the apartments',
            'icon': 'fas fa-gem',
            'order': 5
        },
        {
            'title': 'Green & Sustainable',
            'description': 'Eco-friendly features including rainwater harvesting, solar heating, and energy-efficient systems for sustainable living',
            'icon': 'fas fa-leaf',
            'order': 6
        },
    ]
    
    for why_data in why_choose_data:
        WhyChooseUs.objects.create(
            project=project,
            **why_data
        )
    print(f"✅ Created {len(why_choose_data)} why choose us points")
    
    # Create Specifications
    specifications_data = [
        {
            'category': 'Flooring',
            'items': [
                {'name': 'Living & Dining Room', 'description': '24"x24" premium vitrified tiles from Kajaria/Somany with anti-skid finish'},
                {'name': 'Master Bedroom', 'description': 'Imported laminated wooden flooring with 15-year warranty'},
                {'name': 'Other Bedrooms', 'description': '24"x24" premium vitrified tiles with wooden finish texture'},
                {'name': 'Kitchen', 'description': 'Anti-skid ceramic tiles 12"x12" with matching dado up to 2 feet height'},
                {'name': 'Bathrooms', 'description': 'Anti-skid ceramic tiles with waterproof treatment and premium finish'},
            ]
        },
        {
            'category': 'Kitchen',
            'items': [
                {'name': 'Kitchen Cabinets', 'description': 'Modular kitchen with soft-close hinges, premium hardware, and granite countertop'},
                {'name': 'Kitchen Appliances', 'description': 'Provision for chimney, hob, microwave, and water purifier with electrical points'},
                {'name': 'Kitchen Sink', 'description': 'Premium stainless steel sink with single lever mixer and waste disposal unit'},
                {'name': 'Kitchen Tiles', 'description': 'Designer tiles up to full height with premium finish and easy maintenance'},
            ]
        },
        {
            'category': 'Bathroom',
            'items': [
                {'name': 'Bathroom Fixtures', 'description': 'Premium CP fittings from Kohler/Grohe with single lever mixers and rain showers'},
                {'name': 'Sanitary Ware', 'description': 'Branded sanitary ware from Kohler/Duravit with concealed cisterns'},
                {'name': 'Hot Water System', 'description': 'Solar water heating system with electric backup for continuous hot water supply'},
                {'name': 'Bathroom Tiles', 'description': 'Designer ceramic tiles up to full height with premium finish and waterproofing'},
                {'name': 'Ventilation', 'description': 'Exhaust fans in all bathrooms with humidity sensors and automatic operation'},
            ]
        },
        {
            'category': 'Doors & Windows',
            'items': [
                {'name': 'Main Door', 'description': 'Premium teak wood main door with digital lock system and security features'},
                {'name': 'Internal Doors', 'description': 'Flush doors with premium polish and branded hardware fittings'},
                {'name': 'Windows', 'description': 'UPVC windows with double glazing for sound insulation and energy efficiency'},
                {'name': 'Balcony Doors', 'description': 'Sliding doors with premium glass and weather sealing for balcony access'},
            ]
        },
        {
            'category': 'Electrical',
            'items': [
                {'name': 'Electrical Wiring', 'description': 'Concealed copper wiring with MCB distribution board and ELCB protection'},
                {'name': 'Power Points', 'description': 'Adequate power points in all rooms with modular switches from Legrand/Schneider'},
                {'name': 'Lighting', 'description': 'LED lighting fixtures in common areas with energy-efficient solutions'},
                {'name': 'Air Conditioning', 'description': 'Split AC provision in all bedrooms and living room with copper piping'},
                {'name': 'Cable TV', 'description': 'Cable TV and internet connectivity provision in all rooms'},
            ]
        },
        {
            'category': 'Plumbing',
            'items': [
                {'name': 'Water Supply', 'description': '24x7 water supply with overhead and underground tanks with water treatment plant'},
                {'name': 'Plumbing Fittings', 'description': 'Concealed plumbing with premium CP fittings and branded accessories'},
                {'name': 'Drainage System', 'description': 'Modern drainage system with STP for water recycling and rainwater harvesting'},
            ]
        },
        {
            'category': 'Safety & Security',
            'items': [
                {'name': 'Fire Safety', 'description': 'Complete fire safety system with sprinklers, smoke detectors, and emergency exits'},
                {'name': 'Security System', 'description': 'Video door phone, CCTV surveillance, and access control systems'},
                {'name': 'Earthquake Resistant', 'description': 'Earthquake-resistant RCC structure designed as per IS codes'},
            ]
        },
        {
            'category': 'Painting',
            'items': [
                {'name': 'Interior Painting', 'description': 'Premium emulsion paint from Asian Paints/Berger with primer and putty finish'},
                {'name': 'Exterior Painting', 'description': 'Weather-resistant exterior paint with texture finish and waterproofing'},
            ]
        },
    ]
    
    spec_category_map = {cat.name: cat for cat in basic_data['spec_categories']}
    
    for spec_data in specifications_data:
        category = spec_category_map[spec_data['category']]
        for item_data in spec_data['items']:
            SpecificationItem.objects.create(
                project=project,
                category=category,
                **item_data
            )
    print(f"✅ Created comprehensive specifications")
    
    # Create Construction Updates
    construction_updates_data = [
        {
            'update_date': date.today() - timedelta(days=30),
            'title': 'Foundation Work Completed - 100%',
            'description': 'Foundation work for all 4 towers has been completed successfully. RCC work for basement parking has commenced. Quality checks and soil testing reports are satisfactory.',
            'order': 1
        },
        {
            'update_date': date.today() - timedelta(days=60),
            'title': 'Ground Floor Slab Work - 75% Complete',
            'description': 'Ground floor slab work is progressing well with 75% completion. Plumbing and electrical conduit work is being done simultaneously. Expected completion by next month.',
            'order': 2
        },
        {
            'update_date': date.today() - timedelta(days=90),
            'title': 'First Floor Construction - 50% Complete',
            'description': 'First floor construction has reached 50% completion. Wall construction and internal wiring work is in progress. Quality monitoring is being done at each stage.',
            'order': 3
        },
        {
            'update_date': date.today() - timedelta(days=120),
            'title': 'Amenities Construction Started',
            'description': 'Construction work for clubhouse and swimming pool area has begun. Landscaping preparation work is also underway. Expected completion in next 6 months.',
            'order': 4
        },
        {
            'update_date': date.today() - timedelta(days=150),
            'title': 'Project Launch and Approvals',
            'description': 'Azure Heights Premium has been officially launched with all necessary approvals including RERA registration. Pre-launch bookings have received overwhelming response.',
            'order': 5
        },
    ]
    
    for update_data in construction_updates_data:
        ConstructionUpdate.objects.create(
            project=project,
            **update_data
        )
    print(f"✅ Created {len(construction_updates_data)} construction updates")
    
    return project

def create_additional_content():
    """Create blogs, careers, and leads"""
    print("📝 Creating Additional Content...")
    
    # Create Blog Tag
    blog_tag = BlogTag.objects.create(name='Real Estate Investment')
    print(f"✅ Created blog tag: {blog_tag.name}")
    
    # Create Blog
    blog = Blog.objects.create(
        title='Why Bandra West is Mumbai\'s Most Sought-After Residential Destination in 2025',
        content='''<h2>Introduction</h2>
        <p>Bandra West has consistently ranked as one of Mumbai's most prestigious residential areas, and 2025 is no exception. This comprehensive guide explores why this locality continues to attract discerning home buyers and investors alike.</p>
        
        <h3>Prime Location and Connectivity</h3>
        <p>Bandra West offers unparalleled connectivity to Mumbai's key business districts including BKC, Lower Parel, and South Mumbai. The upcoming metro connectivity will further enhance its appeal.</p>
        
        <h3>Lifestyle and Amenities</h3>
        <p>From high-end shopping at Linking Road to fine dining at Bandra's famous restaurants, the area offers a complete lifestyle package. The proximity to the seafront adds to its charm.</p>
        
        <h3>Investment Perspective</h3>
        <p>Property values in Bandra West have shown consistent appreciation over the years. The area's limited land availability and high demand ensure strong investment returns.</p>
        
        <h3>Educational Institutions</h3>
        <p>The presence of premium schools and colleges makes it an ideal choice for families. Educational institutions like American School of Bombay enhance the area's appeal.</p>
        
        <h3>Future Development</h3>
        <p>Planned infrastructure developments including metro connectivity and coastal road project will further boost the area's desirability and property values.</p>''',
        meta_title='Why Bandra West Mumbai is the Best Residential Investment in 2025 - Complete Guide',
        meta_description='Discover why Bandra West remains Mumbai\'s most sought-after residential destination in 2025. Complete guide covering location benefits, lifestyle, and investment potential.',
        is_published=True
    )
    blog.tags.add(blog_tag)
    print(f"✅ Created blog: {blog.title}")
    
    # Create Career
    career = Career.objects.create(
        title='Senior Sales Manager - Luxury Residential Properties',
        location='Mumbai, Maharashtra',
        description='''**Position:** Senior Sales Manager - Luxury Residential Properties

**Company:** Prestige Group - Leading Real Estate Developer

**Location:** Mumbai, Maharashtra

**Experience Required:** 5+ years in luxury real estate sales

**Job Description:**
We are seeking a dynamic and experienced Senior Sales Manager to join our luxury residential sales team in Mumbai. The ideal candidate will have a proven track record in selling premium residential properties and building strong client relationships.

**Key Responsibilities:**
• Lead and manage the luxury residential sales team
• Develop and implement effective sales strategies for premium projects
• Build and maintain relationships with HNI clients and channel partners
• Achieve monthly and quarterly sales targets
• Provide market insights and competitive analysis
• Conduct site visits and presentations for potential buyers
• Coordinate with marketing team for promotional activities

**Required Qualifications:**
• Bachelor's degree in Business, Marketing, or related field
• Minimum 5 years of experience in luxury real estate sales
• Proven track record of achieving sales targets
• Excellent communication and presentation skills
• Strong network in Mumbai's real estate market
• Knowledge of luxury property market trends

**Preferred Skills:**
• MBA in Marketing or Sales
• Experience with CRM systems
• Multi-lingual capabilities (Hindi, Marathi, English)
• Valid driving license

**What We Offer:**
• Competitive salary with attractive incentives
• Health insurance and medical benefits
• Performance bonuses and recognition programs
• Career growth opportunities
• Professional development support

**How to Apply:**
Send your resume to careers@prestigegroup.com with subject line "Senior Sales Manager - Mumbai"''',
        is_active=True
    )
    print(f"✅ Created career: {career.title}")
    
    # Create Investment Lead
    investment_lead = InvestmentRequirement.objects.create(
        name='Rajesh Sharma',
        email='rajesh.sharma@example.com',
        contact_number='+91 9876543210',
        location='Mumbai',
        budget='₹1-2 Crores',
        requirement_type='residential',
        how_did_you_know='website',
        agreed_to_terms=True
    )
    print(f"✅ Created investment lead: {investment_lead.name}")
    
    # Create Land Lead
    land_lead = LandRequirement.objects.create(
        name='Sunil Patel',
        email='sunil.patel@example.com',
        contact_number='+91 9876543211',
        location='Mumbai Outskirts',
        budget='₹5-10 Crores',
        area=Decimal('2.5'),
        area_unit='acre',
        requirement_type='buy',
        status='new',
        agreed_to_terms=True
    )
    print(f"✅ Created land lead: {land_lead.name}")

def main():
    """Main function to create complete demo data"""
    print("🚀 Creating ONE Complete Project with ALL Fields...")
    print("=" * 70)
    
    try:
        # Clean database
        clean_database()
        
        # Create basic data
        basic_data = create_basic_data()
        
        # Create complete project
        project = create_complete_project(basic_data)
        
        # Create additional content
        create_additional_content()
        
        print("=" * 70)
        print("✅ SINGLE COMPLETE PROJECT CREATED SUCCESSFULLY!")
        print("=" * 70)
        print("📊 Summary:")
        print(f"🏙️  Cities: 1 (Mumbai)")
        print(f"📂 Categories: 1 (Residential)")
        print(f"🏢 Project Types: 1 (Luxury Apartments)")
        print(f"🏷️  Tags: 5")
        print(f"🏊 Amenities: 6")
        print(f"🏗️  Projects: 1 (Azure Heights Premium)")
        print(f"📐 Floor Plans: 5")
        print(f"📍 Nearest Areas: 10")
        print(f"❓ Why Choose Us: 6 points")
        print(f"🔧 Specifications: 25+ items across 8 categories")
        print(f"🚧 Construction Updates: 5")
        print(f"📝 Blogs: 1")
        print(f"💼 Careers: 1")
        print(f"📞 Sample Leads: 2")
        print("=" * 70)
        print("🎉 Your project is now ready with COMPLETE data!")
        print("🌐 Run 'python manage.py runserver' to see the results")
        print("👤 Admin: admin / 123")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
