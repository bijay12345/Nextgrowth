from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin

class UserModelAdmin(UserAdmin):

    search_fields = ("email", "user_name", "first_name")
    list_display=("id","email","user_name","is_active")
    list_filter = ("email", "user_name", "first_name", "is_active", "is_staff")

    fieldsets=(
        ("User Credential",{"fields":("email","password")}),
        ("Personal Info",{"fields":("user_name",)}),
        ("permissions",{"fields":("is_staff",)}),
    )

    add_fieldsets = (
        (None,{
            "classes":("wide",),
            "fields":("email","user_name","password1","password2"),
            }),
    )
    search_fields = ("user_name","id")
    ordering = ("user_name","id")
    filter_horizontal=()

admin.site.register(NewUser, UserModelAdmin)