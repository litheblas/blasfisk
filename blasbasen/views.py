from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, TemplateView
from blasbasen.models import Person

# Create your views here.

def person_detail(request, person):
    try:
        p = Person.objects.get(pk=person)
    except Person.DoesNotExist:
        raise Http404
    
    a = p.assignment_set.select_related('post').all().order_by('-start_date')
    memberships = a.filter(post__engagement=False).filter(post__membership=True)
    engagements = a.filter(post__engagement=True)
    
    return render(request, 'blasbasen/person_detail.html', {'person': p, 'memberships': memberships, 'engagements': engagements})

class PersonList(ListView):
    model = Person
    context_object_name = 'people'