from django.conf import settings
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    preview = models.ImageField(upload_to="media/", verbose_name="превью", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    url = models.URLField(verbose_name="ссылка", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["name"]


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    preview = models.ImageField(upload_to="media/", verbose_name="превью", **NULLABLE)
    video = models.FileField(upload_to="media/", verbose_name="видео", **NULLABLE)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, related_name="lessons", verbose_name="курс", **NULLABLE
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    url = models.URLField(verbose_name="ссылка", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["name"]


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                             on_delete=models.CASCADE, **NULLABLE)
    course_subscription = models.ForeignKey(Course, verbose_name='курс в подписке', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.course_subscription}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
