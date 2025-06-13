from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at', 'updated_at')  # Affiche ces champs dans la liste d'administration
    search_fields = ('user__username', 'comment')  # Ajoute un champ de recherche par nom d'utilisateur et commentaire
    list_filter = ('created_at', 'updated_at')  # Ajoute des filtres par date de création et de mise à jour

