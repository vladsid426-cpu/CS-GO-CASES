from django.db import models

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
    image = models.ImageField(upload_to='skins/', blank=True)
    image_url = models.URLField(blank=True)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    image_url = models.URLField(blank=True, null=True)
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='skins', blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.rarity}) - ${self.price}"

class Case(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='cases/', blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"