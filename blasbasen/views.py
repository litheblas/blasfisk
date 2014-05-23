# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from blasbasen.models import Person, Section, Post

class PersonList(ListView):
    context_object_name = 'people'
    
    def simple_search(self, queryset, name):
        return queryset.filter(Q(first_name__icontains=name) | 
                               Q(nickname__icontains=name) |
                               Q(last_name__icontains=name))
    
    def get_queryset(self):
        queryset = Person.objects.all()
        #Sökning
        if self.request.GET.get('search') == 's':
            queryset = self.simple_search(queryset, self.request.GET.get('name'))
        
        elif self.request.GET.get('search') == 'a':
            queryset = (self.simple_search(queryset, self.request.GET.get('name')).
                        filter(gender__contains=self.request.GET.get('gender')))
            
            if not self.request.GET.get('w_login'):
                queryset = queryset.exclude(user=True)
            
            if not self.request.GET.get('wo_login'):
                queryset = queryset.exclude(user=None)
        
        if self.request.GET.get('sort'):
            return queryset.order_by(self.request.GET.get('sort'))
        else:
            return queryset
        
    def get_context_data(self, **kwargs):
        context = super(PersonList, self).get_context_data(**kwargs)
        
        context['filters'] = []
        context['filters'].append({'id': 'all',
                                   'name': 'Alla',
                                   'default': True,
                                   'content': context['people']})
        context['filters'].append({'id': 'active',
                                   'name': 'Aktiva',
                                   'content': context['people'].filter(id=Person.objects.active())}) #Lite besvärligt att sortera ut eftersom context['people'] är en QuerySet. Bättre lösning välkomnas
        context['filters'].append({'id': 'oldies',
                                   'name': 'Gamlingar',
                                   'content': context['people'].filter(id=Person.objects.oldies())})
        context['filters'].append({'id': 'honorary',
                                   'name': 'Hedersmedlemmar',
                                   'content': context['people']}) #TODO: Filtrera ut endast hedersmedlemmar
        context['filters'].append({'id': 'others',
                                   'name': 'Löst folk',
                                   'content': context['people']}) #TODO: Filtrera ut endast löst folk
        
        context['sections'] = Section.objects.all().order_by('name')
        context['posts'] = Post.objects.all().order_by('name').order_by('section')
        
        if self.request.GET:
            #Hämtar alla GET-parametrar men tar bort sort. Används av "sorterings-väljaren" för att behålla alla sökparametrar.
            
            #GET är immutable, så vi kopierar den istället
            get_params = self.request.GET.copy()
            
            if get_params['sort']:
                get_params.__delitem__(u'sort')
            context['search_params'] = get_params
        
        return context

class PersonDetail(DetailView):
    model = Person
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PersonDetail, self).get_context_data(**kwargs)

        a = context['person'].assignment_set.select_related('post').all().order_by('-start_date')
        context['memberships'] = a.filter(post__engagement=False).filter(post__membership=True)
        context['engagements'] = a.filter(post__engagement=True)
        return context

class PersonAdd(CreateView):
    model = Person

class PersonChange(UpdateView):
    model = Person