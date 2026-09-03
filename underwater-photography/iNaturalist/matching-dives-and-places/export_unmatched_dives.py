#!/usr/bin/env python3
"""
export_unmatched_dives.py

Compares the location/description tags (<desc>) of all Suunto Eon Core dive workouts
against the canonical site list in `Preferred_dive_site_names.txt`.

Normalizes text (handling smart quotes, case-insensitivity, and common aliases like
'7 Heads' -> 'Seven Heads Pier', 'Barloque' -> 'Barloge Pier', 'Cantys' -> "Canty's Cove").

Generates `unmatched_dives.json` containing:
- Total dive count
- Count and list of matched dives (and their matched preferred location)
- Count and list of unmatched dives for review (e.g. empty descriptions, overseas dive trips,
  or unlisted local sites).
"""

import glob
import json
import os
import re
import unicodedata
import xml.etree.ElementTree as ET

# Base directory and file paths
BASE_DIR = '/Users/astra/github/public/underwater-photography/iNaturalist'
WORKOUTS_DIR = os.path.join(BASE_DIR, 'dive-logs/workouts')
PREF_FILE = os.path.join(BASE_DIR, 'Preferred_dive_site_names.txt')
OUTPUT_FILE = os.path.join(BASE_DIR, 'matching-dives-and-places/unmatched_dives.json')

# Load the preferred location names
with open(PREF_FILE, 'r', encoding='utf-8') as f:
    pref_locations = [line.strip() for line in f if line.strip()]

def clean_str(s):
    """Normalizes unicode characters, replaces typographic quotes, and lowercases text."""
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s)
    s = s.replace('’', "'").replace('‘', "'").replace('`', "'")
    return s.lower()

def match_location(text):
    """
    Attempts to match a dive description against the preferred location list.
    Handles 'Pier' suffix omissions, quote variations, and known aliases.
    """
    if not text:
        return None
    t = clean_str(text)
    for pref in pref_locations:
        p = clean_str(pref).replace('pier', '').strip()
        p = p.replace("'", '')
        t_no_quote = t.replace("'", '')
        if p and p in t_no_quote:
            return pref
        # Common aliases & typo tolerance
        if '7 heads' in t and 'seven heads' in clean_str(pref):
            return pref
        if 'barloque' in t and 'barloge' in clean_str(pref):
            return pref
    return None

# Retrieve and sort all GPX dive files chronologically
gpx_files = sorted(glob.glob(os.path.join(WORKOUTS_DIR, '*.gpx')))

matched_dives = []
unmatched_dives = []

for idx, gpx_path in enumerate(gpx_files, 1):
    fname = os.path.basename(gpx_path)
    
    # Extract date and time from filename
    m = re.match(r'(\d{4}-\d{2}-\d{2})_(\d{2}\.\d{2}\.\d{2})', fname)
    if m:
        date_str, time_str = m.group(1), m.group(2).replace('.', ':')
    else:
        date_str, time_str = fname, ''
    
    # Parse <desc> tag from GPX XML
    desc_text = ''
    try:
        tree = ET.parse(gpx_path)
        desc = tree.getroot().find('.//{http://www.topografix.com/GPX/1/1}desc')
        if desc is not None and desc.text:
            desc_text = desc.text.strip()
    except Exception:
        pass
    
    matched = match_location(desc_text)
    item = {
        'index': idx,
        'date': date_str,
        'time': time_str,
        'raw_description': desc_text if desc_text else '(empty)',
        'filename': fname
    }
    
    if matched:
        item['matched_preferred_location'] = matched
        matched_dives.append(item)
    else:
        unmatched_dives.append(item)

# Build summary payload
summary = {
    'total_dives': len(gpx_files),
    'matched_dives_count': len(matched_dives),
    'unmatched_dives_count': len(unmatched_dives),
    'unmatched_dives': unmatched_dives
}

# Write summary to JSON
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f'Total dives: {len(gpx_files)}')
print(f'Matched dives: {len(matched_dives)}')
print(f'Unmatched dives: {len(unmatched_dives)}')
print(f'Wrote unmatched dives to {OUTPUT_FILE}')
