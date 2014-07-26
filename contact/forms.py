# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage

#DEFAULT_FROM_EMAIL = 'talkmill@gmail.com'
#SERVER_EMAIL = 'talkmill@gmail.com'


class ContactForm(forms.Form):
    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_action = ""
    helper.add_input(Submit('submit', 'Submit'))

    #helper.form_tag = False
    namn = forms.CharField()
    meddelande = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(label='Din E-mailadress')
    cc_myself = forms.BooleanField(required=False,label='Vill du ha en kopia på mailet?')
    def send_email(self):
        subject = "Contact incoming from " + self.cleaned_data['namn']
        message = self.cleaned_data['meddelande']
        sender = self.cleaned_data['sender']
        cc_myself = self.cleaned_data['cc_myself']

        recipients = ['makeover@litheblas.org']
        if cc_myself:
            recipients.append(sender)
        email = EmailMessage(subject, message,sender, recipients)
        email.send()
        return HttpResponseRedirect('/')



