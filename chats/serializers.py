from rest_framework.serializers import ModelSerializer
from chats.models import Chat, Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'role', 'created_at')


class ChatSerializer(ModelSerializer):
    messages = MessageSerializer(many=True, source='message_set')

    class Meta:
        model = Chat
        fields = ('id', 'identity', 'messages')
