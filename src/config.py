"""
Configuration settings for the OpenFoodFacts India Dashboard.
"""

# API Configuration
BASE_URL = "https://world.openfoodfacts.org"
COUNTRY = "india"
PAGE_SIZE = 1000

# Data Processing Settings
REQUIRED_FIELDS = [
    'code',
    'product_name',
    'brands',
    'categories',
    'nutriments',
    'additives_tags',
    'allergens_tags',
    'ingredients_text',
    'nutrition_grades',
    'image_url',
]

# Nutrient Thresholds (per 100g/ml)
NUTRIENT_THRESHOLDS = {
    'sugars_100g': {'low': 5, 'high': 22.5},
    'fat_100g': {'low': 3, 'high': 17.5},
    'salt_100g': {'low': 0.3, 'high': 1.5},
    'proteins_100g': {'low': 8, 'high': 20},
}

# Cache Settings
CACHE_EXPIRY = 3600  # 1 hour in seconds
DATA_REFRESH_INTERVAL = 86400  # 24 hours in seconds 