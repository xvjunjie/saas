from django.urls import path

from users import views
from users.views import UsersView

app_name = 'users'

urlpatterns = [
    path('add/', views.add, name='add'),
    path('select/', views.select, name='select'),
    # path('delete/', views.delete, name='delete'),
    # path('update/', views.update, name='update')
]