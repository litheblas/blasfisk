# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings

#DEFAULT_FROM_EMAIL = 'talkmill@gmail.com'
#SERVER_EMAIL = 'talkmill@gmail.com'

class ContactForm(forms.Form):
    sender_name = forms.CharField(label=_('Your name'))
    sender_email = forms.EmailField(label=_('Your email address'))
    subject = forms.ChoiceField(choices=settings.CONTACT_SUBJECTS, label=_('Subject'))
    message = forms.CharField(widget=forms.Textarea, label=_('Message'))
    # sender_cc = forms.BooleanField(required=False, label=_('Send a copy to you'))


    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.html5_required = True
        self.helper.add_input(Submit('submit', _('Send')))

    def resolve_recipients(self):
        """
        Returns a list of recipients.
        """
        subject = self.cleaned_data['subject']
        return settings.CONTACT_SUBJECT_RECIPIENTS[subject]

    def send_email(self):
        sender_email = self.cleaned_data['sender_email']
        subject = _('Message from %(name)s') % {'name': self.cleaned_data['sender_name']}
        message = self.cleaned_data['message']

        # cc_email = [sender_email] if self.cleaned_data['sender_cc'] else None

        email = EmailMessage(
            to=self.resolve_recipients(),
            # cc=cc_email,
            from_email=sender_email,
            subject=subject,
            body=message,
        )

        email.send()



