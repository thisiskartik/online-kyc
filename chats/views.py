from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from chats.models import Chat
from chats.utils.invoke import invoke
from chats.serializers import ChatSerializer


@api_view(['POST'])
def create_chat(request):
    new_chat = Chat.objects.create()

    system_message = ('Your job is to first greet the user and then get the '
                      'user\'s Full name, DOB, Address, Income range, and Type of employment. '
                      'One by one ask the question to the user. '
                      f'Once you have all the information reply with \'{new_chat.id}\'')
    invoke(new_chat, system_message, 'system')

    return Response(ChatSerializer(new_chat).data, status=HTTP_201_CREATED)


@api_view(['POST'])
def invoke_chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    invoke(chat, request.data.get('message'), 'user')
    return Response(ChatSerializer(chat).data, status=HTTP_200_OK)

