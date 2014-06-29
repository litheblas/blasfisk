# -*- coding: utf-8 -*-
from django.db import models
from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PlaceholderField

from globals import generate_filename


def generate_carousel_image_filename(instance, filename):
    return generate_filename(instance, filename, 'carousel-imgs')


class Carousel(CMSPlugin):
    extra_css_classes = models.CharField(max_length=256, blank=True)
    indicators = models.BooleanField(default=True)
    controls = models.BooleanField(default=True)
    arrows = models.BooleanField(default=True)
    interval = models.IntegerField(default=5000)
    pause = models.CharField(max_length=64, default='hover', blank=True)
    wrap = models.BooleanField(default=True)

    def copy_relations(self, oldinstance):
        for associated_item in oldinstance.entries.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            associated_item.pk = None
            associated_item.carousel = self
            associated_item.save()


class CarouselEntry(models.Model):
    carousel = models.ForeignKey(Carousel, related_name='entries')
    image = models.ImageField(upload_to=generate_carousel_image_filename)
    caption_heading = models.CharField(max_length=256, blank=True)
    caption = models.TextField(blank=True)
    priority = models.IntegerField()

    class Meta:
        ordering = ['priority']


class Jumbotron(CMSPlugin):
    extra_css_classes = models.CharField(max_length=256, blank=True)
    container = models.BooleanField(default=True)
    content = PlaceholderField('jumbotron-content')