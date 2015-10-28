# from dcpython.app.models import User
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserChangeForm
# from django.contrib.auth.forms import UserCreationForm
#
#
# class MyUserChangeForm(UserChangeForm):
#     """
#     """
#    class Meta(UserChangeForm.Meta):
#       model = User
#
#
# class MyUserCreationForm(UserCreationForm):
#     """
#     """
#    class Meta(UserCreationForm.Meta):
#        model = User
#
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             User.objects.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise ValidationError(self.error_messages['duplicate_username'])
#
#
# class MyUserAdmin(UserAdmin):
#     form = MyUserChangeForm
#     add_form = MyUserCreationForm
#
#     fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('meetup_id', )}), )
#
#
# admin.site.register(User, MyUserAdmin)

from .models import Donor, Donation
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

qs_filter = (Q(reviewed=False) | Q(donations__reviewed=False))


class NeedsReview(SimpleListFilter):
    title = _("Level")

    parameter_name = "level"

    def lookups(self, request, model_admin):
        return (("N", "Needs Review"), ("NN", "Reviewed"), )

    def queryset(self, request, queryset):
        if self.value() == "N":
            return queryset.filter(qs_filter)

        if self.value() == "NN":
            return queryset.filter(reviewed=True, donations__reviewed=True)


class DonationInline(admin.TabularInline):
    model = Donation
    fields = ("datetime", "type", "donation", "completed", "valid_until",
              "level", "reviewed")
    readonly_fields = ("datetime", "type", "donation", )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class DonorAdmin(admin.ModelAdmin):
    readonly_fields = ("secret", )
    list_display = ("name", "email", "public_name", "level", )
    list_filter = (NeedsReview, )
    inlines = [DonationInline, ]


admin.site.register(Donor, DonorAdmin)
