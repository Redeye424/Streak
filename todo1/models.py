from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    text_box = models.CharField(max_length=200, default="")
    text_box_on = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Streak(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="streaks")
    name = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class StreakCompletion(models.Model):
    streak = models.ForeignKey(Streak, on_delete=models.CASCADE, related_name="completions")
    completed_date = models.DateField()
    
    def __str__(self):
        return f"{self.streak.name} - {self.completed_date}"