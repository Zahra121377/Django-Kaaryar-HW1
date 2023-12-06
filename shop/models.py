import re

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


def validate_username(value):
    if len(value) < 3 or len(value) > 20:
        raise ValidationError(
            ("Username should be between 3 and 20 characters."),
            code="invalid_username_length",
        )


def validate_phone_number(value):
    if not re.match("^[0-9]+$", value):
        raise ValidationError(
            ("Phone number should contain numeric characters."),
            code="invalid_phone_number",
        )


def validate_password(value):
    if not re.search(r"\d", value):
        raise ValidationError(
            ("Password should contain at least one numeric character."),
            code="invalid_password_numeric",
        )

    if not re.search(r"[a-zA-Z]", value):
        raise ValidationError(
            ("Password should contain at least one alphabet character."),
            code="invalid_password_alphabet",
        )

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(
            ("Password should contain at least one special character."),
            code="invalid_password_special",
        )


class Customer(models.Model):
    first_name = models.CharField(
        max_length=30,
        default="dear",
        editable=True,
        blank=True,
        validators=[MinLengthValidator(limit_value=3)],
    )
    last_name = models.CharField(
        max_length=50,
        default="user",
        editable=True,
        blank=True,
        validators=[MinLengthValidator(limit_value=3)],
    )
    username = models.CharField(
        max_length=20,
        editable=False,
        blank=False,
        validators=[validate_username],
    )
    phone = models.CharField(
        max_length=11,
        editable=True,
        blank=False,
        validators=[validate_phone_number],
    )
    email = models.EmailField()
    password = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(limit_value=8), validate_password],
    )
    address = models.CharField(
        max_length=1000, validators=[MinLengthValidator(limit_value=10)]
    )
    postal_code = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, blank=False)
    price = models.FloatField(default=0)
    category = models.ManyToManyField(Category)
    description = models.TextField(max_length=500)
    
    def __str__(self):
        return self.title