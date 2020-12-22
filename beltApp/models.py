from django.db import models
from django.contrib import messages
import bcrypt
import re

# Creating validations!


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # to ensure EMAIL is a valid email type. Dont forget to include "import re" at top of models.
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        # Errors set to empty until it catches errors from POST DATA. It will display all the errors that fail the if statements

        if len(postData["first_name"]) < 2:
            errors['first_name'] = "First name should be at least 2 characters"

        if len(postData["last_name"]) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"

        if len(postData['email']) < 5:
            errors['email'] = "the Email entered is invalid."

        if len(User.objects.filter(email=postData['email'])) != 0:
            errors['email_validate'] = "This email is already registered."

        if len(postData["password"]) < 5:
            errors['password'] = "password should at least be 5 characters long"
        if postData["password"] != postData['pw_confirm']:
            errors['password'] = "wrong password!"

        return errors

# Log in validator will engage when user fails login info. If Email is correct it will enter the "ELSE" statement erroring the password as incorrect/
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])

        if len(User.objects.filter(email=postData['email'])) == 0:
            errors['email'] = "Email or Password is incorrect."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password_hash.encode()):
                errors['password'] = "Password doesn't match"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(max_length=250)
    password_hash = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return f"Show: {self.first_name} {self.last_name}"


# --------------------------- import tv shows shit ---------------------------------------

class ShowManager(models.Manager):
    # NO FIELDS should be blank
    # title at least 2 chars
    # desc at least 10 char
    # network at least 3 char
    def validateShow(self, postData):
        errors = {}

        if len(postData["location"]) < 2:
            errors["location"] = "Location must be at least 2 characters."

        if len(postData["start_date"]) == 0:
            errors["start_date"] = "Start Date is required."

        if len(postData["end_date"]) == 0:
            errors["end_date"] = "End Date is required."

        if len(postData["description"]) == 0:
            errors["description"] = "Description is required."

        if len(postData["description"]) < 10:
            errors["description"] = "Description must be longer than 10 Characters."

        return errors


class Show(models.Model):
    created_by = models.ForeignKey(
        User, related_name="shows_created", on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShowManager()

    def __str__(self):
        return f'show: {self.title} {self.network}'
