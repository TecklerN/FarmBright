from django.shortcuts import render, redirect
from .nlp_service import process_farmer_query
from .models import Crop, SoilType, Calculation, FarmLocation, AgroDealer
from django.http import JsonResponse
from .gis_service import get_location_agricultural_context
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests

# Home page
def home(request):
    return render(request, 'planner/home.html')

# Plan page

def plan(request):
    crops = Crop.objects.all()
    soil_types = SoilType.objects.all()
    context = {
        'crops': crops,
        'soil_types': soil_types,
        "weather_api_key": settings.OPENWEATHER_API_KEY,
    }
    return render(request, 'planner/plan.html', context)


# Calculation API
@csrf_exempt
def calculate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            crop_id = data.get('crop_id')
            area = float(data.get('area'))
            soil_id = data.get('soil_id')

            crop = Crop.objects.get(id=crop_id)
            soil = SoilType.objects.get(id=soil_id)

            seed_required = crop.seed_rate * area
            fertilizer_required = crop.fertilizer_rate * area * soil.fertilizer_factor
            water_required = crop.water_needs * area * soil.water_factor

            calculation = Calculation(
                user=request.user if request.user.is_authenticated else None,
                crop=crop,
                area=area,
                soil_type=soil,
                seed_required=seed_required,
                fertilizer_required=fertilizer_required,
                water_required=water_required
            )
            calculation.save()

            return JsonResponse({
                'success': True,
                'seed_required': round(seed_required, 2),
                'fertilizer_type': crop.fertilizer_type,
                'fertilizer_required': round(fertilizer_required, 2),
                'water_required': round(water_required, 2),
                'planting_season': crop.planting_season,
                'calculation_id': calculation.id,
                'user_authenticated': request.user.is_authenticated
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Register user
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('planner:register')

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return redirect('planner:register')

        from django.contrib.auth.models import User
        try:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('planner:dashboard')
        except:
            messages.error(request, 'Username already exists.')
            return redirect('planner:register')

    return render(request, 'planner/register.html')

# Login user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('planner:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'planner/login.html')

# Logout user
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('planner:home')

# Dashboard
@login_required
def dashboard_view(request):
    calculations = Calculation.objects.filter(user=request.user).order_by('-created_at')
    user_farms = FarmLocation.objects.filter(user=request.user)

    total_area = calculations.aggregate(Sum('area'))['area__sum']

    most_common_crop = None
    if calculations.exists():
        most_common_crop_data = calculations.values('crop__name').annotate(
            count=Count('id')
        ).order_by('-count').first()
        most_common_crop = most_common_crop_data['crop__name'] if most_common_crop_data else None

    recent_calculations = calculations[:5]

    # Weather data for first farm
    weather_data = None
    if user_farms.exists():
        first_farm = user_farms.first()
        weather_data = get_weather_data(first_farm.latitude, first_farm.longitude)

    return render(request, 'planner/dashboard.html', {
        'calculations': calculations,
        'user_farms': user_farms,
        'total_area': total_area,
        'most_common_crop': most_common_crop,
        'recent_calculations': recent_calculations,
        'weather_data': weather_data
    })

# Save farm location
@csrf_exempt
@login_required
def save_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            location = FarmLocation.objects.create(
                user=request.user,
                name=data.get('name', 'My Farm'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                address=data.get('address', '')
            )
            return JsonResponse({'success': True, 'location_id': location.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False})

# Get all farm locations
@login_required
def get_locations(request):
    locations = FarmLocation.objects.filter(user=request.user)
    data = [{
        'id': loc.id,
        'name': loc.name,
        'lat': float(loc.latitude),
        'lng': float(loc.longitude),
        'address': loc.address
    } for loc in locations]

    return JsonResponse({'locations': data})

# Get weather data using OpenWeatherMap API
def get_weather_data(lat, lng):
    API_KEY = settings.OPENWEATHER_API_KEY # Replace with your real API key
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Predict disease API
@csrf_exempt
@login_required
def predict_disease(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Simple mock AI - replace with real ML model later
        return JsonResponse({
            'disease': 'Early Blight',
            'confidence': 0.87,
            'treatment': 'Apply copper-based fungicide every 7-10 days'
        })
    return JsonResponse({'error': 'Invalid request or missing image'})



def agricultural_context_api(request):
    """
    Return soil and agro-ecological information
    for a given latitude and longitude.
    """

    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET requests are allowed."},
            status=405
        )

    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")

    if not latitude or not longitude:
        return JsonResponse(
            {
                "error": "Latitude and longitude are required."
            },
            status=400
        )

    try:
        latitude = float(latitude)
        longitude = float(longitude)

        result = get_location_agricultural_context(
            latitude=latitude,
            longitude=longitude
        )

        return JsonResponse(result)

    except ValueError:
        return JsonResponse(
            {
                "error": "Latitude and longitude must be valid numbers."
            },
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )

def nlp_query_api(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET requests are allowed."},
            status=405
        )

    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse(
            {"error": "Please provide a farming question."},
            status=400
        )

    try:
        result = process_farmer_query(query)

        # Convert NumPy string to normal Python string
        result["intent"] = str(result["intent"])

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )

    # Agro-dealer API
def agro_dealers_api(request):
    """
    Return agro-dealers within a specified radius
    of the farmer's selected location.
    """

    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET requests are allowed."},
            status=405
        )

    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")
    radius = request.GET.get("radius", 50)

    if not latitude or not longitude:
        return JsonResponse(
            {
                "error": "Latitude and longitude are required."
            },
            status=400
        )

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)

        # Earth's radius in kilometres
        EARTH_RADIUS_KM = 6371.0

        # Get all agro-dealers
        dealers = AgroDealer.objects.all()

        nearby_dealers = []

        for dealer in dealers:

            dealer_lat = float(dealer.latitude)
            dealer_lng = float(dealer.longitude)

            # Convert degrees to radians
            from math import radians, sin, cos, sqrt, atan2

            lat1 = radians(latitude)
            lat2 = radians(dealer_lat)

            delta_lat = radians(dealer_lat - latitude)
            delta_lng = radians(dealer_lng - longitude)

            # Haversine formula
            a = (
                sin(delta_lat / 2) ** 2
                +
                cos(lat1)
                * cos(lat2)
                * sin(delta_lng / 2) ** 2
            )

            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = EARTH_RADIUS_KM * c

            # Only include dealers within radius
            if distance <= radius:

                nearby_dealers.append({
                    "id": dealer.id,
                    "name": dealer.name,
                    "latitude": dealer_lat,
                    "longitude": dealer_lng,
                    "city": dealer.city,
                    "province": dealer.province,
                    "address": dealer.address,
                    "dealer_type": dealer.dealer_type,
                    "products": dealer.products,
                    "phone": dealer.phone,
                    "website": dealer.website,
                    "distance_km": round(distance, 2)
                })

        # Nearest shops first
        nearby_dealers.sort(
            key=lambda dealer: dealer["distance_km"]
        )

        return JsonResponse({
            "success": True,
            "count": len(nearby_dealers),
            "radius_km": radius,
            "dealers": nearby_dealers
        })

    except ValueError:
        return JsonResponse(
            {
                "error": "Latitude, longitude and radius must be valid numbers."
            },
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            status=500
        )