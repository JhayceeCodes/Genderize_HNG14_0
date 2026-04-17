from django.db import models
import uuid


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHERS = "others", "Others"
    
    class AgeGroup(models.TextChoices):
        CHILD = "child", "Child"
        TEEN = "teenager", "Teenager"
        ADULT = "adult", "Adult"
        SENIOR = "senior", "Senior"

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    gender_probability = models.DecimalField(max_digits=3, decimal_places=2)
    sample_size = models.PositiveIntegerField()
    age = models.PositiveSmallIntegerField()
    age_group = models.CharField(max_length=10, choices=AgeGroup.choices)
    country_id = models.CharField(max_length=5)
    country_probability = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)