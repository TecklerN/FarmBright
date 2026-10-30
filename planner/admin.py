from django.contrib import admin
from django.contrib import admin
from .models import Crop, SoilType, FarmLocation, Calculation

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'seed_rate', 'fertilizer_type', 'fertilizer_rate', 'water_needs', 'planting_season')

@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'fertilizer_factor', 'water_factor')

@admin.register(FarmLocation)
class FarmLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'latitude', 'longitude', 'address', 'created_at')

@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop', 'area', 'soil_type', 'seed_required', 'fertilizer_required', 'water_required', 'location', 'region', 'created_at')

# Register your models here.
