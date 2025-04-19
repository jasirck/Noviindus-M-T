from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),


]
