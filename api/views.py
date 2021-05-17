from django.http import HttpResponse
from django.views import View
import json
from .models import Conversation, Customer
from decouple import config
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie, csrf_protect
import messagebird
from messagebird.conversation_message import MESSAGE_TYPE_TEXT
from django.shortcuts import get_object_or_404

class ping(View):

    def get(self, request):
        return HttpResponse('CSV Spammer backend is up and running' )


#@csrf_exempt
#@ensure_csrf_cookie
class SendWhatsAppMessageView(View):

    def post(self,request):
        data = json.loads(request.body)
        to = data['to']
        message = data['message']

        try:
            conversation = Conversation.objects.get(phone_two=to)
        except:
            conversation = None

        print(str(conversation.contactId))

        try:
            message_bird_key = config("message_bird_key")
            # Create the client with the whatsapp specs
            client = messagebird.Client(message_bird_key,
                                        features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])

            # msg = client.message_create('FromMe', '+50375561351', 'Hello World', {'reference': 'Foobar'})
            msgResponse = client.conversation_create_message(conversation.conversationId, {
                'channelId': conversation.channelId,
                'type': MESSAGE_TYPE_TEXT,
                'content': {
                    'text': message
                }
            })

            balance = client.balance()
        except messagebird.client.ErrorException as e:
            for error in e.errors:
                print('  code        : %d' % error.code)
                print('  description : %s' % error.description)
                print('  parameter   : %s\n' % error.parameter)

        return HttpResponse('Response from message sent' + str(msgResponse))



class webhookMessageBird(View):

    def post(self,request):
        data = json.loads(request.body)

        conversationId = data['conversation']['id']
        try:
            conversation = Conversation.objects.get(conversationId=conversationId)
        except:
            conversation = None


        #conversation = get_object_or_404(Conversation, conversationId=conversationId)
        if conversation:
            print("Conversation already exists")
        else:
            conversationId=data['conversation']['id']
            phone_one=data['message']['to']
            phone_two=data['message']['from']
            channel_id = data['message']['channelId']
            contactId=data['conversation']['contactId']
            phone_customer=data['contact']['msisdn']
            #Mark all previous conversations into inactive state
            conversationsCustomer = Conversation.objects.filter(phone_customer=phone_customer)
            for conversation in conversationsCustomer:
                conversation.state = 0
                conversation.save()

            Conversation.objects.create(conversationId=conversationId,phone_customer=phone_customer,phone_one=phone_one,
                                        phone_two=phone_two,state=1,contactId=contactId,channelId=channel_id)



        print("conversation id " + str(json.loads(request.body)))

        return HttpResponse('Response from message sent' + str(json.loads(request.body)))


class getConversationHistory(View):

    def get(self, request):

        data = json.loads(request.body)
        conversationId = data['conversationId']
        phone_customer = data['phone-customer']

        #Get the information by phone number:
        conversationsCustomer = Conversation.objects.filter(phone_customer=phone_customer)

        for conversation in conversationsCustomer:
            print(conversation.contactId)

        for conversation in conversationsCustomer:
            conversation.state = 6
            conversation.save()

        for conversation in conversationsCustomer:
            print(conversation.state)


        return HttpResponse('Response from message sent' )

        #To retrieve conversation history
        # try:
        #     message_bird_key = config("message_bird_key")
        #     # Create the client with the whatsapp specs
        #     client = messagebird.Client(message_bird_key)
        #     conversationList=client.conversation_list()
        #     # Print the object information.
        #     print('The following information was returned as a Conversation List object:')
        #     print(conversationList)
        #
        # except messagebird.client.ErrorException as e:
        #     print('An error occured while requesting a Message object:')
        #
        #     for error in e.errors:
        #         print('  code        : %d' % error.code)
        #         print('  description : %s' % error.description)
        #         print('  parameter   : %s\n' % error.parameter)
        #
        #
        # try:
        #     message_bird_key = config("message_bird_key")
        #     client = messagebird.Client(message_bird_key,features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])
        #
        #     conversation = client.conversation_read(conversationId)
        #
        #     # Print the object information.
        #     print('The following information was returned as a Conversation object:')
        #     print(conversation)
        #
        # except messagebird.client.ErrorException as e:
        #     print('An error occured while requesting a Conversation object:')
        #
        #     for error in e.errors:
        #         print('  code        : %d' % error.code)
        #         print('  description : %s' % error.description)
        #         print('  parameter   : %s\n' % error.parameter)
        #
        # return HttpResponse('Response from message sent')

#Sample code
# try:
#     message_bird_key = config("message_bird_key")
#     # Create the client with the whatsapp specs
#     client = messagebird.Client(message_bird_key,
#                                 features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])
#
#     # msg = client.message_create('FromMe', '+50375561351', 'Hello World', {'reference': 'Foobar'})
#     msg = client.conversation_create_message('6a0e6c96824e47b1856610de7bbe86a4', {
#         'channelId': '67a5b4063e174ab6acdcdb3ceb07f7ff',
#         'type': MESSAGE_TYPE_TEXT,
#         'content': {
#             'text': whatsAppMessageBody
#         }
#     })
#
#     balance = client.balance()
#
#     data = {"alphaa": whatsAppMessageBody, "alphab": 2, "balance-amount": balance.amount,
#             "balance-type": balance.type, "message-details": msg.conversationId}
#     return JsonResponse(data, safe=False)  # or JsonResponse({'data': data})
# except messagebird.client.ErrorException as e:
#     for error in e.errors:
#         print('  code        : %d' % error.code)
#         print('  description : %s' % error.description)
#         print('  parameter   : %s\n' % error.parameter)