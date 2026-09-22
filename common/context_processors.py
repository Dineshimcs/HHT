from django.conf import settings

def brand_context(request):
    """
    Global template context processor for platform brand tokens and active state.
    """
    user_role = getattr(request.user, 'role', 'GUEST') if getattr(request, 'user', None) and request.user.is_authenticated else 'GUEST'
    return {
        'PLATFORM_NAME': settings.AURA_PLATFORM['NAME'],
        'PLATFORM_TAGLINE': settings.AURA_PLATFORM['TAGLINE'],
        'PLATFORM_CURRENCY': settings.AURA_PLATFORM['CURRENCY'],
        'CURRENT_ROLE': user_role,
        'IS_CUSTOMER': user_role == 'CUSTOMER',
        'IS_DRIVER': user_role == 'DRIVER',
        'IS_ADMIN': user_role == 'ADMIN' or getattr(request.user, 'is_superuser', False),
    }
