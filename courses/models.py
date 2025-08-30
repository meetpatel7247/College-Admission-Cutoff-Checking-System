from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class College(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='college_photos/', blank=True, null=True)
    website = models.URLField()

    def __str__(self):
        return self.name

class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stream = models.CharField(max_length=50, choices=[('Science', 'Science'), ('Commerce', 'Commerce')])
    min_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.college.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(100.00, message="Percentage cannot exceed 100."),
            MinValueValidator(0.00, message="Percentage cannot be negative.")
        ]
    )

    def __str__(self):
        return self.user.username