from django.contrib import admin
from dcpython.support.models import Donor
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

class NullLevelFilter(SimpleListFilter):
    title = _("Level")

    parameter_name = "level"

    def lookups(self, request, model_admin):
        return (
            ("N", "Need Level Entry"),
            ("NN", "Level Entered"),
        )

    def queryset(self, request, queryset):
        if self.value() == "N":
            return queryset.filter(level=None)

        if self.value() == "NN":
            return queryset.filter(~Q(level=None))

class DonorAdmin(admin.ModelAdmin):
    readonly_fields = ("secret",)
    list_display = ("name", "slogan", "url", "level",)
    list_filter = (NullLevelFilter,)

admin.site.register(Donor, DonorAdmin)
