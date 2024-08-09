from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.serializers import CreateChatRoomSerializer, AddMessageSerializer, AllChatRoomsSerializer, \
    GetAllMessagesSerializer, MyTokenObtainPairSerializer
from chat.models import ChatRoom, Message


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class CreateChatRoomView(CreateAPIView):
    queryset = ChatRoom.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateChatRoomSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddMessageView(CreateAPIView):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AddMessageSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AllChatRoomsListView(ListAPIView):
    queryset = ChatRoom.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AllChatRoomsSerializer


class GetMessagesListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GetAllMessagesSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Message.objects.filter(room__user__id=user_id)
