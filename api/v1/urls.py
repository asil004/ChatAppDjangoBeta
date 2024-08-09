from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from api.v1.views import CreateChatRoomView, AddMessageView, AllChatRoomsListView, GetMessagesListView, \
    MyObtainTokenPairView

urlpatterns = [
    path('auth/', include([
        path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
        path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
    path('create/', include([
        # user apis
        path('chatroom/', CreateChatRoomView.as_view(), name='create_chatroom'),
        path('message/', AddMessageView.as_view(), name='add_message'),
    ])),
    path('get/', include([
        # superadmin apis
        path('chatrooms/', AllChatRoomsListView.as_view(), name='all_chatrooms'),
        path('messages/<int:user_id>', GetMessagesListView.as_view(), name='get_messages'),
    ])),
]
