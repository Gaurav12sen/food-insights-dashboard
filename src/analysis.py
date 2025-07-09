"""
Module for data analysis and insights generation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def get_summary_stats(df: pd.DataFrame) -> Dict:
    """
    Calculate summary statistics for the dataset.
    
    Args:
        df (pd.DataFrame): Product DataFrame
        
    Returns:
        Dict: Summary statistics
    """
    return {
        'total_products': len(df),
        'unique_brands': df['brands'].nunique(),
        'unique_categories': df['categories'].nunique(),
        'avg_nutrient_score': round(df['nutrient_score'].mean(), 2),
        'data_completeness': round(df.count().mean() / len(df) * 100, 1),
        'products_with_allergens': round(df['allergens_count'].gt(0).mean() * 100, 1),
        'products_with_additives': round(df['additives_count'].gt(0).mean() * 100, 1)
    }

def top_brands(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get top brands by product count.
    
    Args:
        df (pd.DataFrame): Product DataFrame
        n (int): Number of top brands to return
        
    Returns:
        pd.DataFrame: Top brands with counts
    """
    # Get value counts
    brand_counts = df['brands'].value_counts()
    
    # Create DataFrame with explicit column names
    result = pd.DataFrame({
        'brand': brand_counts.index,
        'product_count': brand_counts.values
    })
    
    # Take top n rows
    result = result.head(n)
    
    # Debug print
    print("Debug - top_brands columns:", result.columns.tolist())
    print("Debug - top_brands head:", result.head())
    
    return result

def nutrient_distribution(df: pd.DataFrame, nutrient: str) -> Dict:
    """
    Calculate distribution statistics for a nutrient.
    
    Args:
        df (pd.DataFrame): Product DataFrame
        nutrient (str): Name of nutrient column
        
    Returns:
        Dict: Distribution statistics
    """
    return {
        'mean': round(df[nutrient].mean(), 2),
        'median': round(df[nutrient].median(), 2),
        'std': round(df[nutrient].std(), 2),
        'min': round(df[nutrient].min(), 2),
        'max': round(df[nutrient].max(), 2),
        'q25': round(df[nutrient].quantile(0.25), 2),
        'q75': round(df[nutrient].quantile(0.75), 2)
    }

def category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze nutrient profiles by category.
    
    Args:
        df (pd.DataFrame): Product DataFrame
        
    Returns:
        pd.DataFrame: Category-level statistics
    """
    return df.groupby('categories').agg({
        'nutrient_score': 'mean',
        'sugars_100g': 'mean',
        'fat_100g': 'mean',
        'salt_100g': 'mean',
        'proteins_100g': 'mean',
        'code': 'count'
    }).round(2).reset_index().rename(columns={'code': 'product_count'})

def get_healthiest_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get top n healthiest products based on nutrient score.
    
    Args:
        df (pd.DataFrame): Product DataFrame
        n (int): Number of products to return
        
    Returns:
        pd.DataFrame: Top n healthiest products
    """
    columns = ['product_name', 'brands', 'categories', 'nutrient_score', 
              'proteins_100g', 'sugars_100g', 'fat_100g', 'salt_100g']
    return df.nlargest(n, 'nutrient_score')[columns]

def get_additive_prevalence(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Analyze most common additives.
    
    Args:
        df (pd.DataFrame): Product DataFrame
        n (int): Number of top additives to return
        
    Returns:
        pd.DataFrame: Top n most common additives
    """
    # Get additive counts
    additive_counts = df['additives_tags'].explode().value_counts()
    
    # Create DataFrame with explicit column names
    result = pd.DataFrame({
        'additive': additive_counts.index,
        'occurrence_count': additive_counts.values
    })
    
    # Take top n rows
    result = result.head(n)
    
    # Calculate percentage
    result['percentage'] = round(result['occurrence_count'] / len(df) * 100, 1)
    
    # Debug print
    print("Debug - additives columns:", result.columns.tolist())
    print("Debug - additives head:", result.head())
    
    return result

def get_data_quality_metrics(df: pd.DataFrame) -> Dict:
    """
    Calculate data quality metrics.
    
    Args:
        df (pd.DataFrame): Product DataFrame
        
    Returns:
        Dict: Data quality metrics
    """
    return {
        'missing_values': df.isnull().mean().round(3).to_dict(),
        'completeness_score': round(df.count().mean() / len(df) * 100, 1),
        'duplicate_products': len(df) - df['code'].nunique(),
        'products_with_images': round(df['image_url'].notna().mean() * 100, 1)
    } 