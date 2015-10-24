# encoding: utf-8

from dcpython.blog.models import Post
from django.shortcuts import render
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DateDetailView
import datetime
from django.utils.timezone import get_current_timezone


def blog(request):
    posts = Post.objects.published()[:5]
    years = Post.objects.datetimes('published', 'year', order="DESC")

    ctx = {"posts": posts, 'archive_years': years}

    return render(request, 'blog/blog.html', ctx)


class PostYearArchiveView(YearArchiveView):
    queryset = Post.objects.published()
    date_field = "published"
    make_object_list = True


class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.published()
    date_field = "published"
    make_object_list = True


class PostDetail(DateDetailView):
    queryset = Post.objects.published()
    date_field = "published"
    month_format = '%m'

    def get_object(self, queryset=None):
        tz = get_current_timezone()
        qs = queryset if queryset is not None else self.get_queryset()
        day_start = datetime.datetime(
            int(self.kwargs['year']), int(self.kwargs['month']),
            int(self.kwargs['day']))
        day_end = datetime.datetime.combine(day_start, datetime.time.max)
        return qs.get(slug=self.kwargs['slug'],
                      published__range=(day_start,
                                        day_end, ))
