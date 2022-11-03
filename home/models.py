from django.db import models

from wagtail.core.models import Page
# from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
# from ckeditor.fields import RichTextField

from wagtailmetadata.models import MetadataPageMixin


class HomePage(MetadataPageMixin, Page):
    # body = RichTextField(blank=True, null=True)
    max_count = 1
    content_panels = Page.content_panels
    subpage_types = [
        'home.AboutPage',  # appname.ModelName
        'blog.BlogIndexPage',
        'blog.BlogTagIndexPage',
        'blog.BlogCategoryIndexPage',
        'contact.ContactPage',
    ]
    # content_panels = Page.content_panels + [
    #     FieldPanel('body', classname="full"),
    # ]

class AboutPage(MetadataPageMixin, Page):
    max_count = 1
    content_panels = Page.content_panels
    subpage_types = []
# class ContactPage(Page):
#     max_count = 1
#     content_panels = Page.content_panels