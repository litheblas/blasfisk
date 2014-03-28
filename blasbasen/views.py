from django.shortcuts import render
from django.http import Http404
from blasbasen.models import Person

# Create your views here.
def index(request):
    return render(request, 'page.html')

def person_detail(request, person):
    try:
        p = Person.objects.get(pk=person)
    except Person.DoesNotExist:
        raise Http404
    
    a = p.assignment_set.select_related('post').all().order_by('-start_date')
    memberships = a.filter(post__engagement=False).filter(post__membership=True)
    engagements = a.filter(post__engagement=True)
    
    return render(request, 'person_detail.html', {'person': p, 'memberships': memberships, 'engagements': engagements})