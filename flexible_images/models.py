from django.db import models


# Test models - you won't need these IRL.
class FlexibleImageTestImage(models.Model):
    title = models.CharField(
        max_length=30,
    )

    image = models.ImageField(
        null=True,
        blank=True,
    )

    plain_file = models.FileField(
        null=True,
        blank=True,
    )
