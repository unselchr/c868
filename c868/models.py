from django.db import models
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
    
