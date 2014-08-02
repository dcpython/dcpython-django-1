from django.contrib import admin
from dcpython.blog.models import Post
from django.utils.translation import ugettext_lazy as _
from pagedown.widgets import AdminPagedownWidget
from django.db import models
from markupfield.fields import MarkupField
from django.utils import six

class MarkupTextarea(AdminPagedownWidget):

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, six.text_type):
            value = value.raw
        return super(MarkupTextarea, self).render(name, value, attrs)

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        MarkupField: {'widget': MarkupTextarea},
    }
    list_display = ('title', 'published',)
    readonly_fields = ('slug',)

admin.site.register(Post, PostAdmin)
