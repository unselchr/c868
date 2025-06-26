from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .validators import validateMaxMin, validateInventory
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    email = models.EmailField("email address", unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey('Role', verbose_name='Roles', null=True, related_name='users', on_delete=models.SET_NULL)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Role(models.Model):
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    ADMIN = 'ADMIN'
    READ_ONLY = 'RO'
    USER = 'USER'

    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (READ_ONLY, 'Read Only'),
        (USER, 'User')
    ]

    name = models.CharField(choices=ROLE_CHOICES, max_length=20)

    def __str__(self):
        return self.get_name_display()
    
class Part(models.Model):
    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

    IN_HOUSE = 'IH'
    OUTSOURCED = 'OS'
    SOURCE_CHOICES = [
        (IN_HOUSE, 'In House'),
        (OUTSOURCED, 'Outsourced')
    ]

    name = models.CharField(max_length=64)
    sku = models.CharField(max_length=64)
    sub_parts = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='parent_part')
    source = models.CharField(
        max_length=(15),
        choices=SOURCE_CHOICES,
        default=IN_HOUSE,
    )
    source_id = models.CharField(max_length=64)
    inventory = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    max_inventory = models.IntegerField(validators=[MinValueValidator(1, 'Must be greater than 0.')])
    min_inventory = models.IntegerField(validators=[MinValueValidator(0, 'Must be greater than or equal to 0.')])
    
    def __str__(self):
        return self.name