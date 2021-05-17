from django.db import models

class Message(models.Model):
    messageBody = models.CharField(max_length=300)
    def __str__(self):
        return "message info"

#Customers
class Customer(models.Model):
    name = models.CharField(max_length=255, blank="False")
    phone_primary = models.CharField(max_length=29, blank="False")
    def __str__(self):
        return self.name


class Conversation(models.Model):
    conversationId = models.CharField(max_length=255, blank="False")
    phone_customer = models.CharField(max_length=29, blank="False")
    phone_one = models.CharField(max_length=29, blank="False")
    phone_two = models.CharField(max_length=29, blank="False")
    state = models.IntegerField()
    contactId = models.CharField(max_length=255, blank="False")
    channelId = models.CharField(max_length=255, blank="False")

    def __str__(self):
        return self.conversationId