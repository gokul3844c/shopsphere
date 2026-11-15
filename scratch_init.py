import json
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
MEDIA_PRODUCTS = BASE_DIR / "media" / "products"
STATIC_IMAGES = BASE_DIR / "static" / "images"
FIXTURES_DIR = BASE_DIR / "catalog" / "fixtures"

MEDIA_PRODUCTS.mkdir(parents=True, exist_ok=True)
STATIC_IMAGES.mkdir(parents=True, exist_ok=True)
FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

# Create a clean SVG placeholder
placeholder_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
  <rect width="400" height="400" fill="#f8fafc"/>
  <rect x="40" y="40" width="320" height="320" rx="16" fill="#edf2f7" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="200" cy="180" r="50" fill="#cbd5e1"/>
  <path d="M120 280 L170 210 L220 280 L250 240 L280 280 Z" fill="#94a3b8"/>
  <text x="200" y="325" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="16" font-weight="600" fill="#64748b" text-anchor="middle">ShopSphere Product</text>
</svg>"""

with open(STATIC_IMAGES / "placeholder.svg", "w", encoding="utf-8") as f:
    f.write(placeholder_svg)

print("Created placeholder.svg")
