import geopandas as gpd
from shapely.geometry import Point


# Load FarmBright GIS datasets
soil = gpd.read_file(
    "farmbright/data/raw/soil_map/soil_types.shp"
)

zones = gpd.read_file(
    "farmbright/data/raw/agro_ecological_zones/Agro_Ecological_Zones.shp"
)


def get_location_agricultural_context(latitude, longitude):
    """
    Find the soil and agro-ecological zone
    for a given latitude and longitude.
    """

    # Create a geographic point
    point = gpd.GeoDataFrame(
        {"location": ["Farmer field"]},
        geometry=[Point(longitude, latitude)],
        crs="EPSG:4326"
    )

    # Find matching soil polygon
    soil_match = gpd.sjoin(
        point,
        soil,
        how="left",
        predicate="within"
    )

    # Find matching agro-ecological zone
    zone_match = gpd.sjoin(
        point,
        zones,
        how="left",
        predicate="within"
    )

    # Extract soil information
    soil_sub_family = soil_match.iloc[0]["SUB_FAMILY"]
    soil_description = soil_match.iloc[0]["DESCRIPTIO"]

    # Extract agro-ecological zone
    agro_zone = zone_match.iloc[0]["gez_name"]

    # Return everything as a dictionary
    return {
        "soil_sub_family": soil_sub_family,
        "soil_description": soil_description,
        "agro_ecological_zone": agro_zone
    }


# Test the function
result = get_location_agricultural_context(
    latitude=-17.8252,
    longitude=31.0335
)

print("\n===== FARMBRIGHT AGRICULTURAL CONTEXT =====")
print("Soil Sub-Family:", result["soil_sub_family"])
print("Soil Description:", result["soil_description"])
print("Agro-Ecological Zone:", result["agro_ecological_zone"])