"""
Management command to populate interior app with demo data
"""
from django.core.management.base import BaseCommand
from interior.models import InteriorService, PortfolioWork
from django.core.files.base import ContentFile
import requests
from datetime import date


class Command(BaseCommand):
    help = 'Populate interior app with demo services and portfolio works'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate interior demo data...'))
        
        # Create Interior Services
        services_data = [
            {
                'title': 'Residential Interior',
                'category': 'residential',
                'description': 'Transform your home into a beautiful, functional space that reflects your personal style and enhances your daily living experience with our expert residential interior design services.',
                'badge_text': 'popular',
                'icon_class': 'fas fa-home',
                'features': 'Living Room Design\nBedroom Makeover\nKitchen Planning\nBathroom Design',
                'order': 1,
            },
            {
                'title': 'Commercial Interior',
                'category': 'commercial',
                'description': 'Create professional, productive workspaces that inspire your team and impress your clients with our comprehensive commercial interior solutions tailored to your business needs.',
                'badge_text': 'professional',
                'icon_class': 'fas fa-building',
                'features': 'Office Design\nRetail Spaces\nRestaurant Design\nReception Areas',
                'order': 2,
            },
            {
                'title': 'Modular Solutions',
                'category': 'modular',
                'description': 'Smart, space-saving modular designs that maximize functionality while maintaining aesthetic appeal for modern living and working spaces with innovative storage solutions.',
                'badge_text': 'trending',
                'icon_class': 'fas fa-cube',
                'features': 'Modular Kitchen\nWardrobe Design\nStorage Solutions\nSpace Planning',
                'order': 3,
            },
            {
                'title': '3D Visualization',
                'category': '3d_visualization',
                'description': 'See your space before it\'s built with photorealistic 3D renderings and virtual walkthroughs to visualize your dream interior and make informed design decisions.',
                'badge_text': 'new',
                'icon_class': 'fas fa-cube',
                'features': '3D Floor Plans\nPhotorealistic Renders\nVirtual Walkthroughs\nMaterial Previews',
                'order': 4,
            },
            {
                'title': 'Furniture & Decor',
                'category': 'furniture',
                'description': 'Complete furnishing solutions with carefully curated furniture, lighting, and decorative elements to complement your interior design and create a cohesive look.',
                'badge_text': 'trending',
                'icon_class': 'fas fa-couch',
                'features': 'Custom Furniture\nLighting Design\nWall Art & Decor\nWindow Treatments',
                'order': 5,
            },
            {
                'title': 'Renovation & Remodeling',
                'category': 'renovation',
                'description': 'Transform existing spaces with comprehensive renovation and remodeling services to give your property a fresh, modern look while maintaining structural integrity.',
                'badge_text': 'professional',
                'icon_class': 'fas fa-hammer',
                'features': 'Complete Renovation\nStructural Changes\nFlooring Solutions\nElectrical & Plumbing',
                'order': 6,
            },
        ]

        # Clear existing services
        InteriorService.objects.all().delete()
        self.stdout.write('Cleared existing services')

        # Create services (without images since we're using placeholders)
        for data in services_data:
            service = InteriorService.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'✓ Created service: {service.title}'))

        # Create Portfolio Works
        portfolio_data = [
            {
                'title': 'Modern Living Room',
                'description': 'Contemporary design with clean lines, neutral tones, and elegant furniture pieces creating a welcoming and sophisticated living space.',
                'work_type': 'residential',
                'location': 'Kolkata, West Bengal',
                'completion_date': date(2024, 6, 15),
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Elegant Bedroom Suite',
                'description': 'Luxurious bedroom design with premium finishes, custom furniture, and ambient lighting for ultimate comfort and style.',
                'work_type': 'residential',
                'location': 'Durgapur, West Bengal',
                'completion_date': date(2024, 5, 20),
                'is_featured': False,
                'order': 2,
            },
            {
                'title': 'Contemporary Kitchen',
                'description': 'Functional modular kitchen design with modern appliances, efficient storage, and sleek aesthetics for daily convenience.',
                'work_type': 'modular',
                'location': 'Siliguri, West Bengal',
                'completion_date': date(2024, 7, 10),
                'is_featured': True,
                'order': 3,
            },
            {
                'title': 'Corporate Office Space',
                'description': 'Professional workspace design optimized for productivity with ergonomic furniture, proper lighting, and collaborative areas.',
                'work_type': 'commercial',
                'location': 'Salt Lake, Kolkata',
                'completion_date': date(2024, 4, 30),
                'is_featured': False,
                'order': 4,
            },
            {
                'title': 'Luxury Spa Bathroom',
                'description': 'Spa-like bathroom with premium fixtures, natural materials, and ambient lighting creating a relaxing retreat atmosphere.',
                'work_type': 'residential',
                'location': 'New Town, Kolkata',
                'completion_date': date(2024, 8, 5),
                'is_featured': True,
                'order': 5,
            },
            {
                'title': 'Retail Showroom',
                'description': 'Attractive retail space design with strategic product placement, excellent lighting, and customer-friendly layout to boost sales.',
                'work_type': 'commercial',
                'location': 'Park Street, Kolkata',
                'completion_date': date(2024, 3, 25),
                'is_featured': False,
                'order': 6,
            },
        ]

        # Clear existing portfolio works
        PortfolioWork.objects.all().delete()
        self.stdout.write('Cleared existing portfolio works')

        # Create portfolio works (without images since we're using placeholders)
        for data in portfolio_data:
            work = PortfolioWork.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'✓ Created portfolio work: {work.title}'))

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✓ Successfully populated interior demo data!'))
        self.stdout.write(self.style.SUCCESS(f'  - Created {len(services_data)} services'))
        self.stdout.write(self.style.SUCCESS(f'  - Created {len(portfolio_data)} portfolio works'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.WARNING('\nNote: Images are not included in demo data.'))
        self.stdout.write(self.style.WARNING('Please upload images through Django admin panel.'))
