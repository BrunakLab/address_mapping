#!/usr/bin/env python3
"""
Add approximate coordinates to pharmacies based on city names.
Uses a comprehensive mapping of Danish cities to coordinates.
"""

import csv

# Comprehensive mapping of Danish cities to approximate coordinates (latitude, longitude)
DANISH_CITY_COORDS = {
    # Major cities
    'København': (55.6761, 12.5683),
    'København V': (55.6867, 12.5250),
    'København N': (55.7089, 12.5461),
    'København S': (55.6607, 12.5833),
    'København Ø': (55.6911, 12.6103),
    'København K': (55.6761, 12.5683),
    'København NV': (55.7100, 12.4900),
    'Frederiksberg': (55.6833, 12.5333),
    'Frederiksberg C': (55.6833, 12.5333),
    'Århus': (56.1629, 10.2039),
    'Århus C': (56.1629, 10.2039),
    'Århus N': (56.1800, 10.2100),
    'Odense': (55.4038, 10.4024),
    'Odense C': (55.4038, 10.4024),
    'Odense SV': (55.3800, 10.3800),
    'Aalborg': (57.0486, 9.9217),
    'Aalborg SV': (57.0200, 9.9000),
    'Aalborg SØ': (57.0300, 9.9500),
    'Aalborg Øst': (57.0500, 9.9700),
    'Esbjerg': (55.4667, 8.4500),
    'Randers': (56.4639, 10.0343),
    'Randers NØ': (56.4800, 10.0600),
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
    'Brøndby': (55.6464, 12.4625),
    'Gentofte': (55.7500, 12.5500),
    'Lyngby': (55.8000, 12.5000),
    'Kongens Lyngby': (55.8000, 12.5000),
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
    'Lolland': (54.8000, 11.8000),
    'Guldborgsund': (54.7667, 11.8833),
    'Vordingborg': (55.0000, 11.9167),
    'Faxe': (55.2000, 12.1000),
    'Ringsted': (55.4500, 11.8000),
    'Holbæk': (55.7167, 11.7167),
    'Kalundborg': (55.6833, 11.0833),
    'Sorø': (55.4500, 11.5667),
    'Odsherred': (55.8000, 11.6000),
    'Lejre': (55.6667, 11.9333),
    'Assens': (55.2667, 10.0167),
    'Middelfart': (55.5000, 9.7500),
    'Kerteminde': (55.4500, 10.6167),
    'Nyborg': (55.3167, 10.8167),
    'Langeland': (55.0000, 10.7000),
    'Faaborg': (55.1000, 10.2333),
    'Faaborg-Midtfyn': (55.1000, 10.2333),
    'Aabenraa': (55.0500, 9.4167),
    'Haderslev': (55.2667, 9.9833),
    'Tønder': (54.9500, 8.9167),
    'Nordborg': (55.2167, 9.7500),
    'Skive': (56.5667, 9.0333),
    'Struer': (56.5000, 8.6000),
    'Lemvig': (56.5500, 8.3000),
    'Thy': (56.8000, 8.4000),
    'Morsø': (56.8333, 8.6000),
    'Jammerbugt': (57.1000, 9.6000),
    'Rebild': (57.0000, 9.9000),
    'Mariagerfjord': (56.7000, 9.9500),
    'Bornholm': (55.1167, 14.9000),
    
    # Medium cities and towns
    'Aabybro': (57.1333, 9.6333),
    'Aarup': (55.3333, 10.1000),
    'Allinge': (55.2000, 14.8000),
    'Allingåbro': (56.7833, 10.0667),
    'Aarslev': (55.2833, 10.4500),
    'Aars': (56.8000, 9.5000),
    'Bagsværd': (55.7667, 12.4667),
    'Ballerup': (55.7500, 12.3667),
    'Birkerød': (55.8333, 12.5000),
    'Bjerringbro': (56.4000, 9.6000),
    'Blommenslyst': (55.4167, 10.4333),
    'Brabrand': (56.1667, 10.1167),
    'Brande': (55.7500, 8.9833),
    'Bredebro': (55.0000, 8.6500),
    'Broby': (55.2000, 10.5333),
    'Brovst': (57.1000, 9.1333),
    'Brønderslev': (57.3000, 9.9667),
    'Brønshøj': (55.7167, 12.4333),
    'Brørup': (55.1667, 8.9667),
    'Bylderup-Bov': (54.9667, 9.3667),
    'Bøvlingbjerg': (56.4333, 8.4167),
    'Charlottenlund': (55.8000, 12.5500),
    'Christiansfeld': (55.3500, 9.4833),
    'Dalby': (55.5333, 12.1833),
    'Dragør': (55.6167, 12.6667),
    'Dronninglund': (57.3000, 10.1167),
    'Dyssegård': (55.8000, 12.5333),
    'Ebeltoft': (56.2167, 10.6500),
    'Ejstrupholm': (56.0000, 9.9833),
    'Engesvang': (56.2833, 9.8333),
    'Fakse': (55.2000, 12.1000),
    'Farum': (55.8000, 12.3833),
    'Fjerritslev': (57.1000, 9.4667),
    'Frederikshavn': (57.4500, 10.5667),
    'Frederikssund': (55.8333, 12.0500),
    'Frøstrup': (57.1000, 9.3167),
    'Fuglebjerg': (55.3000, 12.0500),
    'Fårevejle': (55.3667, 11.6667),
    'Gadbjerg': (55.4000, 9.3667),
    'Gilleleje': (56.0833, 12.3000),
    'Glamsbjerg': (55.4167, 10.0833),
    'Glejbjerg': (55.4000, 8.7500),
    'Gredstedbro': (55.1667, 8.5500),
    'Greve': (55.5833, 12.2833),
    'Grindsted': (55.5000, 8.5833),
    'Gråsten': (55.0000, 9.8333),
    'Gudhjem': (55.2167, 14.8667),
    'Gørding': (55.2833, 8.5500),
    'Hadsten': (56.3000, 10.0667),
    'Hals': (57.1667, 10.1500),
    'Harlev Jylland': (56.3000, 9.9500),
    'Havdrup': (55.6000, 12.1333),
    'Hedehusene': (55.6500, 12.2333),
    'Hedensted': (55.8000, 9.7500),
    'Hellerup': (55.7333, 12.5667),
    'Helsinge': (55.9333, 12.4667),
    'Herlev': (55.7333, 12.4500),
    'Hesselager': (55.3000, 10.7667),
    'Hinnerup': (56.2167, 9.6500),
    'Hobro': (56.6667, 10.3000),
    'Holte': (55.8000, 12.5000),
    'Humlebæk': (55.9667, 12.5333),
    'Hurup Thy': (56.8333, 8.4667),
    'Hvalsø': (55.6333, 11.8667),
    'Højbjerg': (55.4667, 10.2000),
    'Hørning': (56.0333, 10.0667),
    'Hørve': (55.5000, 11.6667),
    'Jerslev Sjælland': (55.7667, 12.4833),
    'Jerup': (57.3500, 10.0500),
    'Jordrup': (55.3000, 8.6000),
    'Juelsminde': (55.6500, 10.1167),
    'Jyderup': (55.6500, 11.7667),
    'Jyllinge': (55.7167, 12.1000),
    'Jægerspris': (55.8333, 12.0333),
    'Kalvehave': (55.1000, 12.0500),
    'Karise': (55.3333, 12.0167),
    'Karup Jylland': (56.3500, 8.9500),
    'Kastrup': (55.6333, 12.6333),
    'Kibæk': (55.9167, 8.4833),
    'Kjellerup': (56.1500, 9.5333),
    'Kokkedal': (55.9000, 12.5333),
    'Køge': (55.4500, 12.1833),
    'København K': (55.6761, 12.5683),
    'Langeskov': (55.4000, 10.3000),
    'Langå': (56.3333, 10.0000),
    'Liseleje': (55.9333, 12.1167),
    'Låsby': (55.4000, 8.4667),
    'Løgstør': (56.7833, 9.3000),
    'Løkken': (57.3833, 9.7000),
    'Løgumkloster': (55.0333, 8.9000),
    'Mariager': (56.6667, 10.0000),
    'Maribo': (54.7833, 11.5000),
    'Mårslet': (56.1500, 10.1500),
    'Nimtofte': (55.5333, 11.9333),
    'Nykøbing Mors': (56.7667, 8.8667),
    'Nykøbing Sjælland': (55.9167, 11.6167),
    'Nysted': (54.8667, 11.7167),
    'Nørager': (56.7167, 9.8000),
    'Nørre Alslev': (54.7667, 11.8833),
    'Nørresundby': (57.1000, 9.9167),
    'Oksbøl': (55.6000, 8.2667),
    'Otterup': (55.4167, 10.4167),
    'Præstø': (55.4833, 12.0333),
    'Regstrup': (55.7000, 12.2333),
    'Ribe': (55.3167, 8.7833),
    'Ringkøbing': (56.1000, 8.1333),
    'Risskov': (56.1833, 10.2333),
    'Ry': (56.0000, 9.8500),
    'Rødby': (54.6333, 11.3667),
    'Rødding': (55.5000, 8.7333),
    'Rønne': (55.1167, 14.7500),
    'Sindal': (57.5167, 10.1833),
    'Skagen': (57.7167, 10.5833),
    'Skanderborg': (56.0333, 10.0333),
    'Skibby': (55.7500, 11.9833),
    'Skjern': (55.9500, 8.5000),
    'Skovlunde': (55.7500, 12.4167),
    'Skælskør': (55.2333, 11.2833),
    'Skødstrup': (56.2667, 10.2000),
    'Skørping': (56.7833, 9.8667),
    'Solbjerg': (55.8833, 9.2833),
    'Solrød Strand': (55.5500, 12.2167),
    'Spøttrup': (56.7333, 9.1000),
    'Stege': (55.0000, 12.3000),
    'Stoholm Jylland': (56.4000, 8.9167),
    'Store Heddinge': (55.3667, 12.0167),
    'Storvorde': (56.4333, 8.9667),
    'Svenstrup Jylland': (56.7333, 8.6833),
    'Sæby': (57.2667, 10.5833),
    'Søborg': (55.7333, 12.5167),
    'Søllested': (54.8667, 11.8667),
    'Taastrup': (55.6667, 12.3000),
    'Tarm': (55.9000, 8.3667),
    'Thorsø': (56.4000, 9.6500),
    'Tilst': (56.1333, 10.1000),
    'Tørring': (55.9667, 9.1000),
    'Uldum': (55.9000, 9.9167),
    'Ulfborg': (56.4167, 8.3167),
    'Valby': (55.6667, 12.4667),
    'Vallensbæk Strand': (55.6333, 12.4167),
    'Vamdrup': (55.4333, 9.4000),
    'Vanløse': (55.7167, 12.4667),
    'Vedbæk': (55.8333, 12.5333),
    'Vejen': (55.5000, 9.1333),
    'Vejers Strand': (55.5500, 8.1833),
    'Vester Skerninge': (55.4500, 10.6333),
    'Viby Jylland': (56.1500, 10.2167),
    'Vildbjerg': (56.0667, 8.9500),
    'Vinderup': (56.4333, 8.4833),
    'Virum': (55.8333, 12.5167),
    'Vissenbjerg': (55.4167, 10.1500),
    'Værløse': (55.7833, 12.5000),
    'Åbyhøj': (56.1500, 10.1333),
    'Ølgod': (55.3167, 8.6667),
    'Ølstykke': (55.8333, 12.1667),
    'Øster Ulslev': (55.0000, 11.0833),
    'Øster Vrå': (57.5000, 10.1000),
    'Hadsund': (56.7167, 10.0167),
    'Bogense': (55.5500, 10.0833),
    'Jerslev Jylland': (57.2000, 9.8000),
    'Marstal': (54.8500, 10.5000),
    'Rudkøbing': (54.8667, 10.7500),
    'Samsø': (55.9000, 10.4167),
    'Stenlille': (55.4500, 11.7500),
    'Stubbekøbing': (54.9000, 11.8667),
    'Trustrup': (56.4000, 10.4167),
    'Ærøskøbing': (54.8667, 10.4000),
    'Årslev': (55.4167, 10.1000),
}


def get_coordinates(city):
    """Get approximate coordinates for a Danish city."""
    if not city:
        return None, None
    
    # Try exact match
    if city in DANISH_CITY_COORDS:
        return DANISH_CITY_COORDS[city]
    
    # Try case-insensitive match
    city_lower = city.lower()
    for key, coords in DANISH_CITY_COORDS.items():
        if key.lower() == city_lower:
            return coords
    
    # Try partial match
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
        new_row = dict(row)
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
