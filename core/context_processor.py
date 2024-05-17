from core.models import FriendRequest,Notification


  # Make sure to replace 'yourapp' with the correct app name

def my_context_processor(request):
    try:
        friend_requests = FriendRequest.objects.filter(receiver=request.user).order_by('-id')
    except:
        friend_requests = None
    
    try:
        notification = Notification.objects.filter(user=request.user).order_by('-id')
    except:
        notification = None
        
    
    return {
        "friend_requests": friend_requests,
        "notification": notification
    }