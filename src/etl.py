"""
Module for data extraction, transformation, and loading operations.
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from .config import NUTRIENT_THRESHOLDS

def extract_nutriments(product: Dict) -> Dict:
    """
    Extract nutriment values from a product dictionary.
    
    Args:
        product (Dict): Product data dictionary
        
    Returns:
        Dict: Extracted nutriment values
    """
    nutriments = product.get('nutriments', {})
    return {
        'energy_100g': nutriments.get('energy_100g', np.nan),
        'proteins_100g': nutriments.get('proteins_100g', np.nan),
        'carbohydrates_100g': nutriments.get('carbohydrates_100g', np.nan),
        'sugars_100g': nutriments.get('sugars_100g', np.nan),
        'fat_100g': nutriments.get('fat_100g', np.nan),
        'saturated-fat_100g': nutriments.get('saturated-fat_100g', np.nan),
        'salt_100g': nutriments.get('salt_100g', np.nan),
        'fiber_100g': nutriments.get('fiber_100g', np.nan)
    }

def compute_nutrient_score(row: pd.Series) -> float:
    """
    Compute a simple nutrient score (0-10) based on nutrient values.
    Higher score = healthier product.
    
    Args:
        row (pd.Series): Row of product data
        
    Returns:
        float: Nutrient score
    """
    score = 5.0  # Start with neutral score
    
    # Add points for healthy nutrients
    if row['proteins_100g'] > NUTRIENT_THRESHOLDS['proteins_100g']['high']:
        score += 2
    elif row['proteins_100g'] > NUTRIENT_THRESHOLDS['proteins_100g']['low']:
        score += 1
        
    if row['fiber_100g'] > 3.5:
        score += 1
        
    # Subtract points for unhealthy nutrients
    if row['sugars_100g'] > NUTRIENT_THRESHOLDS['sugars_100g']['high']:
        score -= 2
    elif row['sugars_100g'] > NUTRIENT_THRESHOLDS['sugars_100g']['low']:
        score -= 1
        
    if row['salt_100g'] > NUTRIENT_THRESHOLDS['salt_100g']['high']:
        score -= 2
    elif row['salt_100g'] > NUTRIENT_THRESHOLDS['salt_100g']['low']:
        score -= 1
        
    if row['saturated-fat_100g'] > 5:
        score -= 1
        
    return max(0, min(10, score))  # Clamp between 0 and 10

def products_to_df(products: List[Dict]) -> pd.DataFrame:
    """
    Convert list of product dictionaries to a pandas DataFrame with transformations.
    
    Args:
        products (List[Dict]): List of product dictionaries
        
    Returns:
        pd.DataFrame: Processed DataFrame
    """
    if not products:
        return pd.DataFrame()
    
    # Create base DataFrame
    df = pd.DataFrame(products)
    
    # Extract nutriments into separate columns
    nutriments_df = pd.DataFrame([
        extract_nutriments(product) for product in products
    ])
    
    # Combine DataFrames
    df = pd.concat([df, nutriments_df], axis=1)
    
    # Clean and transform data
    df['brands'] = df['brands'].str.split(',').str[0]  # Take first brand only
    df['categories'] = df['categories'].str.split(',').str[0]  # Take first category
    df['additives_count'] = df['additives_tags'].str.len()
    df['allergens_count'] = df['allergens_tags'].str.len()
    
    # Compute nutrient score
    df['nutrient_score'] = df.apply(compute_nutrient_score, axis=1)
    
    # Drop unnecessary columns and duplicates
    df = df.drop(['nutriments'], axis=1, errors='ignore')
    df = df.drop_duplicates(subset=['code'])
    
    return df

def save_processed_data(df: pd.DataFrame, filepath: str) -> None:
    """
    Save processed DataFrame to CSV with proper encoding.
    
    Args:
        df (pd.DataFrame): Processed DataFrame
        filepath (str): Path to save the CSV file
    """
    df.to_csv(filepath, index=False, encoding='utf-8') 