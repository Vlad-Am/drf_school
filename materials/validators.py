from rest_framework.serializers import ValidationError

key = "youtube.com"


def validate_youtube_url(value):
    if key not in value.lower():
        raise ValidationError("Incorrect YouTube URL")
