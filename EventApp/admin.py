from django.contrib import admin
from django.contrib import admin

from .models import Event,Seat,Booking
# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_title', 'event_Type', 'description', 'start_date','end_date','location','affiche')
    ordering = ('event_title', 'start_date')
    list_per_page = 3
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Event Details', {
            'fields': ('event_title', 'event_Type', 'description')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Location', {
            'fields': ('location',),
        }),
        ('Documents', {
            'fields': ('affiche',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    
    
    search_fields = ('title', 'location',)

admin.site.register(Event, EventAdmin)


admin.site.register(Seat)
admin.site.register(Booking)