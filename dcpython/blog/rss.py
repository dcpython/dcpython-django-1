from django.contrib.syndication.views import Feed
from dcpython.blog.models import Post


class BlogFeed(Feed):
    title = "DCPython News Feed"
    link = "/blog/"
    description = "Latest DCPython User Group News"

    def items(self):
        return Post.objects.order_by('-published')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.teaser
