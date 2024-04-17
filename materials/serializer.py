from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    subject_list = LessonSerializer(source='lesson_set', many=True, read_only=True)
    class Meta:
        model = Course
        fields = ('name', 'description', 'preview', 'count_lessons', 'subject_list', 'user')

    @staticmethod
    def get_count_lessons(instance):
        if instance.lessons:
            return instance.lessons.count()
        else:
            return 0


