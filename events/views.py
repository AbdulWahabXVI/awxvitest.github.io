from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm

from django.core.paginator import Paginator



def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    
    return render(
        request,
        'events/update_event.html',
        {
            'event': event,
            'form': form
        }
    )

def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted-TRUE')

    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(
        request,
        'events/add_event.html',
        {
            'form': form,
            'submitted': submitted
        }
    )

    form = VenueForm
    return render(
        request,
        'events/add_venue.html',
        {
            'form': form
        }
    )

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    
    return render(
        request,
        'events/update_venue.html',
        {
            'venue': venue,
            'form': form
        }
    )

def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(
            request,
            'events/search_venues.html',
            {
               'searched':searched,
               'venues':venues
            }
        )
    else:
        return render(
            request,
            'events/search_venues.html',
            {
                
            }
        )

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(
        request,
        'events/show_venue.html',
        {
            'venue': venue
        }
    )

def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    
    p = Paginator(Venue.objects.all(), 8)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    return render(
        request,
        'events/venue.html',
        {
            'venue_list': venue_list,
            'venues': venues,
            'nums': nums
        }
    )

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted-TRUE')

    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(
        request,
        'events/add_venue.html',
        {
            'form': form,
            'submitted': submitted
        }
    )

    form = VenueForm
    return render(
        request,
        'events/add_venue.html',
        {
            'form': form
        }
    )

def all_events(request):
    event_list = Event.objects.all().order_by('-event_date', 'name')

    p = Paginator(Event.objects.all(), 2)
    page = request.GET.get('page')
    events = p.get_page(page)
    nums = "a" * events.paginator.num_pages

    return render(
        request,
        'events/event_list.html',
        {
            'event_list': event_list,
            'events': events,
            'nums': nums
        }
    )

def home(
    request,
    year=datetime.now().year,
    month=datetime.now().strftime('%B')
    ):
    name = "Wahab"
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )

    now = datetime.now()
    current_year = now.year

    time = now.strftime('%I:%M %p')
    return render(
        request,
        'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
    })
