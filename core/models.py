from django.db import models
from userauths.models import User,Profile,user_directory_path

from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from django.utils.html import format_html


VISIBLE=(
    ('Only Me','Only Me'),
    ('Everyone','Everyone')
)

FriendRequest=(
    ('Pending','Pending'),
    ('Accept','Accept'),
    ('Reject','Reject'),
)

NOTIFICATION_TYPE=(
        ('Friend Request','Friend Request'),
        ('Friend request Accepted','Friend request Accepted'),
        ('New follower','New Follower'),
        ('New Like','New Like'),
        ('New Comment','New Comment'),
        ('Comment Liked','Comment Liked'),
        ('Comment Replied','Comment Replied'),
        
    )
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300,blank=True,null=True)
    image=models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    video=models.FileField(upload_to=user_directory_path,null=True,blank=True)
    visibility=models.CharField(max_length=100,choices=VISIBLE,default='Everyone')
    pid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    likes=models.ManyToManyField(User,blank=True,related_name='likes')
    active=models.BooleanField(default=True)
    slug=models.SlugField(unique=True)
    views=models.PositiveIntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.user.username
        
    def save(self,*args,**kwargs):
        uuid_key=shortuuid.uuid()
        uniqueid=uuid_key[:4]
        if self.slug=='' or self.slug==None:
            self.slug=slugify(self.title) + '-' + uniqueid
        super(Post,self).save(*args,**kwargs)
        
    def post_comments(self):
        comments=Comment.objects.filter(post=self,active=True).order_by('-date')
        return comments
    
    

class History(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300,blank=True,null=True)
    image=models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    video=models.FileField(upload_to=user_directory_path,null=True,blank=True)
    visibility=models.CharField(max_length=100,choices=VISIBLE,default='Everyone')
    pid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
   
    active=models.BooleanField(default=True)
    #slug=models.SlugField(unique=True)
    views=models.PositiveIntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.user.username
        
   
        
    
    

class Gallery(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.post)

    class Meta:
        verbose_name_plural = 'Gallery'

    def thumbnail(self):
        return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit: cover;" />', self.image.url)

    thumbnail.short_description = 'Thumbnail'


class FriendRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='request_user')
    frid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    sender=models.ForeignKey(User,related_name='sender',on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,related_name='reciever',on_delete=models.CASCADE)
    status=models.CharField(max_length=100,choices=FriendRequest)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.sender)
    
    class Meta:
        verbose_name_plural='Friend Request'

class Friend(models.Model):
    fid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    user=models.ForeignKey(User,related_name='friend_user',on_delete=models.CASCADE)
    friend=models.ForeignKey(User,related_name='friend',on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.str(self.friend)
    
    class Meta:
        verbose_name_plural='Friend'
        
class Comment(models.Model):
    cid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.CharField(max_length=1000) 
    active=models.BooleanField(default=True)
    likes=models.ManyToManyField(User,blank=True,related_name='comment_likes')
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.post)
    
    class Meta:
        verbose_name_plural='comment'
        
    def comment_replies(self):
        comment_reply=ReplyComment.objects.filter(comment=self,active=True)
        return comment_reply
        
class ReplyComment(models.Model):
    rid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    user=models.ForeignKey(User,related_name='reply_user',on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    reply=models.CharField(max_length=1000) 
    active=models.BooleanField(default=True)
   
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.comment)
    
    class Meta:
        verbose_name_plural='Reply Comment'
    
class Notification(models.Model):
    nid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    user=models.ForeignKey(User,related_name='noti_user',on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.SET_NULL,null=True,blank=True)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender_user')
    notification_type=models.CharField(max_length=500,choices=NOTIFICATION_TYPE)
    comment=models.ForeignKey(Comment,max_length=1000,on_delete=models.SET_NULL,null=True,blank=True) 
    is_read=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return str(self.user)
    
    class Meta:
        verbose_name_plural='Notification'

