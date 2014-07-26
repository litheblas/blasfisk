from django.shortcuts import render
from django.views.generic import ListView
from events.models import Event

# Create your views here.


class EventList(ListView):
    model = Event
    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        # Nedan skapas bara en array
        context['event_list'] = Event.objects.future().public()
        return context