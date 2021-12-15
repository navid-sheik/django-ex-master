import django
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from mainapp import views

from mainapp.api import accept_request, add_new_hobby, create_new_hobby, decline_request, delete_hobby_from_user, friends_api, get_current_user_hobby, get_friends_requests, send_friends_request, filters_api, update_user_info

app_name =  'mainapp'
urlpatterns = [

    path('', views.profile, name="profile"),
    path('register/', views.register_auth, name="register"),
    path('login/', views.login_auth, name="login"),
    path('logout/', views.logout_auth, name="logout"),
    #Requests and display friends
    path('requests/', views.friends_requests, name="requests"),
    path('friends/', views.friends, name="friends"),
    path('api/friends', friends_api, name="friends_api"),
    #Hobby api 
    path('api/myhobbies', get_current_user_hobby, name="current_hobbies"),
    path('api/createhobby', create_new_hobby, name="create_new_hobby"),
    path('api/addhobby', add_new_hobby, name="add_new_hobby"),
    path('api/deleteHobby/<int:hobby_id>/', delete_hobby_from_user, name="delete_hobby"),
    #Friend requests
    path('api/getFriendsRequests', get_friends_requests, name="friends_requests"),
    path ('api/sendFriendRequest/<int:to_user_id>', send_friends_request, name=  "send_friend_request"),
    path('api/acceptRequest', accept_request,name="accept_request"),
    path('api/declineRequest', decline_request,name="decline_request"),

    path('api/filters', filters_api, name="filters_api"),

    path('api/updateProfile', update_user_info, name="update_user")

    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)