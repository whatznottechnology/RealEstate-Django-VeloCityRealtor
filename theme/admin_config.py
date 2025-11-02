"""
Dynamic configuration for Unfold Admin Panel
Fetches site settings from database to customize admin panel appearance
"""

def get_admin_environment(request):
    """
    Get dynamic admin panel configuration from SiteConfig
    
    This function is called by Unfold on each admin request to provide
    dynamic branding (logo, favicon, title) from the database.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        dict: Environment variables for admin panel customization
    """
    from theme.models import SiteConfig
    from django.db import connection, OperationalError, ProgrammingError
    
    # Safety check: ensure database tables exist
    try:
        with connection.cursor() as cursor:
            # Check if theme_siteconfig table exists (SQLite specific)
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='theme_siteconfig';"
            )
            if not cursor.fetchone():
                print("⚠️  Admin Config: Database table 'theme_siteconfig' not found yet (migrations pending)")
                return {}
    except (OperationalError, ProgrammingError) as e:
        print(f"⚠️  Admin Config: Database not ready - {e}")
        return {}
    except Exception as e:
        print(f"⚠️  Admin Config: Unexpected error checking database - {e}")
        return {}
    
    try:
        # Get site configuration from database
        site_config = SiteConfig.get_config()
        
        # Build environment dictionary
        env = {}
        
        # === SITE TITLE ===
        if site_config.site_title:
            env['SITE_TITLE'] = site_config.site_title
            env['SITE_HEADER'] = f"{site_config.site_title} Admin"
            print(f"✅ Admin Config: Title = '{site_config.site_title}'")
        
        # === SITE LOGO (shown in header) ===
        # Hardcoded to static file for reliability
        logo_url = "/static/admin/img/lofa.png"  # Use relative path
        env['SITE_LOGO'] = logo_url  # Try simple string instead of dict
        print(f"✅ Admin Config: Logo = '{logo_url}' (hardcoded, relative path)")
        
        # === SITE ICON (shown in sidebar next to title) ===
        # Hardcoded to static file for reliability
        favicon_url = "/static/admin/img/lofa.png"  # Use relative path
        env['SITE_ICON'] = favicon_url  # Try simple string instead of dict
        print(f"✅ Admin Config: Icon = '{favicon_url}' (hardcoded, relative path)")
        
        # Use favicon as symbol instead of emoji
        env['SITE_SYMBOL'] = None  # Remove emoji, use icon instead
        
        # === FAVICONS (browser tab icons) ===
        # Hardcoded to static file for reliability
        env['SITE_FAVICONS'] = [
            {
                "rel": "icon",
                "sizes": "32x32",
                "type": "image/png",
                "href": "/static/admin/img/lofa.png",
            },
            {
                "rel": "icon",
                "sizes": "192x192",
                "type": "image/png",
                "href": "/static/admin/img/lofa.png",
            },
            {
                "rel": "apple-touch-icon",
                "sizes": "180x180",
                "type": "image/png",
                "href": "/static/admin/img/lofa.png",
            },
        ]
        print(f"✅ Admin Config: Favicons configured (hardcoded, relative paths)")
        
        print(f"✅ Admin Config: Returning {len(env)} environment variables")
        return env
        
    except Exception as e:
        # Graceful fallback if anything goes wrong
        print(f"❌ Admin Config Error: {e}")
        import traceback
        traceback.print_exc()
        return {}
