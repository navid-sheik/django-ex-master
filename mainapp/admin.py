from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser
from .models import FriendRequest, Hobby, Profile, User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'friends',
                ),
            },
        ),
    )


# UserAdmin.fieldsets += (('Hobbbies', {'fields': ('customer_account','default_customer_account')}))
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Hobby)
admin.site.register(FriendRequest)