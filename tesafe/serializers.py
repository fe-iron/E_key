from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import MessageModel, Seller, Tester
from rest_framework.serializers import ModelSerializer, CharField
from django.db.models import Q


# def create_multiple(user, body):
#     data = get()
#     print("get: ", data)
#     recipients = data[0]
#     for reci in recipients:
#         print("reci: ",reci)
#         if User.objects.filter(email=reci).exists():
#             usr = User.objects.filter(email=reci)
#             fname = usr[0].first_name
#             if MessageModel.objects.filter(recipient=usr[0], body=body, user=user).exists():
#                 pass
#             else:
#                 msg = MessageModel(recipient=usr[0], body=body, user=user, first_name=fname)
#                 msg.save()
#                 print("saved")
#

class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        print("data: ", validated_data)
        user = self.context['request'].user
        fname = User.objects.filter(Q(username=user) | Q(email=user))
        fname = fname[0].first_name
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user,
                           first_name=fname)
        msg.save()
        return msg


    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body', 'first_name')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
