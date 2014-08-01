# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from blasstrap.models import Parallax, ParallaxContent, ParallaxImage


class ParallaxPlugin(CMSPluginBase):
    name = _('Parallax')
    module = _('Parallax')

    model = Parallax
    allow_children = True
    child_classes = ['ParallaxContentPlugin', 'ParallaxImagePlugin']

    render_template = 'plugins/parallax.html'


class ParallaxContentPlugin(CMSPluginBase):
    name = _('Content')
    module = _('Parallax')

    model = ParallaxContent
    require_parent = True
    parent_classes = ['ParallaxPlugin']

    render_template = 'plugins/parallax_content.html'


class ParallaxImagePlugin(CMSPluginBase):
    name = _('Image')
    module = _('Parallax')

    model = ParallaxImage
    require_parent = True
    parent_classes = ['ParallaxPlugin']

    render_template = 'plugins/parallax_image.html'

plugin_pool.register_plugin(ParallaxPlugin)
plugin_pool.register_plugin(ParallaxContentPlugin)
plugin_pool.register_plugin(ParallaxImagePlugin)


settings.CMS_PLACEHOLDER_CONF['parallax-content'] = {
    'name': _(u'Parallax content'),
    'default_plugins': [
        {
            'plugin_type': 'MarkdownPlugin',
            'values': {
                'body': u'# Parallax. <small>Sexigt.</small>\nLorem ipsum dolor sit amet.<a href="" class="btn btn-primary">Bam!</a>'
            },
        },
    ]
}
