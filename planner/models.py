from django.db import models
from django.db import models
from django.contrib.auth.models import User


class Crop(models.Model):
    name = models.CharField(max_length=100)
    seed_rate = models.DecimalField(max_digits=5, decimal_places=2)  # kg per hectare
    fertilizer_type = models.CharField(max_length=100)
    fertilizer_rate = models.DecimalField(max_digits=5, decimal_places=2)  # kg per hectare
    water_needs = models.IntegerField()  # liters per hectare
    planting_season = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class SoilType(models.Model):
    name = models.CharField(max_length=100)
    fertilizer_factor = models.DecimalField(max_digits=3, decimal_places=2)
    water_factor = models.DecimalField(max_digits=3, decimal_places=2)
    
    def __str__(self):
        return self.name

# planner/models.py
class FarmLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


# Add location field to Calculation model
class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    soil_type = models.ForeignKey(SoilType, on_delete=models.CASCADE)
    seed_required = models.DecimalField(max_digits=10, decimal_places=2)
    fertilizer_required = models.DecimalField(max_digits=10, decimal_places=2)
    water_required = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(FarmLocation, on_delete=models.SET_NULL, null=True, blank=True)  # NEW
    region = models.CharField(max_length=100, blank=True)  # NEW
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.crop.name} - {self.created_at}" 


class AgroDealer(models.Model):
    name = models.CharField(max_length=150)

    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    # Business information
    dealer_type = models.CharField(max_length=100, blank=True)
    products = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    # Optional website/reference
    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"