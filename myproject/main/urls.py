from django.urls import path
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', HomeClass.as_view(), name='home'),  # Главная страница
    path('form/', RegisterView.as_view(), name='form'),  # Страница с формой
    path('users/', UserListClass.as_view(), name='users_list'),  # Страница пользователей
    path('detail/<int:id>/', UserDetailClass.as_view(), name='user_detail'),  # Страница детализации
    path('edit/<int:id>/', EditRecordClass.as_view(), name='edit_record'),  # Страница редактирования
    path('users/delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)