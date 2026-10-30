# planner/management/commands/load_sample_data.py
from django.core.management.base import BaseCommand
from planner.models import Crop, SoilType

class Command(BaseCommand):
    help = 'Load sample data for the agricultural calculator'
    
    def handle(self, *args, **kwargs):
        # Create soil types
        soils = [
            {'name': 'Sandy Soil', 'fertilizer_factor': 1.2, 'water_factor': 1.3},
            {'name': 'Loamy Soil', 'fertilizer_factor': 1.0, 'water_factor': 1.0},
            {'name': 'Clay Soil', 'fertilizer_factor': 0.9, 'water_factor': 0.8},
            {'name': 'Silty Soil', 'fertilizer_factor': 1.0, 'water_factor': 1.1},
        ]
        
        for soil_data in soils:
            SoilType.objects.get_or_create(
                name=soil_data['name'],
                defaults={
                    'fertilizer_factor': soil_data['fertilizer_factor'],
                    'water_factor': soil_data['water_factor']
                }
            )
        
        # Create crops
        crops = [
            {
                'name': 'Maize',
                'seed_rate': 25,
                'fertilizer_type': 'NPK 10-26-26',
                'fertilizer_rate': 200,
                'water_needs': 5000,
                'planting_season': 'Early rainy season'
            },
            {
                'name': 'Wheat',
                'seed_rate': 110,
                'fertilizer_type': 'Urea + DAP',
                'fertilizer_rate': 180,
                'water_needs': 4500,
                'planting_season': 'Cool dry season'
            },
            {
                'name': 'Rice',
                'seed_rate': 90,
                'fertilizer_type': 'Ammonium Sulfate',
                'fertilizer_rate': 150,
                'water_needs': 9000,
                'planting_season': 'Warm wet season'
            },
            {
                'name': 'Rapoko (Finger Millet)',
                'seed_rate': 8,
                'fertilizer_type': 'Compost + NPK',
                'fertilizer_rate': 100,
                'water_needs': 3000,
                'planting_season': 'Early to mid rainy season'
            },
            {
                'name': 'Soybean',
                'seed_rate': 70,
                'fertilizer_type': 'Rhizobium Inoculant',
                'fertilizer_rate': 120,
                'water_needs': 4000,
                'planting_season': 'Warm season'
            },
            {
                'name': 'Vegetables',
                'seed_rate': 5,
                'fertilizer_type': 'Compost Manure',
                'fertilizer_rate': 250,
                'water_needs': 6000,
                'planting_season': 'Varies by vegetable type'
            },
        ]
        
        for crop_data in crops:
            Crop.objects.get_or_create(
                name=crop_data['name'],
                defaults={
                    'seed_rate': crop_data['seed_rate'],
                    'fertilizer_type': crop_data['fertilizer_type'],
                    'fertilizer_rate': crop_data['fertilizer_rate'],
                    'water_needs': crop_data['water_needs'],
                    'planting_season': crop_data['planting_season']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data!'))