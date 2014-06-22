# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from blasbasen.models import Person, Section, Post
from globals import COUNTRIES

class SectionList(ListView):
    model = Section
    context_object_name = 'sections'

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
        
        # Här definieras alla filter. Skriv ett nytt här så genereras det HTML automatiskt.
        # Om det behövs fler sätt att filtrera personer på, rekommenderar jag att man skriver en metod till PersonManager.
        # Det är så jag gjort befintliga filter, så kör man bara en .filter(pk__in=Person.objects.hokuspokus()).
        context['filters'] = []
        context['filters'].append({'id': 'members',
                                   'name': u'Blåsare',
                                   'default': True, # Avgör vilken flik som är förvald. Får bara finnas på ett filter.
                                   'content': context['people'].filter(pk__in=Person.objects.members())})
        context['filters'].append({'id': 'active',
                                   'name': u'Aktiva',
                                   'content': context['people'].filter(pk__in=Person.objects.active())})
        context['filters'].append({'id': 'oldies',
                                   'name': u'Gamlingar',
                                   'content': context['people'].filter(pk__in=Person.objects.oldies())})
        context['filters'].append({'id': 'others',
                                   'name': u'Löst folk',
                                   'content': context['people'].filter(pk__in=Person.objects.others())})
        context['filters'].append({'id': 'all',
                                   'name': u'Alla',
                                   'content': context['people']})
        
        context['sections'] = Section.objects.all().order_by('name')
        context['posts'] = Post.objects.all().order_by('name').order_by('section')
        context['countries'] = COUNTRIES
        
        if self.request.GET:
            #Hämtar alla GET-parametrar men tar bort sort och tab. Används av "sorterings-väljaren" för att behålla alla sökparametrar.
            
            #GET är immutable, så vi kopierar den istället
            get_params = self.request.GET.copy()
            
            if 'sort' in get_params:
                get_params.__delitem__(u'sort')
            
            if 'tab' in get_params:
                get_params.__delitem__(u'tab')
                
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