from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class Skin(models.Model):
    RARITY_CHOICES = [
        ('Common', 'Common'),
        ('Uncommon', 'Uncommon'),
        ('Rare', 'Rare'),
        ('Mythical', 'Mythical'),
        ('Legendary', 'Legendary'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='skins', blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.rarity}) - ${self.price}"

class Case(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.name} - ${self.price if hasattr(self, 'price') else 'N/A'}"

class Human(AbstractUser):  
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='human_set',          # ← important
        related_query_name='human',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='human_set',          # ← important
        related_query_name='human',

    )


    def __str__(self):
        return self.username

