from django.urls import path
from .views import (
    feedback_list,
    feedback_create,
    feedback_edit,
    feedback_delete,
    FeedbackDeleteMultipleView,
    home,
    all_feedbacks
    
)
from . import views


urlpatterns = [
    # path('', home, name='home'),  # Page d'accueil
    path('', feedback_list, name='feedback_list'),
    path('create/', feedback_create, name='feedback_create'),
    path('edit/<int:id>/', feedback_edit, name='feedback_edit'),
    path('delete/<int:pk>/', feedback_delete, name='feedback_delete'),
    path('bulk_delete/', FeedbackDeleteMultipleView.as_view(), name='bulk_delete_feedback'),
    path('all/', all_feedbacks, name='all_feedbacks'),  # URL pour tous les feedbacks

    path('statistics/', views.feedback_statistics, name='feedback_statistics'),
]



