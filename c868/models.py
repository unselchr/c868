from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError
from .validators import validateMaxMin, validateInventory

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
    sub_parts = models.ManyToManyField('self', blank=True)
    source = models.CharField(
        max_length=(15),
        choices=SOURCE_CHOICES,
        default=IN_HOUSE,
    )
    source_id = models.CharField(max_length=64)
    inventory = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    max_inventory = models.IntegerField(validators=[MinValueValidator(1, 'Must be greater than 0.')])
    min_invetory = models.IntegerField(validators=[MinValueValidator(0, 'Must be greater than or equal to 0.')])

    def validateMaxMin(self):
        if self.max_inventory <= self.min_invetory:
            raise ValidationError('Max value is less than or equal to min value.')
    
    def validateInventory(self):
        if self.inventory > self.max_inventory:
            raise ValidationError('Inventory must be less than max.')
        if self.inventory < self.min_invetory:
            raise ValidationError('Inventory must be greater than min.')
    
    def save(self, *args, **kwargs):
        self.validateInventory()
        self.validateMaxMin()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name