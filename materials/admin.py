from django.contrib import admin

from materials.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "description",)
    list_filter = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "description", "course", "url",)
    list_filter = ("name", "description", "course", "owner",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("course_subscription", "user", 'is_sub',)
    list_filter = ("course_subscription", "user",)




