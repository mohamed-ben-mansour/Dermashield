
# models.py
from django.db import models
from django.conf import settings
from textblob import TextBlob  # Exemple d'utilisation de TextBlob pour l'analyse de sentiment

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gif_url = models.URLField(blank=True, null=True)  # Champ pour le GIF
    sentiment = models.CharField(max_length=20, blank=True, null=True)  # Champ sentiment ajouté
    rating = models.IntegerField(
        null=True,  # Permet à la note d'être nulle
        blank=True,  # Permet à la note d'être laissée vide dans les formulaires
        default=0,  # Note par défaut
        choices=[(i, f'{i} étoile{"s" if i > 1 else ""}') for i in range(1, 6)]
    )

    def __str__(self):
        return f'{self.user.username}: {self.comment[:20]}'

    def analyze_sentiment(self):
        from textblob import TextBlob
        analysis = TextBlob(self.comment)
        sentiment_score = analysis.sentiment.polarity
        if sentiment_score > 0:
            return "Positif"
        elif sentiment_score < 0:
            return "Négatif"
        else:
            return "Neutre"



