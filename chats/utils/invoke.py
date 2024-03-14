from chats.utils.openai import get_client
from chats.utils.serialize_messages import serialize_messages
from chats.utils.parse import parse
from chats.models import Message


def invoke(chat, message, role, model='gpt-3.5-turbo'):
    Message.objects.create(chat=chat, message=message, role=role)

    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=serialize_messages(chat.message_set.all())
    )

    response_message = response.choices[0].message
    Message.objects.create(chat=chat, message=response_message.content, role=response_message.role)

    if str(chat.id) in response_message.content:
        parse(chat, model)
