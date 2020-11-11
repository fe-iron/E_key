from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField
from django.db.models import Q
import json


def create_multiple(usernames, fname, user, body):
    for i in usernames:
        if User.objects.filter(email=i).exists():
            reci = User.objects.get(email=i)
            msg = MessageModel(recipient=reci, body=body, user=user, first_name=fname)
            msg.save()
    return msg


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        flag = False
        try:
            usernames = json.loads(validated_data['recipient']['username'])
            flag = True
        except json.JSONDecodeError as e:
            pass

        user = self.context['request'].user
        fname = User.objects.filter(Q(username=user) | Q(email=user))
        fname = fname[0].first_name

        if flag:
            msg = create_multiple(usernames, fname, user, validated_data['body'])
        else:
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
