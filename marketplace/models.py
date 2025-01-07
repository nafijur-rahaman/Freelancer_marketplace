from django.db import models
from django.contrib.auth.models import User

# Define user roles for clarity
class UserRole(models.TextChoices):
    FREELANCER = 'Freelancer', 'Freelancer'
    CLIENT = 'Client', 'Client'
    ADMIN = 'Admin', 'Admin'


class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CLIENT,  # Default user role is Client
    )
    

    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"



class JobPost(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='open')  
    
    def __str__(self):
        return self.title