#!/usr/bin/env python3
"""
generate_dives_table.py

Parses all Suunto Eon Core dive workout GPX files in the `workouts/` directory,
extracts the dive date, timestamp, user description/notes (<desc>), and filename,
and generates a structured markdown summary table in `dives_table.md`.
"""

import glob
import os
import re
import xml.etree.ElementTree as ET

# Base directories and file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKOUTS_DIR = os.path.join(BASE_DIR, 'workouts')
OUTPUT_PATH = os.path.join(BASE_DIR, 'dives_table.md')

# Retrieve and sort all GPX dive files chronologically
gpx_files = sorted(glob.glob(os.path.join(WORKOUTS_DIR, '*.gpx')))

# Initialize Markdown table header
lines = [
    '# Dive Logs Table\n',
    f'Total dives recorded: **{len(gpx_files)}**\n',
    '| # | Date | Time | Location / Place Description | Filename |',
    '| :--- | :--- | :--- | :--- | :--- |'
]

for idx, gpx_path in enumerate(gpx_files, 1):
    fname = os.path.basename(gpx_path)
    
    # Extract date (YYYY-MM-DD) and time (HH:MM:SS) from standard filename pattern
    # Example: 2026-08-29_10.09.23-scubadiving.gpx
    m = re.match(r'(\d{4}-\d{2}-\d{2})_(\d{2}\.\d{2}\.\d{2})', fname)
    if m:
        date_str, time_str = m.group(1), m.group(2).replace('.', ':')
    else:
        date_str, time_str = fname, ''
    
    # Extract location or log note from GPX metadata <desc> tag
    desc_text = ''
    try:
        tree = ET.parse(gpx_path)
        root = tree.getroot()
        desc = root.find('.//{http://www.topografix.com/GPX/1/1}desc')
        if desc is not None and desc.text:
            # Escape pipes to avoid breaking the markdown table syntax
            desc_text = desc.text.strip().replace('|', '-')
    except Exception:
        desc_text = ''
    
    lines.append(f'| {idx} | {date_str} | {time_str} | {desc_text} | `{fname}` |')

# Save generated table to dives_table.md
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f'Successfully wrote {len(gpx_files)} dives to {OUTPUT_PATH}')
