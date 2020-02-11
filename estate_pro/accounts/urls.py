from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name ='signup'),
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html'), name = 'password_change'),
    path('change_password/success/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_success.html'),
        name = 'password_change_done'),
    path('<int:pk>/details/', views.UserDetailsView.as_view(), name='details_view'),
    path('<int:pk>/details/edit/', views.DetailsUpdate.as_view(), name='details_update'),
    path('chat/', views.InboxChatView.as_view(), name='chat'),
    path('chat/<int:pk>/reply/', views.ChatReplyView.as_view(), name='chat_details'),
]
