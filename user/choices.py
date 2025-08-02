from django.db.models import TextChoices

class MyUserRoleEnum(TextChoices):
    STANDARD_USER  = 'standard_user'
    MANAGER = 'manager'
    ACCOUNTANT = 'accountant'
