from django.db import models
from django.contrib.auth.models import User

# Add role field to User via profile
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class GatePass(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'), 
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Electronics', 'Electronics'),
        ('Information Technology', 'Information Technology'),
    ]
    
    # Basic Info (matching your frontend exactly)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=200)
    roll_number = models.CharField(max_length=50)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    material_description = models.TextField()
    date_time = models.DateTimeField()
    
    # Status & Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_passes')
    
    def __str__(self):
        return f"GP-{self.id} - {self.student_name} ({self.roll_number})"
    
    class Meta:
        ordering = ['-created_at']

# Signal to create UserProfile when User is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)