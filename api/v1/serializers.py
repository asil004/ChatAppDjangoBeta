from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from chat.models import ChatRoom, Message


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class CreateChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
        read_only_fields = ['user']


class AddMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['author']


class AllChatRoomsSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class GetAllMessagesSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
