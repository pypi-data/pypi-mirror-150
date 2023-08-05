from django.db import models

# Create your models here.

SMALL = 'small'
MEDIUM = 'medium'
LARGE = 'large'
XLARGE = 'xlarge'
DIMENSION_PACKAGE= (
    (SMALL, SMALL),
    (MEDIUM, MEDIUM),
    (LARGE, LARGE),
    (XLARGE, XLARGE)
)

class Delivery(models.Model):
    origin = models.CharField(max_length=500, blank=False, null=False)
    destination = models.CharField(max_length=500, blank=False, null=False)
    dimension = models.CharField(max_length=100, choices=DIMENSION_PACKAGE, blank=False, null=False, default=SMALL)
    date_created = models.DateTimeField(auto_now_add=True)