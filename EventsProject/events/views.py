from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils import timezone

from .models import Event, EventSubscribtion
from .forms import EventForm
# Create your views here.

##################  EVENT LIST AND CRUD VIEWS  ##################




def eventListView(request):
    #current time
    now = timezone.now()

    # SEARCHING EVENTS BY TITLE
    query = request.GET.get('searchQuery')
    if query:
        searchedEvents = Event.objects.filter(title__icontains=query, date__gte=now).order_by('date')

        context = {
            'query':query,
            'searchedEvents': searchedEvents,
        }
        return render(request, 'events/searchResults.html', context)

    # HOME PAGE EVENTS    
    events_list = Event.objects.filter(date__gte=now).order_by('date')

    #PAGINATING THE EVENTS FROM THE HOME PAGE
    page = request.GET.get('page', 1)
    paginator = Paginator(events_list, 3)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)    
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {'events': events}
    return render(request, 'events/eventList.html', context)




def eventDetailView(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participants_count = event.eventsubscribtion_set.all().count()

    context = {
        'event': event,
    }
    return render(request, 'events/eventDetails.html', context)




@login_required()
def eventCreateView(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        try:
            if form.is_valid():

                #adding the current user as the owner of the event
                form.instance.owner = request.user
                form.save()
                messages.info(request, "New event created successfully.")
                return redirect('events-list')    
        except ValidationError:
            messages.info(request, "The date cannot be in the past!")
            return redirect('event-create')
    context = {'form': form}
    return render(request, 'events/eventForm.html', context)




@login_required()
def eventUpdateView(request, pk):
    event = get_object_or_404(Event, id=pk)
    form = EventForm(instance=event)
    if request.user == event.owner:
        if request.method == "POST":
            form = EventForm(request.POST, request.FILES, instance=event)

            try:
                if form.is_valid():

                    #adding the current user as the owner of the event
                    form.instance.owner = request.user 
                    form.save()
                    messages.info(request, "Event updated successfully.")
                    return redirect('events-list')
                    
            except ValidationError:

                messages.info(request, 'The date cannot be in the past!')
                return redirect('event-update', event.id)
        context = {'form': form}
        return render(request, 'events/eventForm.html', context) 
    else:
        return render(request, 'ErrorPages/401.html', status=401)



@login_required()
def eventDeleteView(request, pk):
    event = get_object_or_404(Event, id=pk)
    if request.user == event.owner:
        if request.method == "POST" and request.user == event.owner:
            event.delete()
            messages.info(request, 'event deleted successfully.')
            return redirect('events-list')

        context = {'event': event}    
        return render(request, 'events/eventDelete.html', context)    
    else:
        return render(request, 'ErrorPages/401.html', status=401)



##################  END EVENT LIST AND CRUD VIEWS  ##################




@login_required
def subscribeToEventView(request, event_id):
    try:
        # getting the data needed to create an event subscribtion
        current_user = request.user
        event = get_object_or_404(Event, id=event_id)

        if request.method == "POST":
            
            subscribtion, created = EventSubscribtion.objects.get_or_create(
                participant=current_user,
                event=event
                )

            # check if the object created successfully
            if created:
                messages.info(request, 'You have subscirbed successfully to the event.')
                return redirect('events-list')
            else:
                messages.info(request, "You already a part of this event.")
                return redirect('events-list')

        else:
            # Raise 405 -Method Not Allowed- Error
            return render(request, "ErrorPages/405.html", status=405)

    except:
        messages.info(request, "Something went wrong please try again.")
        return redirect('events-list')




@login_required
def withdrawalFromEventView(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        user = request.user

        if request.method == "POST":
            event_subscribtion = get_object_or_404(EventSubscribtion, participant=user, event=event)

            event_subscribtion.delete()
            messages.info(request, 'You have sucessfully withdrawn from the event')
            return redirect('events-list')
                
        # Raise 405 -Method Not Allowed- Error
        else:
            return render(request, 'ErrorPages/405.html', status=405)
    except:
        messages.info(request, "You already not a part of this event.")
        return redirect('events-list')




#VIEW FOR MANAGEING USERS'S OWENED AND SUBSCRIBED TO EVENTS.
@login_required()
def userDashboardView(request):
    now = timezone.now()
    user = request.user

    #EVENTS THE USER SUBSCRIBED TO.
    SubedEvents = user.eventsubscribtion_set.filter(participant=user)

    # EVENTS THE USER OWEN.
    userOwnedEvents = user.event_set.filter(owner=user, date__gte=now).order_by('date')
    context = {
        'SubedEvents': SubedEvents,
        'userOwnedEvents': userOwnedEvents
        }
    return render(request, 'events/userDashboard.html', context)
