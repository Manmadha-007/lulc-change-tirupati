# pipeline/lulc_class_mapping.py

# ESA WorldCover → Project LULC Classes
WORLD_COVER_MAPPING = {
    # Forest
    10: 1,   # Tree cover

    # Water
    80: 2,   # Permanent water bodies

    # Agriculture
    40: 3,   # Cropland

    # Barren
    60: 4,   # Bare / sparse vegetation

    # Built-up
    50: 5    # Built-up
}
