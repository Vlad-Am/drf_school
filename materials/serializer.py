from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('name', 'description', 'preview', 'count_lessons',)

    def get_count_lessons(self, instance):
        if instance.lessons:
            return instance.lessons.count()
        else:
            return 0


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
