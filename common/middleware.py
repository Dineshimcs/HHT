import logging
from django.utils import timezone

logger = logging.getLogger('aura.audit')

class AuditLoggingMiddleware:
    """
    Middleware that captures request metadata for security auditing.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = timezone.now()
        response = self.get_response(request)
        
        # Log write/mutation operations
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] and hasattr(request, 'user'):
            user_str = str(request.user) if request.user.is_authenticated else 'Anonymous'
            logger.info(
                f"AUDIT | User: {user_str} | Method: {request.method} | "
                f"Path: {request.path} | Status: {response.status_code} | "
                f"IP: {self.get_client_ip(request)}"
            )
            
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '127.0.0.1')
