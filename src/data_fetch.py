"""
Module for fetching data from the OpenFoodFacts API.
"""

import requests
from tqdm import tqdm
from typing import List, Dict, Optional
from .config import BASE_URL, COUNTRY, PAGE_SIZE, REQUIRED_FIELDS

def fetch_products(page: int = 1) -> List[Dict]:
    """
    Fetch a single page of products from OpenFoodFacts API.
    
    Args:
        page (int): Page number to fetch
        
    Returns:
        List[Dict]: List of product dictionaries
    """
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        'action': 'process',
        'tagtype_0': 'countries',
        'tag_contains_0': 'contains',
        'tag_0': COUNTRY,
        'page_size': PAGE_SIZE,
        'page': page,
        'json': 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('products', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {str(e)}")
        return []

def fetch_all_products(max_pages: int = 100) -> List[Dict]:
    """
    Fetch all products from OpenFoodFacts API up to max_pages.
    
    Args:
        max_pages (int): Maximum number of pages to fetch
        
    Returns:
        List[Dict]: Combined list of all products
    """
    all_products = []
    
    with tqdm(total=max_pages, desc="Fetching products") as pbar:
        for page in range(1, max_pages + 1):
            products = fetch_products(page)
            if not products:
                break
            
            # Filter products to include only required fields
            filtered_products = []
            for product in products:
                filtered_product = {
                    field: product.get(field, None) 
                    for field in REQUIRED_FIELDS
                }
                filtered_products.append(filtered_product)
            
            all_products.extend(filtered_products)
            pbar.update(1)
            
    return all_products

def fetch_product_by_code(barcode: str) -> Optional[Dict]:
    """
    Fetch a single product by its barcode.
    
    Args:
        barcode (str): Product barcode
        
    Returns:
        Optional[Dict]: Product data if found, None otherwise
    """
    url = f"{BASE_URL}/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 1:
            return data.get('product')
        return None
    except requests.exceptions.RequestException:
        return None 