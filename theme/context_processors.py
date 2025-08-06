from .models import SiteConfig


def site_config(request):
    """Context processor to make site configuration available in all templates"""
    try:
        config = SiteConfig.get_config()
        return {
            'site_config': config
        }
    except Exception:
        # Return empty config if there's an error
        return {
            'site_config': None
        }
