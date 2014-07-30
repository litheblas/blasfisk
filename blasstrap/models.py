# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PlaceholderField
from decimal import Decimal

from globals import generate_filename


def generate_carousel_image_filename(instance, filename):
    return generate_filename(instance, filename, 'carousel-imgs')


def generate_pusher_image_filename(instance, filename):
    return generate_filename(instance, filename, 'pusher-imgs')


def generate_parallax_image_filename(instance, filename):
    return generate_filename(instance, filename, 'parallax-imgs')


def generate_parallax_inner_image_filename(instance, filename):
    return generate_filename(instance, filename, 'parallax-mobile-imgs')


class Carousel(CMSPlugin):
    extra_css_classes = models.CharField(max_length=256, blank=True)
    indicators = models.BooleanField(default=True)
    controls = models.BooleanField(default=True)
    arrows = models.BooleanField(default=True)
    interval = models.IntegerField(default=5000)
    pause = models.CharField(max_length=64, default='hover', blank=True)
    wrap = models.BooleanField(default=True)

    def copy_relations(self, copied_instance):
        # Delete all entries to not duplicate them for every save
        self.entries.all().delete()
        for associated_item in copied_instance.entries.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            associated_item.pk = None
            associated_item.carousel = self
            associated_item.save()


class CarouselEntry(models.Model):
    carousel = models.ForeignKey(Carousel, related_name='entries')
    image = models.ImageField(upload_to=generate_carousel_image_filename)
    heading = models.CharField(max_length=256, blank=True)
    caption = models.TextField(blank=True)
    priority = models.IntegerField()

    class Meta:
        ordering = ['priority']


class Jumbotron(CMSPlugin):
    extra_css_classes = models.CharField(max_length=256, blank=True)
    container = models.BooleanField(default=True)
    content = PlaceholderField('jumbotron-content')


class Pusher(CMSPlugin):
    wrapper_css_classes = models.CharField(max_length=256, blank=True, default='row pusher')
    entry_css_classes = models.CharField(max_length=256, blank=True, default='col-sm-4 item')
    container = models.BooleanField(default=False)

    def copy_relations(self, copied_instance):
        # Delete all entries to not duplicate them for every save
        self.entries.all().delete()
        for associated_item in copied_instance.entries.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            associated_item.pk = None
            associated_item.pusher = self
            associated_item.save()


class PusherEntry(models.Model):
    pusher = models.ForeignKey(Pusher, related_name='entries')
    image = models.ImageField(upload_to=generate_pusher_image_filename)
    heading = models.CharField(max_length=256, blank=True)
    caption = models.TextField(blank=True, default='<p></p>',
                               help_text='Använd med förstånd, HTML-taggar tillåts. Se till att koden är korrekt och att du använder <p>.')
    priority = models.IntegerField()

    class Meta:
        ordering = ['priority']


class Parallax(CMSPlugin):
    speed = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.2'))
    cover_ratio = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.75'))
    holder_min_height = models.IntegerField(default=200)

    # media_width = models.IntegerField(default=1600)
    # media_height = models.IntegerField(default=900)
    # media_width_unparallaxed = models.IntegerField(default=800)
    # media_height_unparallaxed = models.IntegerField(default=450)


class ParallaxImage(CMSPlugin):
    image = models.ImageField(upload_to=generate_parallax_image_filename)
    # mobile_image = models.ImageField(upload_to=generate_parallax_mobile_image_filename)
    extra_height = models.IntegerField(default=0)


class ParallaxContent(CMSPlugin):
    image = models.ImageField(blank=True, null=True, upload_to=generate_parallax_inner_image_filename)
    image_placement = models.BooleanField(default=False, help_text=_('True is to the right.'))
    content = PlaceholderField('parallax-content')