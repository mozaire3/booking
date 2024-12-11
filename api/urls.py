from django.urls import path


from .views import Login,auth2,Rooms,Hotels,Hotel,Room,RoomsOne,Logout,Register,Users,User,Payment,Payments



urlpatterns = [
   
    path('auth/register/',Register.as_view(),name='get_user'),
    path('auth/login/',Login.as_view(),name='get_user'),
    path('users/',Users.as_view(),name='create_user'),
    path('users/<int:pk>/',User.as_view(),name='get_user'),
    path('hotel/',Hotels.as_view(),name='courses'),
    path('hotel/<int:pk>/',Hotel.as_view(),name='courseid'),
    path('payment/',Payments.as_view(),name='payments'),
    path('payment/<int:pk>/',Payment.as_view(),name='payment'),
    path('auth/logout/',Logout.as_view(),name='logout'),
    path('rooms/',Rooms.as_view(),name='course_contents'),
    path('roomsone/<int:courseId>',RoomsOne.as_view(),name='course_contentsOne'),
    path('rooms/<int:pk>/', Room.as_view(),name='detail_course_content'),
    path('auth02/',auth2.as_view(),name="auth")
]

