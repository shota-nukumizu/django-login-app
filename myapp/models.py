from django.db import models
from django.contrib.auth.models import AbstractUser

LEADER = 1
SUPER_ADVISOR = 2
NORMAL = 3
ROLE_CHOICES = (
    (LEADER, 'leader'),
    (SUPER_ADVISOR, 'super-advisor'),
    (NORMAL, 'normal')
)

class SampleUser(AbstractUser):
    role = models.IntegerField(choices=ROLE_CHOICES, default=3)