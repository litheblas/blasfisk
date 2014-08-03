from django.shortcuts import render
from contact.forms import ContactForm
from django.views.generic.edit import FormView


# Create your views here.

class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'

    def form_valid(self, form):
        form.send_email()
        return super(ContactFormView, self).form_valid(form)