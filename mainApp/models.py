from django.db import models

# Create your models here.


class GitHubRepository(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    stars = models.IntegerField()
    forks = models.IntegerField()
    issues = models.IntegerField()
    pull_requests = models.IntegerField()
    
    def __str__(self):
        return self.name