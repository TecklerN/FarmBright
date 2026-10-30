import geopandas as gpd

# =============================
# SOIL MAP
# =============================

soil_path = "farmbright/data/raw/soil_map/soil_types.shp"

soil = gpd.read_file(soil_path)

print("\n==============================")
print("        SOIL MAP")
print("==============================")

print("Rows:", len(soil))

print("\nColumns:")
print(soil.columns.tolist())

print("\nCRS:")
print(soil.crs)

print("\nFirst 5 attribute records:")
print(soil.drop(columns="geometry").head().to_string(index=False))

print("\nMissing values:")
print(soil.drop(columns="geometry").isnull().sum())


# =============================
# AGRO-ECOLOGICAL ZONES
# =============================

zone_path = "farmbright/data/raw/agro_ecological_zones/Agro_Ecological_Zones.shp"

zones = gpd.read_file(zone_path)

print("\n==============================")
print("    AGRO-ECOLOGICAL ZONES")
print("==============================")

print("Rows:", len(zones))

print("\nColumns:")
print(zones.columns.tolist())

print("\nCRS:")
print(zones.crs)

print("\nFirst 10 attribute records:")
print(zones.drop(columns="geometry").head(10).to_string(index=False))

print("\nMissing values:")
print(zones.drop(columns="geometry").isnull().sum())