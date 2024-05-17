from django.shortcuts import render
from core.models import Post,History,ReplyComment,Friend,ChatMessage,Comment,ReplyComment,Friend,FriendRequest,Notification
import shortuuid
from django.utils.text import slugify
from django.http import JsonResponse
from django.utils.timesince import timesince
from  django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.defaultfilters import timesince
from django.contrib.auth.decorators import login_required
from userauths.models import User

from django.db.models import OuterRef,Subquery,Q

# Create your views here.
noti_new_like="New Like"
noti_new_follower="New Followers"
noti_friend_request="Friend Request"
noti_new_comment="New Comment"
noti_comment_liked="Comment Liked"
noti_comment_replied="Comment Replied"
noti_friend_request_accepted="Friend Request Acceptd"

def send_notification(user=None,sender=None,post=None,comment=None,notification_type=None):
    notification=Notification.objects.create(
        user=user,
        sender=sender,
        post=post,
        comment=comment,
        notification_type=notification_type,
    )
    
    return notification
@login_required
def post_detail(request,slug):
    posts=Post.objects.get(slug=slug,visibility='Everyone',active=True)
    context={
        'posts':posts
    }
    
    return render(request,'core/detail.html',context)
@login_required
def index(request):
    posts=Post.objects.filter(active=True,visibility='Everyone').order_by('-id')
    poster=History.objects.filter(active=True,visibility='Everyone').order_by('-id')
    friend=Friend.objects.all().order_by('-id')
    
    context={
        'postss':posts,
        'poster':poster,
        'friend':friend
    }
    return render(request,'core/index.html',context)

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('post-caption')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('post-thumbnail')
        
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        
        if title and image:
            post = Post(
                title=title,
                visibility=visibility,
                image=image,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            post.save()
            
            # Calculate time difference using current time if post.date is None
            current_time = timezone.now()
            post_date = post.date if post.date is not None else current_time
            time_difference = timesince(post_date)
            
            # Convert ImageFieldFile to string representation of image URL
            image_url = post.image.url if post.image else ''

            return JsonResponse({
                'post': {
                    'title': post.title,
                    'image': image_url,
                    'full_name': post.user.profile.full_name,
                    'profile_image': post.user.profile.image.url,
                    'date': time_difference,
                    'id': post.id
                }
            })
        
        else:
            return JsonResponse({'error': 'image or title does not exist'})
    
    return JsonResponse({'data': 'sent'})

def like_post(request):
    id = request.GET.get('id')
    post = Post.objects.get(id=id)
    user = request.user
    bool_val = False
    
    if user in post.likes.all():
        post.likes.remove(user)
    
    else:
        post.likes.add(user)
        bool_val = True
    
    post.save()  # Save the changes to the post

    if post.user != request.user:
        send_notification(post.user,user,post,None,noti_new_like)
    
    data = {
        'bool': bool_val,
        'likes': post.likes.all().count()
    }
    
    return JsonResponse({'data': data})

def comment_on_post(request):
    id=request.GET['id']
    comment=request.GET['comment']
    post=Post.objects.get(id=id)
    comment_count=Comment.objects.filter(post=post).count()
    user=request.user
    
    new_comment=Comment.objects.create(
        post=post,
        comment=comment,
        user=user
    )
    
    if new_comment.user != post.user:
        send_notification(post.user,user,post,new_comment,noti_new_comment)
    
    
    data = {
        "bool": True,
        "comment": new_comment.comment,
        "profile_image":new_comment.user.profile.image.url,
        "user_id": new_comment.user.id,
        "date": timesince(new_comment.date),
        "comment_id": new_comment.id,
        "post_id": new_comment.post.id,
        "comment_count": comment_count +int(1)
}

    
    return JsonResponse({'data': data})

def like_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False
    
    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool= True

    if comment.user != user:
        send_notification(comment.user,user,comment.post,comment,noti_comment_liked)
    
    
    data = {
        'bool': bool,
        'likes': comment.likes.all().count()
    }
    
    return JsonResponse({'data': data})

from django.core.serializers import serialize
from django.http import JsonResponse
from django.template.defaultfilters import timesince
from django.db.models.fields.files import ImageFieldFile

def reply_comment(request):
    id = request.GET.get('id')
    reply = request.GET.get('reply')
    comment = Comment.objects.get(id=id)
    user = request.user
    
    new_reply = ReplyComment.objects.create(
        comment=comment,
        reply=reply,
        user=user
    )
    if comment.user != user:
        send_notification(comment.user,user,comment.post,comment,noti_comment_replied)
    
    data = {
        "bool": True,
        "reply": new_reply.reply,
        "profile_image": new_reply.user.profile.image.url,
        "user_id": new_reply.user.id,
        "date": timesince(new_reply.date),
        "reply_id": new_reply.id,
        "post_id": new_reply.comment.post.id,
    }
    
    return JsonResponse({'data': data})

def delete_comment(request):
    id=request.GET['id']
    comment=Comment.objects.filter(id=id)
    comment.delete()
    
    data={
        'bool':True,
        
    }
    
    return JsonResponse({'data': data})


def delete_reply(request):
    id=request.GET['id']
    reply=ReplyComment.objects.filter(id=id)
    reply.delete()
    
    data={
        'bool':True,
        
    }
    
    return JsonResponse({'data': data})

def add_friend(request):
    sender=request.user
    receiver_id=request.GET['id']
    bool=False
    
    if sender.id==int(receiver_id):
        return JsonResponse({'error':"you can not send friend request to your self"})
    receiver=User.objects.get(id=receiver_id)
    
    try:
        friend_request=FriendRequest.objects.get(sender=sender,receiver=receiver)
        if friend_request:
            friend_request.delete()
        bool=False
        return JsonResponse({'error':'canceled','bool':bool})
    except FriendRequest.DoesNotExist:
        friend_request=FriendRequest(sender=sender,receiver=receiver)
        friend_request.save()
        bool=True
        
        send_notification(receiver,sender,None,None,noti_friend_request)
    
        return JsonResponse({'success':'sent','bool':bool})
    
def accept_friend_request(request):
    id=request.GET['id']
    receiver = request.user
    sender = User.objects.get(id=id)

    friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
    receiver.profile.friends.add(sender)
    sender.profile.friends.add(receiver)
    friend_request.delete()
    
    send_notification(sender,receiver,None,None,noti_friend_request_accepted)
    data = {
        "Message": "Accepted",
        "bool":True
        
    }
    
    return JsonResponse({'data':data})

def reject_friend_request(request):
    id=request.GET['id']
    receiver = request.user
    sender = User.objects.get(id=id)

    friend_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
    
    friend_request.delete()
    
    data = {
        "Message": "Rejected",
        "bool":True
        
    }
    
    return JsonResponse({'data':data})

def unfriend(request):
    sender=request.user
    friend_id=request.GET['id']
    bool=False
    if sender.id==int(friend_id):
        
        return JsonResponse({'error':'you can not unfriend yourself'})

    my_friend=User.objects.get(id=friend_id)
    if my_friend in sender.profile.friends.all():
        sender.profile.friends.remove(my_friend)
        my_friend.profile.friends.remove(sender)
        bool=True
        return JsonResponse({'success':'unfriend successfull','bool':bool})






@csrf_exempt
def history(request):
    if request.method == 'POST':
        title = request.POST.get('post-text')
       
        image = request.FILES.get('post-thumbnail')
        
        #uuid_key = shortuuid.uuid()
        #uniqueid = uuid_key[:4]
        
        if title and image:
            history = History(
                title=title,
                
                image=image,
                user=request.user,
                #slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            history.save()
            
            # Calculate time difference using current time if post.date is None
            current_time = timezone.now()
            post_date = history.date if history.date is not None else current_time
            time_difference = timesince(post_date)
            
            # Convert ImageFieldFile to string representation of image URL
            image_url = history.image.url if history.image else ''

            return JsonResponse({
                'post': {
                    'title': history.title,
                    'image': image_url,
                    'full_name': history.user.profile.full_name,
                    'profile_image': history.user.profile.image.url,
                    'date': time_difference,
                    'id': history.id
                }
            })
        
        else:
            return JsonResponse({'error': 'image or title does not exist'})
    
    return JsonResponse({'data': 'sent'})


def inbox(request):
    user_id = request.user
    
    chat_messages = ChatMessage.objects.filter(
        id__in=Subquery(
            User.objects.filter(
                Q(sender__receiver=user_id) | Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_message=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'), receiver=user_id) |  
                        Q(receiver=OuterRef('id'), sender=user_id)    
                    ).order_by('-id')[:1].values_list('id', flat=True)  # Get only the first message ID
                )
            ).values_list('last_message', flat=True).order_by('id')
        )
    ).order_by('-id')  
    print(chat_messages)
    context = {
        'chat_messages': chat_messages  
    }
    
    return render(request, 'chat/chat.html', context)


def inbox_detail(request,username):
    
    user_id = request.user
    
    chat_messages = ChatMessage.objects.filter(
        id__in=Subquery(
            User.objects.filter(
                Q(sender__receiver=user_id) | Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_message=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'), receiver=user_id) |  
                        Q(receiver=OuterRef('id'), sender=user_id)    
                    ).order_by('-id')[:1].values_list('id', flat=True)  # Get only the first message ID
                )
            ).values_list('last_message', flat=True).order_by('id')
        )
    ).order_by('-id')
    
    sender=request.user
    receiver=User.objects.get(username=username)
    receiver_detail=User.objects.get(username=username)
    
    message_detail=ChatMessage.objects.filter(
        Q(sender=sender,receiver=receiver) | Q(sender=receiver,receiver=sender)
    ).order_by('date')
    
    message_detail.update(is_read=True)
    
    if message_detail:
        r=message_detail.first()
        receiver=User.objects.get(username=r.receiver)
    else:
       receiver=User.objects.get(username=username)
       

    context = {
        'chat_messages': chat_messages,
        'message_detail':message_detail,
        'sender':sender,
        'receiver':receiver,  
        'receiver_detail':receiver_detail,  
    }
    
    return render(request, 'chat/chat_detail.html', context)