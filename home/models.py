from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class ArticlePage(Page):
    """A page for blog articles that can have comments"""
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Add comments to the context
        context['comments'] = self.comments.all()
        return context

