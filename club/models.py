from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class ClubUser(AbstractUser):
    MEMBERSHIP_TYPES = (
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    )

    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPES, default='standard')
    address = models.TextField()

    # Avoid conflicts by specifying related_name
    groups = models.ManyToManyField(
        Group,
        related_name='clubuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='clubuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    REQUIRED_FIELDS = ['email', 'name', 'last_name', 'phone', 'membership_type', 'address']


class Court(models.Model):
    SURFACE_CHOICES = (
        ('hard', 'Hard'),
        ('clay', 'Clay'),
        ('grass', 'Grass'),
    )

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    surface = models.CharField(max_length=50, choices=SURFACE_CHOICES)
    lights = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    court = models.ForeignKey('Court', on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__gte='07:00:00') & models.Q(end_time__lte='22:00:00'),
                name='valid_reservation_time',
            ),
            models.UniqueConstraint(
                fields=['court', 'date', 'start_time', 'end_time'],
                name='unique_court_reservation',
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.court} ({self.date} {self.start_time} - {self.end_time})"
