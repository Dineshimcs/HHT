from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Notification

@csrf_exempt
def unread_count(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        count = 0
        
    response = JsonResponse({'unread_count': count, 'status': 'success'})
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt
def notification_list(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    if not request.user.is_authenticated:
        return JsonResponse({'notifications': [], 'unread_count': 0})

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
    data = [
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat(),
        }
        for n in notifications
    ]
    response = JsonResponse({'notifications': data, 'unread_count': Notification.objects.filter(user=request.user, is_read=False).count()})
    response['Access-Control-Allow-Origin'] = '*'
    return response

@csrf_exempt
def mark_as_read(request, pk=None):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    if request.user.is_authenticated:
        if pk:
            Notification.objects.filter(id=pk, user=request.user).update(is_read=True)
        else:
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)

    response = JsonResponse({'status': 'success'})
    response['Access-Control-Allow-Origin'] = '*'
    return response
