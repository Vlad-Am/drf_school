from django.contrib import admin

from users.models import Pays


@admin.register(Pays)
class PayAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'course', 'payment_method')
    list_filter = ('date',)
