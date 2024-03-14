def serialize_messages(messages):
    serialized_messages = []
    for message in messages:
        serialized_messages.append({
            'role': message.role,
            'content': message.message
        })
    return serialized_messages
