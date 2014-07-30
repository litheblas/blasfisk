# -*- coding: utf-8 -*-
from django.contrib.admin import StackedInline
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from blasstrap.models import Carousel, CarouselEntry


class CarouselEntryInline(StackedInline):
    model = CarouselEntry
    extra = 3


class CarouselPlugin(CMSPluginBase):
    name = _(u'Carousel')
    module = _(u'Bootstrap')

    model = Carousel
    allow_children = False
    render_template = "plugins/carousel.html"

    inlines = [CarouselEntryInline]

plugin_pool.register_plugin(CarouselPlugin)
