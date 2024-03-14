import re
from datetime import date
from chats.utils.openai import get_client
from chats.utils.serialize_messages import serialize_messages
from identities.models import Identity, INCOME_RANGE_CHOICES


def parse(chat, model='gpt-3.5-turbo'):
    messages = serialize_messages(chat.message_set.all())

    income_range_format = "\n".join([range[1]+":"+range[0] for range in list(INCOME_RANGE_CHOICES)])
    system_message = ('Now that you have all the information parse it and give the output in the following format\n'
                      'Name:<Name of the user>\n'
                      'DOB:<Date of birth of the user in yyyy-MM-dd format>\n'
                      'Address:<Address of the user>\n'
                      'Income Range:<Income range category of the user>\n'
                      'Type of employment:<Type of employment of the user>\n\n'
                      'Income range categories are:\n'
                      'Range:Category\n'
                      f'{income_range_format}')
    messages.append({
        'role': 'system',
        'content': system_message
    })

    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1
    )

    output = response.choices[0].message.content
    name = re.search(r"Name:(.*)\n?", output).group(1).strip()
    dob = date.fromisoformat(re.search(r"DOB:(.*)\n?", output).group(1).strip())
    address = re.search(r"Address:(.*)\n?", output).group(1).strip()
    income_range = re.search(r"Income Range:(.*)\n?", output).group(1).strip()
    type_of_employment = re.search(r"Type of employment:(.*)\n?", output).group(1).strip()

    print(name, dob, address, income_range, type_of_employment)
    identity = Identity.objects.create(full_name=name,
                                       date_of_birth=dob,
                                       address=address,
                                       income_range=income_range,
                                       type_of_employment=type_of_employment)
    chat.identity = identity
    chat.save()



