# forum/urls.py
from django.urls import path
from . import views
from forum.views import home

app_name = 'forum'  # Allows namespacing, so you can use 'forum:forum_list' in redirects

urlpatterns = [
    path('', views.forum_list, name='forum_list'),                    # List all forums
    path('<int:forum_id>/', views.forum_detail, name='forum_details1'), # View details of a specific forum
    path('create/', views.forum_create, name='forum_create'),         # Create a new forum
    path('<int:forum_id>/edit/', views.forum_update, name='forum_update'), # Update an existing forum
    path('<int:forum_id>/delete/', views.forum_delete, name='forum_delete'), # Delete a forum
    path('comment/<int:comment_id>/delete/confirm/', views.delete_comment, name='onfirm_delete_comment'),
    path('comment/<int:comment_id>/reply/', views.reply_to_comment, name='reply_to_comment'),
    path('delete-response/<int:response_id>/', views.delete_response, name='delete_response'),
    path('upvote/<int:forum_id>/', views.upvote_forum, name='upvote_forum'),





    

]

