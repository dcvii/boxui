from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('karma/', views.karma_interaction, name='karma_interaction'),
    path('karma/<int:comment_id>/', views.get_comment_karma, name='get_comment_karma'),
]

