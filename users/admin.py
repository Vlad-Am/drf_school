from django.contrib import admin

from users.models import Pays, User


@admin.register(Pays)
class PayAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'course', 'payment_method')
    list_filter = ('date',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active',)
    list_filter = ('email',)
