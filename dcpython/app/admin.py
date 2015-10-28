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
