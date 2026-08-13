
from GeoSpatialPricingEngine import *
import os

filePath = '../notebooks/Jupyter/TestSpec.json'
print("Using spec file: " + os.path.abspath(filePath))

pebObj=PricingEngineBuilder.build_from_json(file_path=os.path.abspath(filePath))

print("\n\nbuilder object:")
print(pebObj)

print("\n\nbuilder's Geo-taxonomy object data:")
print(pebObj.geo_taxonomy.data)

print("\n\nbuilder's orders object data:")
print(pebObj.orders.data)

print("\n\nbuilder's tiled-region object:")
print(pebObj.tiled_region)

print(f"\n\nbuilder's calibration records ({len(pebObj.calibration_records)} total):")
print(list(pebObj.calibration_records.items())[:4])
