from django.db import models
from django.contrib.auth.models import User, AbstractUser,  Group, Permission


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('investor', 'Investor'),
        ('contributor', 'Contributor')
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True, help_text='Specific permissions for this user.')



class Publication(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='publications/', blank=True, null=True)
    audio = models.FileField(upload_to='publications/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    ACTION_CHOICES = (
        ('like', 'Like'),
        ('intersted', 'Intersted'),
        ('invest', 'Invest'),
        ('contribute', 'Contribute'),

    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    needed_funds = models.DecimalField(max_digits=10, decimal_places=2)
    current_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    
    def __str__(self):
        return self.title


class Contribution(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.contributor.username} contributed {self.amount} to {self.project.title}"


class Investment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.investor.username} invested {self.amount} in {self.project.title}"
