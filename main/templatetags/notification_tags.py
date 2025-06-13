from django import template

register = template.Library()

@register.filter
def has_unread_notifications(user):
    if user.is_authenticated:
        return user.notifications.filter(read=False).exists()
    return False
