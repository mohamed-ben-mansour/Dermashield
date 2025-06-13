from django.shortcuts import render
from .models import Event
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse


# Create your views here.
# def eventList(request):
#     list = Event.objects.all()
#     return render(request, 'events/event_list.html', {
#         'list' : list
#     })
    
    
from .models import Event
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Seat, Booking

from django.contrib.auth import get_user_model
from django.db.models import Q

    
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'EventApp/event_detail.html'
    context_object_name = 'event'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer les réservations associées à cette conférence
        return context
        
    
class EventListView(ListView):
    model = Event
    template_name = 'EventApp/event_list.html'
    context_object_name='list'
    def get_queryset(self):
        # Get the search query and sort order from GET parameters
        search_query = self.request.GET.get('search', '')
        sort_order = self.request.GET.get('sort', 'asc')  # Default is 'asc' for ascending order

        # Start with all events
        events = Event.objects.all()

        # If there's a search query, filter events
        if search_query:
            events = events.filter(
                Q(event_title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Sort the events based on the sort order
        if sort_order == 'asc':
            events = events.order_by('start_date')
        elif sort_order == 'desc':
            events = events.order_by('-start_date')

    

        return events

    def get_context_data(self, **kwargs):
        # Get the context from the superclass
        context = super().get_context_data(**kwargs)

        # Add search query and sort order to the context
        search_query = self.request.GET.get('search', '')
        sort_order = self.request.GET.get('sort', 'asc')

        context['search_query'] = search_query
        context['sort_order'] = sort_order

        return context
    
    
 
#def index(request):
 #   return render(request, 'EventApp/index.html')   
 
 
 
 
from django.shortcuts import render, get_object_or_404
from .models import Event
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.db.models import Q
from .models import Event

@login_required
def event_list(request):
    search_query = request.GET.get('search', '')
    sort_order = request.GET.get('sort', 'asc')  # Default is 'asc' for ascending order

    # Filter events based on search query
    events = Event.objects.filter(
        Q(event_title__icontains=search_query) |
        Q(description__icontains=search_query)
    ) if search_query else Event.objects.all()

    # Sort events based on start date
    if sort_order == 'asc':
        events = events.order_by('start_date')
    elif sort_order == 'desc':
        events = events.order_by('-start_date')

    if request.user.is_authenticated and request.user.new_event:
        request.user.new_event = False
        request.user.save()
        
    return render(request, 'events/event_list.html', {
        'events': events,
        'search_query': search_query,
        'sort_order': sort_order
    })











def event_seating(request, event_id):
    # Fetch the event and its related seats
    event = get_object_or_404(Event, id=event_id)
    seats = event.seats.all()

    # Calculate total seats, available seats, and booked seats
    total_seats = seats.count()
    available_seats = seats.filter(is_booked=False).count()
    booked_seats = total_seats - available_seats

    # Pass the calculated values to the template
    return render(request, 'EventApp/event_seating.html', {
        'event': event,
        'seats': seats,
        'total_seats': total_seats,
        'available_seats': available_seats,
        'booked_seats': booked_seats
    })

    



# views.py
 # Add this import

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

def book_seat(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    if seat.is_booked:
        return render(request, 'error.html', {'message': 'Seat already booked.'})
    
    # If it's a GET request, show the confirmation page
    if request.method == 'GET':
        return render(request, 'confirm_booking.html', {'seat': seat})

    # If it's a POST request, process the booking
    elif request.method == 'POST':
        # Create a booking for the user
        booking = Booking.objects.create(user=request.user, seat=seat)
        
        # Mark the seat as booked
        seat.is_booked = True
        seat.save()

        # Redirect to the event seating page after successful booking
        return redirect('events:event_seating', event_id=seat.event.id)




def event_list(request):
    # Get the search query from the request
    search_query = request.GET.get('search', '')
    
    # Filter events based on the search query
    events = Event.objects.filter(
        Q(event_title__icontains=search_query) | 
        Q(description__icontains=search_query)
    ) if search_query else Event.objects.all()

    # Pass search query and events to the template
    context = {
        'events': events,
        'search_query': search_query,
    }
    return render(request, 'events/event_list.html', context)








from django.db.models import Count, Q
from django.shortcuts import render
from .models import Event, Booking

def event_statistics(request):
    # Aggregate the number of booked seats for each event type
    stats = (
        Event.objects.filter(seats__is_booked=True)
        .values('event_Type')
        .annotate(booked_count=Count('seats__id', filter=Q(seats__is_booked=True)))
    )
    
    # Convert the result into a format suitable for the template
    event_types = [entry['event_Type'] for entry in stats]
    booked_counts = [entry['booked_count'] for entry in stats]
    
    context = {
        'event_types': event_types,
        'booked_counts': booked_counts,
    }
    return render(request, 'admin/EventApp/event.html', context)
  