class Group(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='group_user')
    member=models.ManyToManyField(User,related_name='members')
    name=models.CharField(max_length=300,blank=True,null=True)
    discription=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    video=models.FileField(upload_to=user_directory_path,null=True,blank=True)
    visibility=models.CharField(max_length=100,choices=VISIBLE,default='Everyone')
    gid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    active=models.BooleanField(default=True)
    slug=models.SlugField(unique=True)
    views=models.PositiveIntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.user.username
        
    def save(self,*args,**kwargs):
        uuid_key=shortuuid.uuid()
        uniqueid=uuid_key[:4]
        if self.slug=='' or self.slug==None:
            self.slug=slugify(self.title) + '-' + uniqueid
        super(Group,self).save(*args,**kwargs)
        


class GroupPost(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300,blank=True,null=True)
    image=models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    video=models.FileField(upload_to=user_directory_path,null=True,blank=True)
    visibility=models.CharField(max_length=100,choices=VISIBLE,default='Everyone')
    pid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    likes=models.ManyToManyField(User,blank=True,related_name='group_likes')
    active=models.BooleanField(default=True)
    slug=models.SlugField(unique=True)
    views=models.PositiveIntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.user.username
        
    def save(self,*args,**kwargs):
        uuid_key=shortuuid.uuid()
        uniqueid=uuid_key[:4]
        if self.slug=='' or self.slug==None:
            self.slug=slugify(self.title) + '-' + uniqueid
        super(GroupPost,self).save(*args,**kwargs)
        


    def thumbnail(self):
        return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit: cover;" />', self.image.url)

    thumbnail.short_description = 'Thumbnail'


class Page(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='page_user')
    follower=models.ManyToManyField(User,related_name='page_members')
    name=models.CharField(max_length=300,blank=True,null=True)
    discription=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    video=models.FileField(upload_to=user_directory_path,null=True,blank=True)
    visibility=models.CharField(max_length=100,choices=VISIBLE,default='Everyone')
    gid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    active=models.BooleanField(default=True)
    slug=models.SlugField(unique=True)
    views=models.PositiveIntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.user.username
        
    def save(self,*args,**kwargs):
        uuid_key=shortuuid.uuid()
        uniqueid=uuid_key[:4]
        if self.slug=='' or self.slug==None:
            self.slug=slugify(self.title) + '-' + uniqueid
        super(Page,self).save(*args,**kwargs)
        
    def thumbnail(self):
        return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit: cover;" />', self.image.url)

    thumbnail.short_description = 'Thumbnail'


class PagePost(models.Model):
    page=models.ForeignKey(Page,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300,blank=True,null=True)
    image=models.ImageField(upload_to=user_directory_path,null=True,blank=True)
    video=models.FileField(upload_to=user_directory_path,null=True,blank=True)
    visibility=models.CharField(max_length=100,choices=VISIBLE,default='Everyone')
    pid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    likes=models.ManyToManyField(User,blank=True,related_name='page_likes')
    active=models.BooleanField(default=True)
    slug=models.SlugField(unique=True)
    views=models.PositiveIntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.user.username
        
    def save(self,*args,**kwargs):
        uuid_key=shortuuid.uuid()
        uniqueid=uuid_key[:4]
        if self.slug=='' or self.slug==None:
            self.slug=slugify(self.title) + '-' + uniqueid
        super(PagePost,self).save(*args,**kwargs)
        
    def thumbnail(self):
        return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit: cover;" />', self.image.url)

    thumbnail.short_description = 'Thumbnail'

class ChatMessage(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='chat_user')
    sender=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='message_sender')
    receiver=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='message_reciever')
    message=models.CharField(max_length=10000000)
    is_read=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
    
    mid=ShortUUIDField(length=7,max_length=25,alphabet='abcdefghijklmnopqrstuvwxyz')
    
    #def __str__(self):
        #return self.sender
    
    class Meta:
        verbose_name_plural='Chat Message'
    
    