from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import FriendRequest,User,Message
from django.db.models import Q


class FriendFilter(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        request = self.context["request"]
        friends = FriendRequest.objects.filter(Q(askTo=request.user) & Q(approved=True))

        list_friend = []
        for friend in friends:
            list_friend.append(friend.askFrom.id)
        queryset = User.objects.filter(id__in=list_friend)
        return queryset


class MessageSerializer(serializers.ModelSerializer):

    receiver = FriendFilter()

    class Meta:
        model = Message
        fields = ("id","sender","receiver","message")
        extra_kwargs = {"sender": {"read_only": True}}