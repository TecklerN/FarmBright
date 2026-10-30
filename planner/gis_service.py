import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Load FarmBright GIS datasets
soil = gpd.read_file(
    BASE_DIR / "farmbright/data/raw/soil_map/soil_types.shp"
)

zones = gpd.read_file(
    BASE_DIR / "farmbright/data/raw/agro_ecological_zones/Agro_Ecological_Zones.shp"
)

def get_location_agricultural_context(latitude, longitude):
    """
    Find the soil type and agro-ecological zone
    for a given latitude and longitude.
    """

    # Create geographic point
    point = gpd.GeoDataFrame(
        {"location": ["Farmer field"]},
        geometry=[Point(longitude, latitude)],
        crs="EPSG:4326"
    )

    # -----------------------------
    # SOIL LOOKUP
    # -----------------------------
    soil_match = gpd.sjoin(
        point,
        soil,
        how="left",
        predicate="within"
    )

    # If no soil polygon is found, try a small buffer
    if soil_match.iloc[0]["SUB_FAMILY"] is None or pd.isna(
    soil_match.iloc[0]["SUB_FAMILY"]
    ):

        point_metric = point.to_crs("EPSG:3857")
        point_buffer = point_metric.copy()
        point_buffer["geometry"] = point_metric.geometry.buffer(1000)
        point_buffer = point_buffer.to_crs("EPSG:4326")

        soil_match = gpd.sjoin(
            point_buffer,
            soil,
            how="left",
            predicate="intersects"
        )

    # -----------------------------
    # AGRO-ECOLOGICAL ZONE LOOKUP
    # -----------------------------
    zone_match = gpd.sjoin(
        point,
        zones,
        how="left",
        predicate="within"
    )

    # If no zone is found, try a small buffer
    if zone_match.iloc[0]["gez_name"] is None or pd.isna(
    zone_match.iloc[0]["gez_name"]
    ):

        point_metric = point.to_crs("EPSG:3857")
        point_buffer = point_metric.copy()
        point_buffer["geometry"] = point_metric.geometry.buffer(1000)
        point_buffer = point_buffer.to_crs("EPSG:4326")

        zone_match = gpd.sjoin(
            point_buffer,
            zones,
            how="left",
            predicate="intersects"
        )

        # -----------------------------
    # EXTRACT RESULTS
    # -----------------------------
    soil_sub_family = soil_match.iloc[0]["SUB_FAMILY"]
    soil_description = soil_match.iloc[0]["DESCRIPTIO"]

    agro_zone = zone_match.iloc[0]["gez_name"]

    # Fallback for Masvingo/Mashava locations
    if pd.isna(soil_sub_family):
        soil_sub_family = "2/4X"

    if pd.isna(soil_description):
        soil_description = "Masvingo soil context"

    if pd.isna(agro_zone):
        agro_zone = "Region IV"

    return {
        "soil_sub_family": soil_sub_family,
        "soil_description": soil_description,
        "agro_ecological_zone": agro_zone
    }