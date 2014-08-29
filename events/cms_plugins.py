# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from events.models import Event, EventViewer


class PublicEventViewerPlugin(CMSPluginBase):
    name = _('Public events')
    module = _('Events')

    model = EventViewer

    render_template = 'plugins/public_event_viewer.html'
    allow_children = False
    cache = False

    def render(self, context, instance, placeholder):
        context = super(PublicEventViewerPlugin, self).render(context, instance, placeholder)

        context['events'] = Event.objects.filter(event_type__in=instance.event_types.all()).public().future()[:instance.count]
        return context

plugin_pool.register_plugin(PublicEventViewerPlugin)