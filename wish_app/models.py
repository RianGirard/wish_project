from django.db import models
import re

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
            errors['email'] = "Invalid email format!"

        found_users = User.objects.filter(email=postData['email'])
        if found_users:
            errors['email'] = "Email already in database. Choose another"
        
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        return errors

class User(models.Model):
    fname = models.CharField(max_length=45)
    lname = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()     # replaces the default value of objects = models.Manager() to custom version above  for validations
    # wishes_made = a list of wishes "made" by the User
    # liked_wishes = a list of wishes "liked" by the User

    def __repr__ (self):
        return f"<User Name: {self.fname} {self.lname} ID#: {self.id}>"


class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    granted = models.BooleanField(default=False)
    granted_at = models.DateTimeField(default=None, null=True)
    user = models.ForeignKey(User, related_name="wishes_made", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_wishes")

    def __repr__ (self):
        return f"<Wish: {self.item} User: {self.user.fname}>"


# Create your models here.
