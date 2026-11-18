#!/usr/bin/env python3
"""
Geocode Danish pharmacies using Nominatim (OpenStreetMap).
Adds lattitude_guess and longitude_guess columns to the output.

Usage: python geocode_pharmacies.py
"""

import csv
import requests
import time

INPUT_FILE = 'data/list_pharmacies_inactive_pre.tsv'
OUTPUT_FILE = 'data/list_pharmacies_post_mistral.tsv'

# Cache for coordinates to avoid duplicate API calls
coord_cache = {}

def get_coordinates(city, country='Denmark'):
    """Get latitude and longitude for a city using Nominatim."""
    if city in coord_cache:
        return coord_cache[city]
    
    try:
        # URL encode the city name
        import urllib.parse
        query = urllib.parse.quote(f'{city}, {country}')
        url = f'https://nominatim.openstreetmap.org/search?format=json&q={query}&limit=1'
        
        response = requests.get(
            url, 
            headers={'User-Agent': 'MistralVibe'},
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            if results:
                lat = float(results[0]['lat'])
                lon = float(results[0]['lon'])
                coord_cache[city] = (lat, lon)
                print(f'Got: {city} -> ({lat:.6f}, {lon:.6f})')
                return lat, lon
            else:
                print(f'No result found for: {city}')
    except Exception as e:
        print(f'Error geocoding {city}: {e}')
    
    return None, None

def main():
    print(f'Reading {INPUT_FILE}...')
    
    with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=',')
        rows = list(reader)
    
    # Collect unique cities
    unique_cities = set(row['city'] for row in rows if row.get('city'))
    print(f'Found {len(unique_cities)} unique cities to geocode.')
    
    # Geocode all unique cities
    print('\nGeocoding cities...')
    for city in sorted(unique_cities):
        get_coordinates(city)
        time.sleep(1.1)  # Rate limit: max 1 request per second for Nominatim
    
    # Write output with coordinates
    print('\nWriting output...')
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = rows[0].keys() if rows else []
        fieldnames = list(fieldnames) + ['lattitude_guess', 'longitude_guess']
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        
        for row in rows:
            city = row.get('city', '')
            lat, lon = coord_cache.get(city, (None, None))
            row['lattitude_guess'] = lat if lat is not None else ''
            row['longitude_guess'] = lon if lon is not None else ''
            writer.writerow(row)
    
    print(f'\nDone! Saved {len(rows)} rows to {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
