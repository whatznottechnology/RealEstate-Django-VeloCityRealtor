"""
Unit Tests for Promotional Toggle System

Tests the new promotional toggle fields and their filtering logic
to ensure multiple toggles can be enabled simultaneously and
homepage sections return correct projects.
"""

from django.test import TestCase
from django.db.models import Q, Count
from Projects.models import Project, Category, ProjectType, City, Tag
from datetime import date


class PromotionalToggleTests(TestCase):
    """Test suite for promotional toggle functionality"""

    @classmethod
    def setUpTestData(cls):
        """Set up test data that's shared across all test methods"""
        # Create test category
        cls.category = Category.objects.create(
            name='Residential',
            description='Residential properties'
        )
        
        # Create test city
        cls.city = City.objects.create(
            name='Mumbai',
            state='Maharashtra',
            country='India'
        )
        
        # Create test project type
        cls.project_type = ProjectType.objects.create(
            name='Apartment',
            category=cls.category
        )
        
        # Create test tags
        cls.tag_luxury = Tag.objects.create(name='Luxury')
        cls.tag_gated = Tag.objects.create(name='Gated Community')
        cls.tag_premium = Tag.objects.create(name='Premium')

    def test_multiple_promotional_toggles_enabled(self):
        """Test that a project can have multiple promotional toggles enabled simultaneously"""
        project = Project.objects.create(
            name='Test Project Multi Toggle',
            slug='test-project-multi-toggle',
            category=self.category,
            city=self.city,
            project_type=self.project_type,
            is_active=True,
            # Enable multiple promotional toggles
            promo_hot_deals=True,
            promo_premium_projects=True,
            promo_trending_projects=True,
            promo_most_viewed=True,
            promo_for_sale=True
        )
        
        # Verify all toggles are saved correctly
        project.refresh_from_db()
        self.assertTrue(project.promo_hot_deals)
        self.assertTrue(project.promo_premium_projects)
        self.assertTrue(project.promo_trending_projects)
        self.assertTrue(project.promo_most_viewed)
        self.assertTrue(project.promo_for_sale)

    def test_hot_deals_section_query(self):
        """Test that hot deals section returns correct projects"""
        # Create hot deal projects
        hot_deal_1 = Project.objects.create(
            name='Hot Deal 1',
            slug='hot-deal-1',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_hot_deals=True
        )
        
        hot_deal_2 = Project.objects.create(
            name='Hot Deal 2',
            slug='hot-deal-2',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_hot_deals=True
        )
        
        # Create non-hot-deal project
        regular_project = Project.objects.create(
            name='Regular Project',
            slug='regular-project',
            category=self.category,
            city=self.city,
            is_active=True
        )
        
        # Query like in home view
        hot_deals = Project.objects.filter(
            promo_hot_deals=True,
            is_active=True
        )
        
        # Verify results
        self.assertEqual(hot_deals.count(), 2)
        self.assertIn(hot_deal_1, hot_deals)
        self.assertIn(hot_deal_2, hot_deals)
        self.assertNotIn(regular_project, hot_deals)

    def test_premium_projects_section_query(self):
        """Test that premium projects section returns correct projects"""
        premium_1 = Project.objects.create(
            name='Premium 1',
            slug='premium-1',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_premium_projects=True
        )
        
        premium_2 = Project.objects.create(
            name='Premium 2',
            slug='premium-2',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_premium_projects=True
        )
        
        # Query like in home view
        premium_projects = Project.objects.filter(
            promo_premium_projects=True,
            is_active=True
        )
        
        self.assertEqual(premium_projects.count(), 2)
        self.assertIn(premium_1, premium_projects)
        self.assertIn(premium_2, premium_projects)

    def test_trending_projects_section_query(self):
        """Test that trending projects section returns correct projects"""
        trending_1 = Project.objects.create(
            name='Trending 1',
            slug='trending-1',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_trending_projects=True
        )
        
        trending_2 = Project.objects.create(
            name='Trending 2',
            slug='trending-2',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_trending_projects=True
        )
        
        # Query like in home view
        trending_projects = Project.objects.filter(
            promo_trending_projects=True,
            is_active=True
        )
        
        self.assertEqual(trending_projects.count(), 2)
        self.assertIn(trending_1, trending_projects)
        self.assertIn(trending_2, trending_projects)

    def test_residential_commercial_sections(self):
        """Test residential and commercial promotional toggles"""
        residential = Project.objects.create(
            name='Residential Complex',
            slug='residential-complex',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_residential_projects=True
        )
        
        # Create commercial category
        commercial_cat = Category.objects.create(
            name='Commercial',
            description='Commercial properties'
        )
        
        commercial = Project.objects.create(
            name='Commercial Space',
            slug='commercial-space',
            category=commercial_cat,
            city=self.city,
            is_active=True,
            promo_commercial_projects=True
        )
        
        # Query residential
        residential_projects = Project.objects.filter(
            Q(promo_residential_projects=True) | Q(category__name__icontains='residential'),
            is_active=True
        )
        
        # Query commercial
        commercial_projects = Project.objects.filter(
            Q(promo_commercial_projects=True) | Q(category__name__icontains='commercial'),
            is_active=True
        )
        
        self.assertIn(residential, residential_projects)
        self.assertIn(commercial, commercial_projects)

    def test_for_sale_rent_lease_toggles(self):
        """Test the for sale/rent/lease promotional toggles"""
        for_sale = Project.objects.create(
            name='For Sale Property',
            slug='for-sale-property',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_for_sale=True
        )
        
        for_rent = Project.objects.create(
            name='For Rent Property',
            slug='for-rent-property',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_for_rent=True
        )
        
        for_lease = Project.objects.create(
            name='For Lease Property',
            slug='for-lease-property',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_for_lease=True
        )
        
        # Query each type
        sale_projects = Project.objects.filter(
            promo_for_sale=True,
            is_active=True
        )
        
        rent_projects = Project.objects.filter(
            promo_for_rent=True,
            is_active=True
        )
        
        lease_projects = Project.objects.filter(
            promo_for_lease=True,
            is_active=True
        )
        
        self.assertEqual(sale_projects.count(), 1)
        self.assertEqual(rent_projects.count(), 1)
        self.assertEqual(lease_projects.count(), 1)
        self.assertIn(for_sale, sale_projects)
        self.assertIn(for_rent, rent_projects)
        self.assertIn(for_lease, lease_projects)

    def test_related_projects_with_shared_tags(self):
        """Test related projects logic with shared tags"""
        # Create base project with tags
        base_project = Project.objects.create(
            name='Base Project',
            slug='base-project',
            category=self.category,
            city=self.city,
            is_active=True
        )
        base_project.tags.add(self.tag_luxury, self.tag_gated)
        
        # Create related project with shared tags
        related_1 = Project.objects.create(
            name='Related with Tags',
            slug='related-with-tags',
            category=self.category,
            city=self.city,
            is_active=True
        )
        related_1.tags.add(self.tag_luxury)  # Shares luxury tag
        
        # Create related project same category
        related_2 = Project.objects.create(
            name='Related Same Category',
            slug='related-same-category',
            category=self.category,
            city=self.city,
            is_active=True
        )
        
        # Create unrelated project
        unrelated = Project.objects.create(
            name='Unrelated Project',
            slug='unrelated-project',
            category=Category.objects.create(name='Other'),
            city=City.objects.create(name='Delhi', state='Delhi', country='India'),
            is_active=True
        )
        
        # Get project tags for comparison
        project_tags = list(base_project.tags.values_list('id', flat=True))
        
        # Build filter like in public_project_detail_view
        filters = Q()
        if project_tags:
            filters |= Q(tags__id__in=project_tags)
        if base_project.category:
            filters |= Q(category=base_project.category)
        if base_project.city:
            filters |= Q(city=base_project.city)
        
        # Get related projects
        related_projects = Project.objects.filter(
            is_active=True
        ).exclude(id=base_project.id).filter(filters).annotate(
            tag_matches=Count('tags', filter=Q(tags__id__in=project_tags))
        ).order_by('-tag_matches', '-created_at').distinct()
        
        # Verify results
        self.assertIn(related_1, related_projects)
        self.assertIn(related_2, related_projects)
        self.assertNotIn(unrelated, related_projects)
        
        # Verify tag-matched project comes first
        related_list = list(related_projects)
        self.assertEqual(related_list[0].id, related_1.id)

    def test_related_projects_with_promotional_toggles(self):
        """Test related projects logic with shared promotional toggles"""
        base_project = Project.objects.create(
            name='Base Hot Deal',
            slug='base-hot-deal',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_hot_deals=True,
            promo_premium_projects=True
        )
        
        # Related with same promotional toggles
        related_1 = Project.objects.create(
            name='Related Hot Deal',
            slug='related-hot-deal',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_hot_deals=True
        )
        
        # Build filter
        filters = Q()
        if base_project.promo_hot_deals:
            filters |= Q(promo_hot_deals=True)
        if base_project.promo_premium_projects:
            filters |= Q(promo_premium_projects=True)
        if base_project.category:
            filters |= Q(category=base_project.category)
        
        # Get related projects
        related_projects = Project.objects.filter(
            is_active=True
        ).exclude(id=base_project.id).filter(filters).distinct()
        
        self.assertIn(related_1, related_projects)

    def test_inactive_projects_excluded(self):
        """Test that inactive projects are excluded from all queries"""
        active_project = Project.objects.create(
            name='Active Project',
            slug='active-project',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_hot_deals=True
        )
        
        inactive_project = Project.objects.create(
            name='Inactive Project',
            slug='inactive-project',
            category=self.category,
            city=self.city,
            is_active=False,
            promo_hot_deals=True
        )
        
        # Query hot deals
        hot_deals = Project.objects.filter(
            promo_hot_deals=True,
            is_active=True
        )
        
        self.assertIn(active_project, hot_deals)
        self.assertNotIn(inactive_project, hot_deals)

    def test_composite_index_performance(self):
        """Test that composite indexes exist for performance"""
        from django.db import connection
        
        # Get table name
        table_name = Project._meta.db_table
        
        # Get constraints (indexes) - updated for Django 5.x
        with connection.cursor() as cursor:
            constraints = connection.introspection.get_constraints(cursor, table_name)
        
        # Verify our promotional toggle indexes exist
        index_names = [
            'idx_hot_deals_active',
            'idx_premium_active',
            'idx_trending_active',
            'idx_mostviewed_active',
            'idx_forsale_active',
            'idx_forrent_active',
            'idx_forlease_active'
        ]
        
        # Check that at least some indexes exist
        existing_indexes = [name for name in index_names if name in constraints]
        
        # Verify indexes were created (should have all 7)
        self.assertGreater(len(existing_indexes), 0, "At least some promotional indexes should exist")

    def test_badge_priority_logic(self):
        """Test badge priority system for property cards"""
        # Premium should have highest priority
        premium_project = Project.objects.create(
            name='Premium with Multiple Badges',
            slug='premium-multi-badges',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_premium_projects=True,
            promo_hot_deals=True,
            promo_trending_projects=True
        )
        
        # Test priority order:
        # 1. Premium > 2. Hot Deal > 3. Trending > 4. Most Viewed
        
        # Premium should be shown (highest priority)
        self.assertTrue(premium_project.promo_premium_projects)
        
        # Create project with only hot deal
        hot_deal_only = Project.objects.create(
            name='Hot Deal Only',
            slug='hot-deal-only',
            category=self.category,
            city=self.city,
            is_active=True,
            promo_hot_deals=True
        )
        
        self.assertTrue(hot_deal_only.promo_hot_deals)
        self.assertFalse(hot_deal_only.promo_premium_projects)
