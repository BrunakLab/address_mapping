#!/usr/bin/env python3
"""
Add approximate coordinates to pharmacies based on city names.
Uses a local mapping of Danish cities to coordinates.
"""

import csv

# Mapping of Danish cities to approximate coordinates (latitude, longitude)
# Source: Public domain city coordinates for Denmark
DANISH_CITY_COORDS = {
    'København': (55.6761, 12.5683),
    'København V': (55.6867, 12.5250),
    'København N': (55.7089, 12.5461),
    'København S': (55.6607, 12.5833),
    'København Ø': (55.6911, 12.6103),
    'Frederiksberg': (55.6833, 12.5333),
    'Frederiksberg C': (55.6833, 12.5333),
    'Århus': (56.1629, 10.2039),
    'Århus C': (56.1629, 10.2039),
    'Odense': (55.4038, 10.4024),
    'Aalborg': (57.0486, 9.9217),
    'Esbjerg': (55.4667, 8.4500),
    'Randers': (56.4639, 10.0343),
    'Kolding': (55.4961, 9.4861),
    'Horsens': (55.8608, 9.8453),
    'Vejle': (55.7097, 9.5354),
    'Roskilde': (55.6433, 12.0808),
    'Helsingør': (56.0364, 12.6142),
    'Herning': (56.1339, 8.9833),
    'Silkeborg': (56.1706, 9.5503),
    'Næstved': (55.2203, 11.7656),
    'Sønderborg': (54.9092, 9.7850),
    'Svendborg': (55.0586, 10.6111),
    'Hjørring': (57.4667, 9.9833),
    'Thisted': (56.9469, 8.7206),
    'Hillerød': (55.9442, 12.3036),
    'Holstebro': (56.3564, 8.6156),
    'Fredericia': (55.5667, 9.7500),
    'Viborg': (56.4550, 9.4019),
    'Korsør': (55.3333, 11.1500),
    'Slagelse': (55.4081, 11.3675),
    'Nykøbing Falster': (54.7667, 11.8833),
    'Tårnby': (55.6167, 12.6333),
    'Ball Knowle': (55.6167, 12.6333),
    'Brøndby': (55.6464, 12.4625),
    'Gentofte': (55.7500, 12.5500),
    'Lyngby': (55.8000, 12.5000),
    'Glostrup': (55.6667, 12.4333),
    'Rødovre': (55.6750, 12.4417),
    'Albertslund': (55.6500, 12.4000),
    'Hvidovre': (55.6667, 12.4500),
    'Vallensbæk': (55.6667, 12.4333),
    'Ishøj': (55.6333, 12.3667),
    'Høje Taastrup': (55.6667, 12.3000),
    'Furesø': (55.8000, 12.4833),
    'Egedal': (55.7500, 12.2833),
    'Rudersdal': (55.8333, 12.5000),
    'Allerød': (55.9667, 12.5000),
    'Halsnæs': (56.0000, 12.2000),
    'Gribskov': (56.0833, 12.0667),
    'Helsingør': (56.0364, 12.6142),
    'Lolland': (54.8000, 11.8000),
    'Guldborgsund': (54.7667, 11.8833),
    'Vordingborg': (55.0000, 11.9167),
    'Næstved': (55.2203, 11.7656),
    'Faxe': (55.2000, 12.1000),
    'Ringsted': (55.4500, 11.8000),
    'Holbæk': (55.7167, 11.7167),
    'Kalundborg': (55.6833, 11.0833),
    'Sorø': (55.4500, 11.5667),
    'Odsherred': (55.8000, 11.6000),
    'Lejre': (55.6667, 11.9333),
    'Bornholm': (55.1167, 14.9000),
    'Assens': (55.2667, 10.0167),
    'Nordfyn': (55.8000, 9.9000),
    'Odense': (55.4038, 10.4024),
    'Middelfart': (55.5000, 9.7500),
    'Kerteminde': (55.4500, 10.6167),
    'Nyborg': (55.3167, 10.8167),
    'Svendborg': (55.0586, 10.6111),
    'Ærø': (54.8500, 10.4167),
    'Langeland': (55.0000, 10.7000),
    'Faaborg': (55.1000, 10.2333),
    'Faaborg-Midtfyn': (55.1000, 10.2333),
    'Aabenraa': (55.0500, 9.4167),
    'Haderslev': (55.2667, 9.9833),
    'Tønder': (54.9500, 8.9167),
    'Sønderborg': (54.9092, 9.7850),
    'Nordborg': (55.2167, 9.7500),
    'Skive': (56.5667, 9.0333),
    'Struer': (56.5000, 8.6000),
    'Lemvig': (56.5500, 8.3000),
    'Thy': (56.8000, 8.4000),
    'Morsø': (56.8333, 8.6000),
    'Jammerbugt': (57.1000, 9.6000),
    'Rebild': (57.0000, 9.9000),
    'Mariagerfjord': (56.7000, 9.9500),
    'Læsø': (57.2833, 11.0000),
    'Anholt': (56.7167, 11.5167),
    'Samsø': (55.9000, 10.4167),
    'Fanø': (55.5000, 8.4333),
    'Læsø': (57.2833, 11.0000),
    'Ærøskøbing': (54.8667, 10.4000),
    'Marstal': (54.8500, 10.5000),
    'Rudkøbing': (54.8667, 10.7500),
    'Sakskøbing': (54.8333, 11.0500),
    'Nakskov': (54.8333, 11.1333),
    'Stubbekøbing': (54.9000, 11.8667),
    'Ringe': (55.0000, 10.6000),
    'Bogense': (55.5500, 10.0833),
    'Munkebo': (55.4500, 10.6167),
    'Ottrup': (54.9000, 10.0333),
    'Stenlille': (55.4500, 11.7500),
    'Vrå': (57.2000, 9.8000),
    'Jerslev Jylland': (57.2000, 9.8000),
    'Trustrup': (56.4000, 10.4167),
    'Løgumkloster': (55.0333, 8.9000),
    'Hadsund': (56.7167, 10.0167),
}


def get_coordinates(city):
    """Get approximate coordinates for a Danish city."""
    # Try exact match
    if city in DANISH_CITY_COORDS:
        return DANISH_CITY_COORDS[city]
    
    # Try case-insensitive match
    city_lower = city.lower()
    for key, coords in DANISH_CITY_COORDS.items():
        if key.lower() == city_lower:
            return coords
    
    # Try partial match (city contains the key or vice versa)
    for key, coords in DANISH_CITY_COORDS.items():
        if city_lower in key.lower() or key.lower() in city_lower:
            return coords
    
    return None, None


def main():
    input_file = 'data/list_pharmacies_inactive_pre.tsv'
    output_file = 'data/list_pharmacies_post_mistral.tsv'
    
    print(f'Reading {input_file}...')
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=',')
        rows = list(reader)
    
    print(f'Read {len(rows)} rows')
    
    # Add coordinates to each row
    new_rows = []
    for row in rows:
        new_row = dict(row)  # Make a copy
        city = new_row.get('city', '')
        lat, lon = get_coordinates(city)
        new_row['lattitude_guess'] = lat if lat is not None else ''
        new_row['longitude_guess'] = lon if lon is not None else ''
        new_rows.append(new_row)
    
    # Write output
    print(f'Writing {output_file}...')
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        if new_rows:
            fieldnames = list(new_rows[0].keys())
        else:
            fieldnames = []
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        for row in new_rows:
            writer.writerow(row)
    
    print(f'Done! Saved {len(new_rows)} rows to {output_file}')


if __name__ == '__main__':
    main()
