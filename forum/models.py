from django.db import models
from django.conf import settings
import re
from django.contrib.auth import get_user_model



class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    date_creation = models.DateField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)  # Add this field for upvotes

    def __str__(self):
        return self.title


class Comment(models.Model):
    forum = models.ForeignKey(Forum, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_likes', blank=True)  # Liste des utilisateurs qui ont liké
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='responses')  # "responses" for replies


    # Nombre total de likes pour un commentaire
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.forum.title}"






class Response(models.Model):
    comment = models.ForeignKey(Comment, related_name='responses_on_comment', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user.username} to {self.comment.user.username}'s comment"
