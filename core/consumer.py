from asgiref.sync import sync_to_async
from channels.generic.websocket import WebSocketConsumer
from userauths.models import User,Profile
import json

from core.models import ChatMessage


class ChatConsumer(WebSocketConsumer):
    def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s' % self.room_name
        
        sync_to_async(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
    def disconnect(self):
        
         sync_to_async(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
         
    def receive(self,text_data):
        data=json.loads(text_data)
        message=data.get('message')
        sender_username=data.get('sender')
        
        try:
            sender=User.objects.get(username=sender_username)
            profile=Profile.objects.get(user=sender)
            profile_image=profile.image.url
        except User.DoesNotExist:
            profile_image=''
        
        receiver=User.objects.get(username=data['receiver'])
        chat_message=ChatMessage(sender=sender,receiver=receiver,message=message)
        
        chat_message.save()
        
        sync_to_async(self.channel_layer.group_send)(
            
            self.room_group_name,
            {
                'type':'chat_message',
                'sender':'sender',
                'receiver':'receiver',
                'profile_image':'profile_image'
                
            }
            
        )
        
        
    def chat_message(self,event):
        self.send(text_data=json.dumps(event))