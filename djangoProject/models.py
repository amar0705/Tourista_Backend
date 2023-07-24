# In your_app/models.py
from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class Host(models.Model):
    name = models.CharField(max_length=200)
    host_status = models.BooleanField(default=True)
    about = models.TextField()
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=200)
    phone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

    def is_authenticated(self):
        return True


class Guest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    phone = models.IntegerField()
    bio = models.TextField()
    profile_image = models.URLField()
    dob = models.DateField(null=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

    def is_authenticated(self):
        return True


class State(models.Model):
    state = models.TextField()

    def __str__(self):
        return self.state


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.TextField()

    def __str__(self):
        return self.city

class Location(models.Model):
    state = models.TextField()
    city = models.TextField()

    def __str__(self):
        return self.city


class PropertyType(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Property(models.Model):
    property = models.TextField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    total_bedrooms = models.IntegerField()
    summary = models.TextField()
    address = models.TextField()
    price = models.IntegerField()
    hosted_since = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property


class RevokedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    revoked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
