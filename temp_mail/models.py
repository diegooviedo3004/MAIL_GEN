from django.db import models
import re
# Create your models here.

class TempMail(models.Model):
    user = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_login(self):
        pattern = r'^([\w.-]+)@([\w.-]+)$'
        match = re.match(pattern, self.email)
        login = match.group(1)
        return login
    
    def get_domain(self):
        pattern = r'^([\w.-]+)@([\w.-]+)$'
        match = re.match(pattern, self.email)
        domain = match.group(2)
        return domain

    def __str__(self):
        return self.email
