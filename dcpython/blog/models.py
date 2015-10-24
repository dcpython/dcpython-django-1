from django.db import models
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from markupfield.fields import MarkupField
from django.utils import timezone


class PostManager(models.Manager):
    use_for_related = True

    def published(self):
        return self.filter(published__lt=now())


class Post(models.Model):
    """
    Simple blog post
    """

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200)
    teaser = MarkupField(markup_type='markdown')
    body = MarkupField(markup_type='markdown')
    draft = models.BooleanField(default=False)
    published = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey('app.User')

    objects = PostManager()

    @property
    def local_published(self):
        current_tz = timezone.get_current_timezone()
        return self.published.astimezone(current_tz)

    def get_absolute_url(self):
        return reverse('post-detail',
                       kwargs={'slug': self.slug,
                               'year': self.local_published.year,
                               'month': self.local_published.month,
                               'day': self.local_published.day})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # ensure if in draft, there is no published date
        if self.draft:
            self.published = None
        # ensure that if not in draft, there is a published date
        if not self.published and not self.draft:
            self.published = now()
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-published', )
        get_latest_by = 'published'
        unique_together = (('published', 'slug'))
