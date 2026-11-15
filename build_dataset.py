import json
import os
from pathlib import Path
from decimal import Decimal

BASE_DIR = Path(__file__).resolve().parent
MEDIA_PRODUCTS = BASE_DIR / "media" / "products"
STATIC_IMAGES = BASE_DIR / "static" / "images"
FIXTURES_DIR = BASE_DIR / "catalog" / "fixtures"

MEDIA_PRODUCTS.mkdir(parents=True, exist_ok=True)
STATIC_IMAGES.mkdir(parents=True, exist_ok=True)
FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES_DATA = [
    {
        "name": "Electronics",
        "slug": "electronics",
        "color": "#3b82f6",
        "icon": "⚡",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
        "products": [
            ("Noise-Cancelling Over-Ear Headphones", "SoundPeak", 4999, 7999, 35, 4.6, 320, True,
             "Premium active noise cancelling wireless headphones with 40-hour battery life and ultra-comfortable memory foam earcups.",
             {"Battery Life": "40 Hours", "Connectivity": "Bluetooth 5.3, 3.5mm AUX", "Driver": "40mm Neodymium", "Warranty": "1 Year Manufacturer"},
             "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"),
            ("Compact Bluetooth Soundbar 80W", "EchoWave", 3499, 5499, 22, 4.4, 185, False,
             "Immersive home theatre soundbar featuring deep bass reflex ports, HDMI ARC, optical input, and Bluetooth streaming.",
             {"Output Power": "80W RMS", "Inputs": "HDMI ARC, Optical, AUX, USB", "Dimensions": "78 x 6.5 x 6.5 cm", "Warranty": "1 Year"},
             "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800"),
            ("Smart 4K Ultra HD Streaming Box", "VisionStream", 2999, 4499, 40, 4.5, 412, True,
             "Streaming player with Dolby Vision, HDR10+, voice remote with Google Assistant, and access to thousands of apps.",
             {"Resolution": "4K UHD @ 60fps", "Audio": "Dolby Atmos pass-through", "RAM/Storage": "2GB / 16GB", "Warranty": "1 Year"},
             "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=800"),
            ("True Wireless Earbuds with ANC", "AeroPods", 1999, 3999, 65, 4.3, 890, False,
             "Active noise cancellation, environmental noise cancellation for crystal clear calls, and IPX5 water resistance.",
             {"Playtime": "32 Hours with Case", "Water Resistance": "IPX5", "Charging": "USB Type-C Fast Charge", "Warranty": "1 Year"},
             "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800"),
            ("Outdoor Weatherproof Security Camera", "SafeEye", 2799, 4299, 18, 4.2, 94, False,
             "1080p full HD outdoor surveillance camera with infrared color night vision, motion tracking, and two-way audio.",
             {"Resolution": "1080p Full HD", "Field of View": "130 degrees", "Storage": "MicroSD up to 128GB & Cloud", "Weatherproof": "IP66"},
             "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=800"),
            ("Rugged Portable Waterproof Speaker", "BoomGo", 1599, 2499, 50, 4.7, 630, True,
             "Compact travel speaker delivering surprisingly punchy bass and 360-degree sound. IP67 waterproof and dustproof.",
             {"Battery Life": "14 Hours", "Waterproof Rating": "IP67", "Bluetooth": "v5.2", "Weight": "380g"},
             "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800"),
            ("4K Action Camera with Dual Screens", "ApexCam", 6999, 10999, 15, 4.3, 145, False,
             "Capture sports and underwater adventures in crisp 4K 60FPS with 6-axis electronic image stabilization.",
             {"Video": "4K@60fps, 1080p@120fps", "Photo": "20MP", "Waterproof": "30m with case", "Battery": "1350mAh"},
             "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800"),
            ("Smart Dimmable LED Desk Lamp", "LumiDesk", 1299, 1999, 45, 4.5, 278, False,
             "Eye-care LED desk lamp with 5 color temperatures, slide touch brightness dimmer, and integrated USB charging port.",
             {"Brightness Levels": "5 Modes, 10 Brightness levels", "CRI": "> 90", "Power": "12W", "Timer": "45 min auto-off"},
             "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800"),
            ("Fast Power Bank 20000mAh 22.5W", "VoltMax", 1499, 2299, 75, 4.6, 1150, True,
             "High-capacity portable charger with Power Delivery 3.0 and Quick Charge 3.0. Charges three devices simultaneously.",
             {"Capacity": "20000mAh 74Wh", "Outputs": "2x USB-A, 1x USB-C PD", "Input": "Type-C 18W", "Weight": "420g"},
             "https://images.unsplash.com/photo-1609592426868-45e054527787?w=800"),
            ("Mini Foldable GPS Drone with HD Camera", "SkyScout", 8499, 13999, 12, 4.1, 88, False,
             "Beginner-friendly quadcopter with optical flow hovering, GPS return-to-home, and live FPV Wi-Fi video transmission.",
             {"Flight Time": "22 Minutes", "Camera": "2.7K HD Tiltable", "Range": "500m", "Weight": "249g (No License Required)"},
             "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=800"),
            ("Smart Wi-Fi Plug with Energy Monitor 16A", "PlugLink", 799, 1299, 90, 4.4, 530, False,
             "Control heavy appliances like geysers, ACs and heaters remotely. Works with Alexa and Google Assistant.",
             {"Max Load": "16A, 3680W", "Wi-Fi": "2.4 GHz 802.11 b/g/n", "App Support": "iOS & Android", "Features": "Timer & Schedule"},
             "https://images.unsplash.com/photo-1558002038-1055907df827?w=800"),
            ("Studio Cardioid USB Condenser Microphone", "VocalCraft", 3299, 4999, 28, 4.6, 210, False,
             "Plug and play studio microphone ideal for podcasting, streaming, voiceovers, and gaming. Includes pop filter and shock mount.",
             {"Polar Pattern": "Cardioid", "Sample Rate": "192kHz/24bit", "Cable Length": "2m USB-A to B", "Mount": "Heavy Metal Base"},
             "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800"),
            ("Digital Alarm Clock with Wireless Charging", "ChronoPad", 1199, 1799, 38, 4.3, 160, False,
             "Multi-functional bedside digital LED clock with Qi 10W wireless charging pad, temperature display, and dimmable display.",
             {"Charging Output": "10W / 7.5W / 5W", "Display": "White LED, 3 brightness levels", "Material": "ABS + Fabric", "Power": "Type-C cable included"},
             "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800"),
        ]
    },
    {
        "name": "Computers",
        "slug": "computers",
        "color": "#6366f1",
        "icon": "💻",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800",
        "products": [
            ("SphereBook 15.6-inch Thin & Light Laptop", "SphereTech", 42999, 58999, 14, 4.5, 92, True,
             "FHD IPS anti-glare display, Intel Core i5 12th Gen, 16GB DDR4 RAM, 512GB PCIe NVMe SSD, backlit keyboard, Windows 11.",
             {"Processor": "Intel Core i5-1235U", "RAM": "16GB DDR4", "Storage": "512GB NVMe SSD", "Display": "15.6 inch FHD IPS", "Battery": "Up to 8.5 Hours"},
             "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800"),
            ("27-inch 4K UHD IPS Frameless Monitor", "ViewMaster", 19999, 27999, 19, 4.6, 230, True,
             "Ultra-sharp 3840x2160 resolution with 99% sRGB color gamut, HDR400, USB-C 65W power delivery, and height-adjustable stand.",
             {"Screen Size": "27 Inch (68.5 cm)", "Resolution": "3840 x 2160 Pixels (4K)", "Refresh Rate": "60Hz", "Ports": "HDMI 2.0, DP 1.4, USB-C"},
             "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800"),
            ("Portable External NVMe SSD 1TB USB 3.2", "FlashDrive", 6499, 9499, 45, 4.8, 620, True,
             "Blazing-fast read speeds up to 1050 MB/s. Compact drop-resistant aluminum enclosure with USB-C to C and C to A cables.",
             {"Capacity": "1 TB", "Speed": "Up to 1050 MB/s Read", "Interface": "USB 3.2 Gen 2 (Type-C)", "Durability": "2-meter drop protection"},
             "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800"),
            ("Ergonomic Vertical Wireless Mouse", "OptiGrip", 1299, 1999, 55, 4.4, 340, False,
             "Natural handshake position reduces wrist strain. 6 buttons, silent clicks, adjustable DPI (800/1200/1600), rechargeable battery.",
             {"DPI Levels": "800 - 1200 - 1600", "Connection": "2.4GHz USB Receiver", "Battery": "500mAh Rechargeable Li-ion", "Weight": "110g"},
             "https://images.unsplash.com/photo-1527814050087-3793815479db?w=800"),
            ("8-in-1 Aluminum USB-C Hub Multiport Adapter", "PortCraft", 1899, 2999, 60, 4.5, 480, False,
             "Expands your USB-C port to 4K HDMI, 100W Power Delivery, Gigabit Ethernet, SD/TF card reader, and 3x USB 3.0 ports.",
             {"HDMI": "4K @ 30Hz", "Power Delivery": "Up to 100W Pass-through", "Ethernet": "RJ45 1000Mbps", "Material": "Aluminum Alloy"},
             "https://images.unsplash.com/photo-1544652478-6653e09f18a2?w=800"),
            ("Pro HD 1080p Streaming Webcam with Privacy Shutter", "ClearCam", 1799, 2799, 40, 4.3, 215, False,
             "Full HD glass lens with auto light correction, dual stereo noise-canceling mics, and a magnetic physical privacy cover.",
             {"Resolution": "1080p @ 30fps", "Focus Type": "Autofocus", "Microphone": "Built-in Dual Stereo", "Interface": "USB 2.0 Plug & Play"},
             "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800"),
            ("Mechanical Gaming Keyboard RGB Hot-Swappable", "KeyForge", 2999, 4499, 32, 4.7, 510, True,
             "Tenkeyless 87-key compact mechanical keyboard with custom red linear switches, per-key RGB backlighting, and braided cable.",
             {"Switch Type": "Red Linear Mechanical", "Layout": "Tenkeyless (87 Keys)", "Backlight": "16.8 Million Colors RGB", "Keycaps": "Double-shot PBT"},
             "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800"),
            ("Wi-Fi 6 Dual-Band Mesh Router AX1800", "NetSphere", 3799, 5999, 25, 4.5, 175, False,
             "Next-gen speeds up to 1.8 Gbps. Connect up to 40 devices seamlessly with OFDMA and MU-MIMO technology.",
             {"Wi-Fi Standard": "Wi-Fi 6 (802.11ax)", "Speed": "574 Mbps (2.4GHz) + 1201 Mbps (5GHz)", "Coverage": "Up to 2,000 sq ft", "Antennas": "4 External High-Gain"},
             "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=800"),
            ("Aluminum Ventilated Laptop Cooling Stand", "AluRiser", 999, 1599, 70, 4.6, 730, False,
             "Heavy-duty sandblasted aluminum stand elevates laptop screen to eye level. Folds flat for effortless portability.",
             {"Material": "Premium Aluminum Alloy", "Compatibility": "10 to 17 inch laptops", "Adjustment": "6 Ergonomic Angles", "Weight Capacity": "Up to 15 kg"},
             "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800"),
            ("Graphic Drawing Pen Tablet 10x6 inch", "ArtisPen", 3499, 5299, 20, 4.4, 130, False,
             "Battery-free stylus with 8192 levels of pressure sensitivity, tilt recognition, and 8 customizable shortcut express keys.",
             {"Active Area": "10 x 6.25 inches", "Pressure Sensitivity": "8192 Levels", "Report Rate": "266 PPS", "OS Support": "Windows, Mac, Android"},
             "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=800"),
            ("Heavy Duty Under-Desk Cable Management Tray", "TidyWire", 699, 1099, 85, 4.5, 390, False,
             "No-drill clamp mounting under-desk wire organizer basket. Keeps power strips, charger bricks, and cords neatly hidden.",
             {"Mounting": "Clamp-on (No Drilling)", "Material": "Carbon Steel Wire", "Dimensions": "40 x 16 x 15 cm", "Max Load": "10 kg"},
             "https://images.unsplash.com/photo-1595053826286-2e59ef79ff18?w=800"),
            ("Curved 34-inch WQHD Gaming Monitor 144Hz", "CurveVision", 32999, 44999, 8, 4.7, 85, True,
             "1500R curvature panoramic 21:9 ultrawide panel, 1ms response time, AMD FreeSync Premium, dual HDMI and DisplayPort.",
             {"Screen Size": "34 Inch Curved (1500R)", "Resolution": "3440 x 1440 WQHD", "Refresh Rate": "144Hz", "Response Time": "1ms MPRT"},
             "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800"),
            ("Waterproof Neoprene Laptop Sleeve 14-inch", "ShieldCase", 649, 999, 65, 4.3, 290, False,
             "Shock-absorbing plush fleece interior padding with accessory front zipper pocket for mouse and charger.",
             {"Size Compatibility": "13.3 - 14.1 inch", "Material": "Water-resistant Neoprene", "Pockets": "Main compartment + Front zip", "Color": "Slate Grey"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
        ]
    },
    {
        "name": "Mobile Phones",
        "slug": "mobile-phones",
        "color": "#0ea5e9",
        "icon": "📱",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
        "products": [
            ("SpherePhone Apex 5G (8GB RAM, 128GB)", "SphereMobile", 18999, 24999, 25, 4.4, 450, True,
             "6.67-inch AMOLED 120Hz display, Snapdragon 7 Gen 2, 64MP OIS primary camera, 5000mAh battery with 67W fast charging.",
             {"Processor": "Snapdragon 7 Gen 2 5G", "RAM": "8GB LPDDR5", "Storage": "128GB UFS 3.1", "Display": "6.67 inch FHD+ 120Hz AMOLED", "Camera": "64MP OIS + 8MP Wide + 2MP Macro"},
             "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800"),
            ("SpherePhone Titan Pro 5G (12GB RAM, 256GB)", "SphereMobile", 28999, 36999, 18, 4.7, 310, True,
             "Flagship camera phone with Sony IMX890 sensor, Hasselblad color tuning, 100W SUPERVOOC charging, and curved 1.5K display.",
             {"Processor": "Snapdragon 8+ Gen 1", "RAM": "12GB", "Storage": "256GB", "Battery": "5000mAh with 100W Charger", "Display": "1.5K 120Hz Curved AMOLED"},
             "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=800"),
            ("Nova Lite 4G Smartphone (4GB RAM, 64GB)", "NovaTech", 7999, 10999, 45, 4.1, 520, False,
             "Budget champion featuring 6.5-inch HD+ 90Hz screen, 50MP AI camera, octa-core processor, and huge 6000mAh battery.",
             {"Display": "6.5 inch HD+ 90Hz", "RAM/ROM": "4GB / 64GB (Expandable 1TB)", "Battery": "6000mAh", "Camera": "50MP Dual AI Camera"},
             "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=800"),
            ("65W GaN 3-Port Fast Wall Charger", "VoltSpeed", 1699, 2499, 60, 4.6, 680, True,
             "Next-generation Gallium Nitride (GaN) technology charges laptops, tablets, and phones simultaneously in an ultra-compact body.",
             {"Total Output": "65W Max", "Ports": "2x USB-C PD 3.0, 1x USB-A QC 3.0", "Technology": "GaN III Chip", "Safety": "Overvoltage & Temperature Protection"},
             "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800"),
            ("Wireless Magnetic Charging Stand 15W", "MagSphere", 1499, 2299, 42, 4.4, 290, False,
             "Snap and charge effortlessly in portrait or landscape mode. Strong magnetic alignment with LED indicator light.",
             {"Output": "15W / 10W / 7.5W Fast Charge", "Compatibility": "MagSafe compatible & Qi devices", "Cable": "1.2m USB-C Cable Included", "Angle": "30-degree tilt"},
             "https://images.unsplash.com/photo-1622445262464-84b1456045b6?w=800"),
            ("3-Axis Handheld Smartphone Gimbal Stabilizer", "GimbalPro", 5499, 8999, 16, 4.5, 140, True,
             "Smooth cinematic smartphone stabilization with face tracking, gesture controls, time-lapse modes, and built-in extension rod.",
             {"Stabilization": "3-Axis Mechanical", "Battery Life": "8 Hours", "Payload": "Up to 290g", "App Features": "Object Tracking, Panorama, Hitchock Zoom"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
            ("Heavy-Duty Ring Kickstand Phone Case", "ArmorShield", 499, 899, 110, 4.3, 840, False,
             "Military-grade drop protection with dual-layer shock absorption, rotating magnetic ring stand, and raised bezel camera guards.",
             {"Protection": "MIL-STD-810G Drop Tested", "Material": "Hard PC + Flexible TPU", "Features": "360-degree Ring Stand", "Compatibility": "Multiple Models"},
             "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800"),
            ("Tempered Glass Screen Protector 9H [2-Pack]", "ClearShield", 299, 599, 150, 4.5, 1420, False,
             "Edge-to-edge full coverage 9H hardness tempered glass with oleophobic coating against fingerprints and smudges.",
             {"Hardness": "9H Surface Hardness", "Thickness": "0.33mm Ultra-Thin", "Coating": "Hydrophobic & Oleophobic", "Pack Contains": "2 Glasses + Easy Alignment Frame"},
             "https://images.unsplash.com/photo-1584006682522-dc17d6c0d9ac?w=800"),
            ("Magnetic Air Vent Car Phone Mount Holder", "DriveEase", 399, 799, 95, 4.4, 610, False,
             "Ultra-strong neodymium magnets securely hold phone on bumpy roads. 360-degree ball joint for optimal viewing angle.",
             {"Mount Type": "Air Vent Clip with Twist Lock", "Magnets": "6x N52 Strong Magnets", "Rotation": "360 Degree", "Color": "Matte Black"},
             "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=800"),
            ("Braided USB-C to USB-C Fast Cable [2-Pack 2M]", "DuraCord", 449, 799, 120, 4.7, 980, False,
             "Durable double-braided nylon cord rated for 20,000+ bends. Supports 100W PD charging and 480Mbps data sync.",
             {"Length": "2 Meters (6.6 ft)", "Power": "Up to 100W (20V/5A)", "Data Rate": "480 Mbps", "Material": "Braided Nylon & Aluminum Connectors"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
            ("Universal Waterproof Phone Pouch IPX8 [Pack of 2]", "DrySeal", 349, 699, 80, 4.2, 330, False,
             "Certified IPX8 waterproof down to 30 meters. Transparent touch-sensitive windows for underwater photos and swimming.",
             {"Waterproof Rating": "IPX8 (30 Meters)", "Touch Compatible": "Yes (Capacitive)", "Fit": "Phones up to 7.0 inches", "Includes": "2 Pouches + 2 Lanyards"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
            ("Clip-On LED Selfie Ring Light for Phones", "GlowGrip", 399, 699, 65, 4.3, 275, False,
             "Rechargeable compact ring light with 3 light modes (warm, cool, mixed) and step-less dimming for flattering video calls.",
             {"LED Count": "36 High-CRI Beads", "Battery": "Built-in 200mAh Rechargeable", "Mount": "Soft Silicone Padded Clip", "Diameter": "8.5 cm"},
             "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=800"),
            ("Dual USB Fast Car Charger 38W Metal", "SpeedDrive", 599, 999, 75, 4.6, 420, False,
             "All-metal zinc alloy body with 20W PD Type-C port and 18W QC 3.0 USB-A port with soft blue LED ring light.",
             {"Total Output": "38W Dual Fast Charge", "Input": "DC 12V-24V", "Material": "Zinc Alloy", "Protection": "Multi-protect Safety System"},
             "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=800"),
        ]
    },
    {
        "name": "Fashion",
        "slug": "fashion",
        "color": "#ec4899",
        "icon": "👔",
        "image_url": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800",
        "products": [
            ("Classic Oxford Pure Cotton Formal Shirt", "UrbanGent", 1299, 2199, 40, 4.4, 380, True,
             "Crafted from 100% long-staple breathable cotton. Tailored regular fit with button-down collar and chest patch pocket.",
             {"Fabric": "100% Breathable Cotton", "Fit": "Regular Fit", "Sleeve": "Full Sleeve", "Care": "Machine Wash Warm"},
             "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800"),
            ("Slim Fit Stretch Chino Trousers", "MetroWeave", 1499, 2499, 35, 4.3, 290, False,
             "Versatile flat-front chinos crafted from cotton twill with 2% elastane for unrestricted day-to-night flexibility.",
             {"Material": "98% Cotton, 2% Elastane", "Closure": "Button & Zip Fly", "Pockets": "4 Pockets", "Fit": "Slim Fit"},
             "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800"),
            ("All-Weather Waterproof Windbreaker Jacket", "SummitPeak", 2499, 3999, 24, 4.6, 175, True,
             "Breathable lightweight outdoor shell jacket with taped seams, adjustable hood, and zippered weather-sealed pockets.",
             {"Shell": "100% Ripstop Polyester", "Waterproofing": "5000mm Hydrostatic Head", "Features": "Packable into pocket", "Seasons": "Monsoon & Winter"},
             "https://images.unsplash.com/photo-1544441893-675973e31985?w=800"),
            ("Polarized Classic Aviator Sunglasses UV400", "SolarRay", 999, 1799, 50, 4.5, 480, True,
             "Timeless stainless steel metal frames with scratch-resistant TAC polarized lenses that eliminate harmful reflective glare.",
             {"Lens Material": "Triacetate Cellulose (TAC) Polarized", "UV Protection": "100% UV400", "Frame": "Corrosion-resistant Alloy", "Includes": "Hard Leather Case"},
             "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800"),
            ("Genuine Top-Grain Leather Bi-Fold Wallet", "HideCraft", 899, 1499, 65, 4.7, 720, False,
             "Handcrafted vintage leather wallet with RFID blocking lining, 8 card slots, 2 currency compartments, and coin pouch.",
             {"Leather": "Top-Grain Cowhide Leather", "Security": "RFID Blocking Layer", "Dimensions": "11.5 x 9.5 x 1.8 cm", "Warranty": "6 Months"},
             "https://images.unsplash.com/photo-1627123424574-724758594e93?w=800"),
            ("Minimalist Analog Quartz Watch with Mesh Strap", "AuraTime", 1999, 3499, 30, 4.5, 240, True,
             "Ultra-thin 7mm stainless steel watch case with scratch-proof sapphire crystal glass and quick-release Milanese mesh band.",
             {"Movement": "Japanese Miyota Quartz", "Case Diameter": "40mm", "Water Resistance": "3 ATM (Splash Resistant)", "Strap": "Stainless Steel Mesh"},
             "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"),
            ("Lightweight Breathable Running Shoes", "StridePro", 1799, 2999, 45, 4.4, 530, True,
             "Engineered flyknit mesh upper keeps feet cool. High-rebound EVA cushioned midsole for superior shock absorption.",
             {"Upper": "Engineered Knit Mesh", "Sole": "Anti-Slip Textured EVA + Rubber", "Closure": "Lace-Up", "Weight": "240g per shoe"},
             "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"),
            ("Canvas Weekender Travel Duffle Bag 40L", "Voyageur", 1899, 2999, 28, 4.6, 210, False,
             "Rugged heavy-duty washed cotton canvas with genuine leather trim, shoe compartment, and padded shoulder strap.",
             {"Capacity": "40 Litres", "Material": "16oz Heavy Cotton Canvas + Leather", "Dimensions": "52 x 28 x 26 cm", "Compartments": "Separate Shoe Pocket"},
             "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800"),
            ("Merino Blend Crewneck Knit Sweater", "NordicKnit", 1699, 2799, 32, 4.3, 160, False,
             "Super-soft thermal knit sweater offering lightweight warmth without itchiness. Ribbed cuffs and hem retain shape.",
             {"Composition": "50% Merino Wool, 50% Acrylic", "Neck": "Classic Crew Neck", "Care": "Hand Wash or Gentle Machine Cycle", "Fit": "Regular"},
             "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800"),
            ("Vintage Washed Denim Trucker Jacket", "IndigoRaw", 2199, 3499, 22, 4.5, 190, False,
             "Heavy 13oz cotton denim with authentic contrast stitching, shank buttons, and dual chest button-flap pockets.",
             {"Fabric": "100% Ring-Spun Cotton Denim (13oz)", "Wash": "Vintage Indigo Medium Wash", "Hardware": "Brass Shank Buttons", "Pockets": "4 Exterior"},
             "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=800"),
            ("Everyday Cotton Casual Chino Shorts", "BreezeFit", 799, 1399, 50, 4.2, 310, False,
             "Relaxed comfort stretch shorts with elasticated drawstring waistband, deep side pockets, and breathable weave.",
             {"Material": "97% Cotton, 3% Spandex", "Length": "Above Knee (9 inch inseam)", "Waist": "Elastic Waist with Drawcord", "Colors": "Khaki, Olive, Navy"},
             "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=800"),
            ("Pack of 3 Combed Cotton Crew T-Shirts", "BasicClub", 899, 1499, 75, 4.4, 640, False,
             "Premium bio-washed combed cotton tees that retain color and softness wash after wash. Tagless collar prevents itching.",
             {"Pack Contents": "3 T-Shirts (Black, White, Navy)", "Fabric": "180 GSM 100% Combed Cotton", "Neck": "Ribbed Crew Neck", "Pre-shrunk": "Yes"},
             "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800"),
            ("Brushed Fleece Pullover Hoodie", "CozyLayer", 1399, 2299, 38, 4.5, 410, False,
             "Plush 320 GSM cotton fleece with spacious kangaroo pocket, double-layered hood, and metal eyelet drawstrings.",
             {"Fabric": "80% Cotton, 20% Polyester (320 GSM)", "Pocket": "Kangaroo Front Pocket", "Cuffs": "Spandex Ribbed Cuffs", "Fit": "Comfort Oversized"},
             "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800"),
        ]
    },
    {
        "name": "Home and Kitchen",
        "slug": "home-and-kitchen",
        "color": "#f59e0b",
        "icon": "🍳",
        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800",
        "products": [
            ("Digital Air Fryer 5.5L Rapid Air 1400W", "CrispChef", 4499, 7499, 25, 4.6, 520, True,
             "Cook with up to 90% less oil. 8 one-touch preset cooking modes, dishwasher-safe non-stick basket, and auto shut-off timer.",
             {"Capacity": "5.5 Litres", "Power": "1400W", "Temperature": "80C - 200C", "Timer": "60 Minutes with Auto Pause", "Presets": "Fries, Chicken, Fish, Cake, etc."},
             "https://images.unsplash.com/photo-1585515320310-259814833e62?w=800"),
            ("15-Bar Espresso & Cappuccino Coffee Machine", "BaristaPro", 8999, 13999, 14, 4.5, 230, True,
             "Italian 15-bar pump extracts rich crema. Swiveling stainless steel steam wand produces silky micro-foam for lattes.",
             {"Pump Pressure": "15 Bar Italian ULKA Pump", "Water Tank": "1.5L Removable", "Boiler": "Die-cast Aluminum Alloy", "Includes": "Single & Double Shot Filters"},
             "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800"),
            ("3-Piece Granite Non-Stick Cookware Set", "KitchenStone", 2499, 4199, 35, 4.4, 410, False,
             "PFOA-free 5-layer granite coating. Set includes 24cm Frying Pan, 24cm Kadhai with Glass Lid, and 28cm Dosa Tawa.",
             {"Coating": "5-Layer German Greblon Granite", "Base": "Induction & Gas Compatible", "Handles": "Stay-Cool Bakelite", "Warranty": "2 Years"},
             "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=800"),
            ("Robotic Vacuum Cleaner & Mop with Gyro Navigation", "RoboClean", 14999, 21999, 10, 4.3, 115, True,
             "2500Pa strong suction, smart 2-in-1 sweeping and water mopping, auto-recharge dock, and smartphone app control.",
             {"Suction": "2500 Pascals", "Battery": "3200mAh (Up to 110 min runtime)", "Dustbin/Water Tank": "450ml / 250ml", "Cliff Sensors": "Anti-Drop & Anti-Collision"},
             "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800"),
            ("Stainless Steel Double-Walled Electric Kettle 1.8L", "BoilFast", 899, 1499, 60, 4.5, 890, False,
             "Cool-touch outer body protects against burns. 1500W rapid boil element, auto shut-off, and boil-dry protection.",
             {"Capacity": "1.8 Litres", "Power": "1500 Watts", "Interior": "Food-grade 304 Stainless Steel", "Safety": "Auto-cutoff on boiling"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
            ("14-Piece Stainless Steel Knife Block Set", "ChefEdge", 2999, 4999, 20, 4.7, 340, False,
             "High-carbon German stainless steel forged blades with full tang ergonomic handles and solid pine wood block.",
             {"Steel": "German 1.4116 High Carbon Stainless", "Pieces": "Chef, Bread, Santoku, Utility, Paring, 6x Steak, Honing Steel, Shears, Block", "Hardness": "HRC 56±2"},
             "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800"),
            ("Ultrasonic Cool Mist Humidifier with Aroma Diffuser 4L", "AeroMist", 2199, 3299, 30, 4.4, 180, False,
             "Whisper-quiet operation (<28dB) relieves dry cough, allergies, and dry skin. Essential oil tray for aromatherapy.",
             {"Tank Capacity": "4.0 Litres", "Run Time": "Up to 30 Hours Continuous", "Noise Level": "< 28 dB", "Nozzle": "360-degree Rotatable"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
            ("16-Piece Ceramic Matte Dinnerware Set for 4", "ArtisanClay", 3499, 5499, 18, 4.6, 145, False,
             "Modern Scandinavian matte reactive glaze ceramic. Set contains dinner plates, salad plates, cereal bowls, and mugs.",
             {"Material": "Lead-Free Stoneware Ceramic", "Service For": "4 Persons (16 Pieces Total)", "Safe For": "Microwave & Dishwasher Safe", "Finish": "Matte Slate Grey"},
             "https://images.unsplash.com/photo-1614088685112-0a760b71a3c8?w=800"),
            ("High-Speed Nutri-Blender & Smoothie Maker 1000W", "BlendPulse", 2799, 4299, 40, 4.5, 490, True,
             "Crushes ice, frozen fruits, nuts, and leafy greens in seconds with 6-leaf surgical stainless steel extraction blades.",
             {"Motor": "1000W Pure Copper High Torque", "Speed": "22,000 RPM", "Jars Included": "700ml Tall Cup + 500ml Travel Cup with Sipper Lid", "BPA Free": "Yes (Tritan)"},
             "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=800"),
            ("Contoured Cervical Memory Foam Bed Pillow", "SleepOrthic", 1299, 1999, 50, 4.3, 370, False,
             "Slow-rebound high-density memory foam supports spine and relieves neck tension for back and side sleepers.",
             {"Core": "100% Slow Rebound Memory Foam", "Cover": "Breathable Tencel Fabric (Removable & Washable)", "Dimensions": "60 x 38 x 11/9 cm"},
             "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800"),
            ("Revolving 16-Jar Countertop Spice Rack Tower", "SpiceCraft", 899, 1499, 45, 4.4, 280, False,
             "Smooth 360-degree rotating stainless steel tower keeps herbs and spices organized and accessible while cooking.",
             {"Jars": "16 Glass Jars with Dual Shaker Tops", "Stand": "Stainless Steel Revolving Carousel", "Capacity": "100ml per jar"},
             "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=800"),
            ("Automatic Touchless Liquid Soap Dispenser 350ml", "PureHand", 699, 1199, 70, 4.2, 410, False,
             "Accurate infrared sensor dispenses soap in 0.25 seconds. Waterproof battery compartment and adjustable dosage.",
             {"Sensor Range": "0 - 5 cm", "Capacity": "350 ml", "Power": "4x AAA Batteries", "Waterproof": "IPX4"},
             "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800"),
            ("Enameled Cast Iron Dutch Oven Pot with Lid 4.5L", "HeritageCook", 3999, 6499, 15, 4.8, 160, True,
             "Heavy-duty cast iron provides unmatched heat retention and distribution. Perfect for sourdough bread, stews, and braising.",
             {"Capacity": "4.5 Litres", "Material": "Enameled Cast Iron", "Oven Safe": "Up to 260C (500F)", "Color": "Cherry Red"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
        ]
    },
    {
        "name": "Books",
        "slug": "books",
        "color": "#10b981",
        "icon": "📚",
        "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800",
        "products": [
            ("The Pragmatic Programmer: 20th Anniversary Edition", "David Thomas & Andrew Hunt", 899, 1299, 40, 4.8, 620, True,
             "One of the most significant books in software development. Filled with classic and modern insights on craftsmanship.",
             {"Format": "Paperback", "Pages": "352", "Publisher": "Addison-Wesley", "Language": "English", "ISBN": "978-0135957059"},
             "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800"),
            ("Designing Data-Intensive Applications", "Martin Kleppmann", 1499, 2199, 30, 4.9, 950, True,
             "The definitive architectural guide to data storage, replication, partitioning, consistency, and distributed streaming systems.",
             {"Format": "Paperback", "Pages": "616", "Publisher": "O'Reilly Media", "Language": "English", "ISBN": "978-1449373320"},
             "https://images.unsplash.com/photo-1532012164546-f432f2e37b73?w=800"),
            ("Atomic Habits: Proven Way to Build Good Habits", "James Clear", 499, 799, 90, 4.8, 2400, True,
             "An easy and proven way to build good habits and break bad ones using small changes that deliver remarkable results.",
             {"Format": "Hardcover", "Pages": "320", "Publisher": "Random House Business", "Language": "English", "ISBN": "978-1847941831"},
             "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800"),
            ("Clean Code: A Handbook of Agile Software Craftsmanship", "Robert C. Martin", 999, 1499, 35, 4.7, 810, False,
             "Legendary software expert Uncle Bob presents a revolutionary paradigm on how to write robust, readable, clean code.",
             {"Format": "Paperback", "Pages": "464", "Publisher": "Pearson Education", "Language": "English", "ISBN": "978-0132350884"},
             "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800"),
            ("The Psychology of Money: Timeless Lessons on Wealth", "Morgan Housel", 399, 599, 85, 4.7, 1800, True,
             "Doing well with money isn't necessarily about what you know. It's about how you behave. 19 short engaging stories.",
             {"Format": "Paperback", "Pages": "256", "Publisher": "Jaico Publishing House", "Language": "English", "ISBN": "978-9390166268"},
             "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800"),
            ("Deep Work: Rules for Focused Success in a Distracted World", "Cal Newport", 449, 699, 45, 4.6, 920, False,
             "Master hard things and produce work of true value by developing superhuman concentration in an age of constant notification.",
             {"Format": "Paperback", "Pages": "304", "Publisher": "Piatkus", "Language": "English", "ISBN": "978-0349411903"},
             "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800"),
            ("Sapiens: A Brief History of Humankind", "Yuval Noah Harari", 599, 899, 60, 4.7, 1650, False,
             "Explore how an insignificant ape became the master of planet Earth in this international phenomenon and thought-provoking classic.",
             {"Format": "Paperback", "Pages": "512", "Publisher": "Vintage", "Language": "English", "ISBN": "978-0099590088"},
             "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800"),
            ("Python Crash Course, 3rd Edition: A Hands-On Guide", "Eric Matthes", 1299, 1899, 25, 4.8, 430, True,
             "World's bestselling guide to the Python programming language. Build interactive games, data visualizations, and web apps.",
             {"Format": "Paperback", "Pages": "552", "Publisher": "No Starch Press", "Language": "English", "ISBN": "978-1718502703"},
             "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800"),
            ("The Lean Startup: Innovation Creates Radically Successful Businesses", "Eric Ries", 549, 799, 40, 4.5, 780, False,
             "Most startups fail. But many of those failures are preventable. Learn rapid scientific iteration and validated learning.",
             {"Format": "Paperback", "Pages": "336", "Publisher": "Crown Business", "Language": "English", "ISBN": "978-0307887894"},
             "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800"),
            ("Thinking, Fast and Slow", "Daniel Kahneman", 499, 799, 50, 4.6, 1200, False,
             "Nobel laureate Kahneman takes us on an intellectual journey exploring the two systems that drive the way we think and decide.",
             {"Format": "Paperback", "Pages": "512", "Publisher": "Penguin Books", "Language": "English", "ISBN": "978-0141033570"},
             "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800"),
            ("System Design Interview – An Insider's Guide", "Alex Xu", 1699, 2499, 20, 4.8, 590, True,
             "Invaluable resource to prepare for system design rounds. Step-by-step walkthroughs of chat, video streaming, rate limiters.",
             {"Format": "Paperback", "Pages": "322", "Publisher": "Independently Published", "Language": "English", "ISBN": "979-8664653403"},
             "https://images.unsplash.com/photo-1532012164546-f432f2e37b73?w=800"),
            ("Zero to One: Notes on Startups, or How to Build the Future", "Peter Thiel", 449, 699, 55, 4.5, 990, False,
             "The great secret of our time is that there are still uncharted frontiers to explore and new inventions to create.",
             {"Format": "Hardcover", "Pages": "224", "Publisher": "Crown Currency", "Language": "English", "ISBN": "978-0804139298"},
             "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800"),
            ("Premium Hardcover Dotted Journal Notebook [A5]", "PaperNest", 399, 599, 100, 4.7, 850, False,
             "160 pages of thick 120 GSM bleed-proof ivory paper with ribbon bookmarks, expandable back pocket, and elastic closure band.",
             {"Cover": "Vegan Leather Hardcover", "Paper Weight": "120 GSM Acid-Free", "Ruling": "5mm Dot Grid", "Size": "A5 (14.8 x 21 cm)"},
             "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=800"),
        ]
    },
    {
        "name": "Sports",
        "slug": "sports",
        "color": "#14b8a6",
        "icon": "⚽",
        "image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800",
        "products": [
            ("High-Density Eco-TPE Yoga Mat with Alignment Lines (6mm)", "ZenMove", 899, 1499, 45, 4.6, 610, True,
             "Double-sided non-slip textured surfaces provide optimal cushioning for joints. Laser-engraved alignment guides maintain posture.",
             {"Material": "Eco-friendly TPE (No PVC, No Latex)", "Thickness": "6 mm Extra Thick", "Dimensions": "183 x 61 cm", "Includes": "Carrying Strap"},
             "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800"),
            ("Adjustable Cast Iron Dumbbell Set 20kg with Connector", "IronGrip", 3499, 5299, 20, 4.7, 430, True,
             "Converts dumbbells into a barbell within seconds using foam-padded connector rod. Includes chrome plates and spinlock collars.",
             {"Total Weight": "20 kg (44 lbs)", "Plates Included": "4x 2.5kg, 4x 1.25kg, 4x 0.5kg", "Bars": "2x Dumbbell Handles + 1x Barbell Joiner", "Material": "Electroplated Cast Iron"},
             "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800"),
            ("Resistance Bands Loop Exercise Set [5 Levels]", "FlexBand", 499, 899, 80, 4.4, 780, False,
             "100% natural Malaysian latex workout bands ranging from X-Light (5 lbs) to X-Heavy (40 lbs). Includes travel mesh bag.",
             {"Material": "100% Natural Latex", "Resistance": "5 - 40 lbs per band", "Quantity": "5 Bands + Travel Bag", "Ideal For": "Squats, Glutes, Stretching, Rehab"},
             "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=800"),
            ("Insulated Stainless Steel Sports Bottle 1000ml", "HydroVessel", 799, 1299, 60, 4.7, 920, True,
             "Double-wall vacuum insulation keeps drinks cold for 24 hours or steaming hot for 12 hours. Sweat-free powder coat exterior.",
             {"Capacity": "1000 ml (32 oz)", "Insulation": "Vacuum Double Wall 18/8 Steel", "Lids": "Straw Lid + Chug Sports Lid", "BPA Free": "100%"},
             "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=800"),
            ("Pro Ball-Bearing Speed Jump Rope for Cardio", "AeroSkip", 399, 699, 90, 4.5, 540, False,
             "360-degree dual ball bearings ensure smooth, tangle-free, lightning-fast rotations for CrossFit, double unders, and boxing.",
             {"Cable": "Steel Wire with PVC Sheath (3m Adjustable)", "Handles": "Aluminum Alloy with Anti-Slip Texture", "Bearings": "Dual Precision Steel", "Weight": "170g"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
            ("Deep Tissue Percussion Muscle Massage Gun", "ReliefPro", 2999, 4999, 25, 4.5, 310, True,
             "High-torque brushless motor delivers 30 speed levels up to 3200 RPM to relieve sore muscles and accelerate post-workout recovery.",
             {"Speeds": "30 Speed Levels (1200 - 3200 RPM)", "Heads": "6 Interchangeable Massage Heads", "Battery": "2500mAh (Up to 6 Hours)", "Noise": "QuietGlide Tech (<45dB)"},
             "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800"),
            ("Instant Pop-Up Waterproof Camping Tent (4-Person)", "CampTrail", 4499, 6999, 15, 4.4, 130, False,
             "Hydraulic automatic pop-up frame sets up in under 60 seconds. PU 3000mm waterproof coating with mesh ventilation windows.",
             {"Capacity": "3 - 4 Adults", "Dimensions": "210 x 210 x 140 cm", "Fabric": "210D Oxford Cloth PU 3000mm", "Weight": "3.8 kg"},
             "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800"),
            ("Trail Running Hydration Backpack with 2L Bladder", "HydroRunner", 1899, 2999, 30, 4.6, 210, False,
             "Ergonomic lightweight running vest with breathable back panel, reflective safety strips, and leak-proof 2L water bladder.",
             {"Bladder Capacity": "2 Litres (TPU Food Grade)", "Vest Weight": "280g Ultra-Light", "Storage": "Phone Pocket + Key Clip + Snack Pouches", "Chest Straps": "Adjustable Dual"},
             "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800"),
            ("Pro Synthetic Leather Boxing Gloves 12oz", "KnockOut", 1499, 2299, 35, 4.5, 360, False,
             "Triple-density foam padding dissipates shock impact on knuckles and wrists. Breathable palm mesh keeps hands cool.",
             {"Size/Weight": "12 oz", "Material": "Premium Engineered PU Leather", "Wrist Closure": "Full Hook & Loop Strap", "Thumb Lock": "Yes (Prevents Sprains)"},
             "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=800"),
            ("Full Carbon Fiber Badminton Racket Twin Pack", "SmashCourt", 1999, 3299, 28, 4.6, 420, True,
             "Lightweight 4U (82g) full graphite frame pre-strung at 24 lbs. Package includes 2 rackets, 3 nylon shuttlecocks, and full cover.",
             {"Material": "High Modulus Graphite", "Weight": "4U (82g - 84g)", "Tension": "Pre-strung at 24 lbs (Supports up to 28 lbs)", "Balance": "Even Balance"},
             "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=800"),
            ("Official Match FIFA-Standard Football Size 5", "StrikerPro", 799, 1299, 50, 4.4, 490, False,
             "Thermal bonded 32-panel seamless construction ensures true flight trajectory, zero water absorption, and high shape retention.",
             {"Size": "Size 5 (Official Adult)", "Construction": "Thermal Bonded Seamless", "Bladder": "Reinforced Butyl Rubber Bladder", "Surface": "Textured Polyurethane"},
             "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800"),
            ("Compression Knee Brace Sleeves [Pair]", "JointGuard", 699, 1199, 70, 4.5, 680, False,
             "3D circular knitting technology delivers targeted compression to stabilize patella and ligaments during squats and running.",
             {"Material": "68% Polyamide, 32% Spandex", "Features": "Double Silicone Anti-Slip Gel Strips", "Quantity": "2 Knee Sleeves", "Support Level": "Moderate Medical Grade"},
             "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800"),
            ("Polarized Sports Cycling & Running Sunglasses", "VeloSpeed", 899, 1499, 40, 4.4, 250, False,
             "Wide wraparound panoramic UV400 shield protects eyes from wind, dust, and glare. Lightweight TR90 flexible frame.",
             {"Frame": "TR90 Memory Polymer", "Lenses": "Polarized HD Polycarbonate", "UV Protection": "UV400", "Includes": "Myopia Inner Frame + Hard Case"},
             "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800"),
        ]
    },
    {
        "name": "Beauty",
        "slug": "beauty",
        "color": "#a855f7",
        "icon": "✨",
        "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800",
        "products": [
            ("Hydrating Hyaluronic Acid Serum 2% + B5 (30ml)", "DermaGlow", 599, 899, 55, 4.6, 940, True,
             "Multi-molecular weight hyaluronic acid penetrates deep skin layers to deliver intense plumping hydration and smooth fine lines.",
             {"Volume": "30 ml", "Key Actives": "2% Pure Hyaluronic Acid + Provitamin B5", "Skin Type": "All Skin Types (Dry, Oily, Sensitive)", "Cruelty-Free": "Yes"},
             "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800"),
            ("Vitamin C 15% Daily Brightening Face Wash (150ml)", "GlowLab", 399, 599, 70, 4.5, 780, False,
             "Gentle sulphate-free foaming gel cleanser infused with Kakadu plum extract and niacinamide to fade dark spots and even tone.",
             {"Volume": "150 ml", "Ingredients": "15% Vitamin C, Niacinamide, Aloe Vera", "Formula": "Sulphate & Paraben Free", "pH": "Balanced 5.5"},
             "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800"),
            ("Matte Finish Invisible Gel Sunscreen SPF 50+ PA++++", "SunArmor", 649, 999, 60, 4.7, 1120, True,
             "Ultra-lightweight transparent sunscreen leaves zero white cast and zero greasy residue. Water and sweat resistant for 80 minutes.",
             {"Sun Protection": "SPF 50+ PA++++ Broad Spectrum", "Finish": "Velvety Matte, Zero White Cast", "Volume": "50 g", "Water Resistance": "80 Minutes"},
             "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800"),
            ("Organic Cold-Pressed Moroccan Argan Hair Oil 100ml", "PureSilk", 799, 1299, 40, 4.6, 450, True,
             "100% pure virgin argan oil tames frizz, protects against heat styling damage, and restores brilliant natural shine.",
             {"Volume": "100 ml", "Purity": "100% Pure USDA Organic Cold-Pressed", "Free From": "Mineral Oil, Silicones, Artificial Fragrance", "Use": "Hair & Scalp Serum"},
             "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=800"),
            ("Authentic Rose Quartz Facial Roller & Gua Sha Set", "CrystalZen", 699, 1199, 45, 4.4, 380, False,
             "Hand-carved natural Brazilian rose quartz stimulates lymphatic drainage, depuffs eye bags, and promotes firm skin elasticity.",
             {"Stone": "100% Genuine Brazilian Rose Quartz", "Hardware": "Reinforced Zinc Alloy (No Squeak)", "Includes": "Dual Roller + Heart Gua Sha Tool + Gift Box"},
             "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800"),
            ("Refreshing Tea Tree & Peppermint Body Wash 300ml", "Botanica", 449, 699, 65, 4.3, 290, False,
             "Invigorating botanical shower gel deeply purifies pores, calms body blemishes, and leaves skin refreshed all day.",
             {"Volume": "300 ml", "Key Botanicals": "Australian Tea Tree Oil, Peppermint, Eucalyptus", "Soap-Free": "Yes", "Fragrance": "Natural Herbal"},
             "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=800"),
            ("Professional Ionic Fast-Drying Hair Dryer 2000W", "SalonPro", 2299, 3699, 25, 4.6, 310, True,
             "Negative ion generator reduces static frizz by 80%. 3 heat settings, 2 speed settings, and cold shot button for locking styles.",
             {"Power": "2000W AC Professional Motor", "Technology": "Tourmaline Ceramic + Negative Ions", "Attachments": "Concentrator Nozzle + Diffuser", "Cord": "2.5m Salon Swivel"},
             "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800"),
            ("AHA 25% + BHA 2% Exfoliating Peeling Solution (30ml)", "DermaClear", 549, 799, 50, 4.5, 620, False,
             "10-minute facial peel solution with glycolic, lactic, and salicylic acids to clear congested pores and reveal radiant smoothness.",
             {"Actives": "25% AHA (Glycolic + Lactic), 2% Salicylic Acid", "Volume": "30 ml", "Application": "10-minute wash-off peel once weekly", "Warning": "Use sunscreen after peel"},
             "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800"),
            ("Raw Shea Butter & Cocoa Intense Body Cream 200g", "VelvetSkin", 499, 799, 55, 4.7, 530, False,
             "Decadent rich moisturizer formulated with unrefined African shea butter, sweet almond oil, and vitamin E for 48-hour moisture.",
             {"Net Weight": "200 g", "Texture": "Rich Whipped Butter", "Key Ingredients": "Raw Shea Butter, Cocoa Butter, Sweet Almond Oil", "Skin Type": "Very Dry Skin"},
             "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800"),
            ("Lengthening & Volumizing Waterproof Mascara 10ml", "LashQueen", 399, 649, 75, 4.4, 490, False,
             "Hourglass silicone brush coats every lash without clumping or flaking. Smudge-proof 24-hour long wear formula.",
             {"Volume": "10 ml", "Color": "Carbon Black", "Waterproof": "Yes (Smudge-proof & Tear-proof)", "Ophthalmologist Tested": "Safe for Contact Lens Wearers"},
             "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800"),
            ("Bamboo Charcoal Pore Cleansing Detox Clay Mask", "PureDetox", 499, 799, 40, 4.5, 340, False,
             "Activated bamboo charcoal draws out stubborn blackheads, micro-pollutants, and excess sebum while kaolin clay refines pores.",
             {"Weight": "100 g", "Key Actives": "Activated Bamboo Charcoal, Kaolin Clay, Witch Hazel", "Free From": "Parabens, Sulphates, Phthalates", "Application Brush": "Included"},
             "https://images.unsplash.com/photo-1567928815116-24bc294c77ea?w=800"),
            ("Complete Beard Grooming & Growth Care Kit", "GentlemanBeard", 1199, 1899, 30, 4.7, 410, True,
             "Includes organic cedarwood beard oil (30ml), beard styling balm (50g), dual-sided wooden comb, and boar bristle brush.",
             {"Kit Contents": "Beard Oil, Beard Butter, Sandalwood Comb, Boar Bristle Brush, Stainless Scissors", "Scent": "Subtle Cedarwood & Bergamot", "Ingredients": "100% Organic Oils"},
             "https://images.unsplash.com/photo-1621607512214-68297480165e?w=800"),
            ("Natural Himalayan Pink Rock Bath Soaking Salts (500g)", "AromaSoak", 349, 549, 60, 4.5, 270, False,
             "100% pure mineral-rich Himalayan pink salt crystals infused with French lavender and chamomile essential oils to melt stress.",
             {"Net Weight": "500 g", "Origin": "Authentic Himalayan Rock Salt", "Infusion": "Lavender & Chamomile Essential Oils", "Benefits": "Relieves Muscle Cramps & Relaxes Mind"},
             "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800"),
        ]
    }
]

# Write SVG generator for high quality local product images
def generate_product_svg(name, category, brand, price, color):
    short_name = name[:30] + ("..." if len(name) > 30 else "")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f1f5f9"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{color}"/>
      <stop offset="100%" stop-color="{color}cc"/>
    </linearGradient>
  </defs>
  <rect width="500" height="500" fill="url(#bg)"/>
  <rect x="25" y="25" width="450" height="450" rx="24" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>
  
  <!-- Category banner badge -->
  <rect x="50" y="50" width="140" height="32" rx="16" fill="url(#accent)"/>
  <text x="120" y="71" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{category}</text>
  
  <!-- Brand text -->
  <text x="50" y="115" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="14" font-weight="700" fill="#64748b" letter-spacing="1">{brand.upper()}</text>
  
  <!-- Central Product Box Graphic -->
  <g transform="translate(150, 140)">
    <rect width="200" height="180" rx="16" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
    <circle cx="100" cy="80" r="42" fill="{color}22" stroke="{color}" stroke-width="2"/>
    <text x="100" y="90" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="32" text-anchor="middle">🛍️</text>
    <rect x="30" y="140" width="140" height="12" rx="6" fill="#e2e8f0"/>
  </g>
  
  <!-- Product Name -->
  <text x="250" y="370" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="18" font-weight="700" fill="#0f172a" text-anchor="middle">{short_name}</text>
  
  <!-- Price Tag -->
  <text x="250" y="410" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="22" font-weight="800" fill="#ea580c" text-anchor="middle">₹{price:,}</text>
  <text x="250" y="440" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif" font-size="12" font-weight="600" fill="#16a34a" text-anchor="middle">✓ ShopSphere Verified Prime</text>
</svg>"""
    return svg

def build_dataset():
    products_json_list = []
    image_manifest = {}
    sku_counter = 1
    total_products = 0

    for cat_data in CATEGORIES_DATA:
        cat_name = cat_data["name"]
        cat_slug = cat_data["slug"]
        cat_color = cat_data["color"]

        for prod in cat_data["products"]:
            name, brand, price, orig_price, stock, rating, reviews, featured, desc, specs, img_url = prod
            sku = f"SP-{cat_slug[:3].upper()}-{sku_counter:04d}"
            prod_slug = f"{sku.lower()}-{cat_slug}"
            local_svg_filename = f"{sku.lower()}.svg"
            local_svg_path = MEDIA_PRODUCTS / local_svg_filename

            # Write local image SVG
            with open(local_svg_path, "w", encoding="utf-8") as svg_file:
                svg_file.write(generate_product_svg(name, cat_name, brand, price, cat_color))

            local_image_rel = f"products/{local_svg_filename}"

            product_record = {
                "sku": sku,
                "name": name,
                "slug": prod_slug,
                "category": cat_name,
                "brand": brand,
                "price": price,
                "original_price": orig_price,
                "stock": stock,
                "rating": rating,
                "review_count": reviews,
                "is_featured": featured,
                "is_active": True,
                "description": desc,
                "specifications": specs,
                "image_url": img_url,
                "local_image": local_image_rel,
            }

            products_json_list.append(product_record)
            image_manifest[sku] = {
                "name": name,
                "category": cat_name,
                "local_image": local_image_rel,
                "remote_image": img_url,
                "fallback_placeholder": "/static/images/placeholder.svg"
            }

            sku_counter += 1
            total_products += 1

    # Save to catalog/fixtures/products.json
    with open(FIXTURES_DIR / "products.json", "w", encoding="utf-8") as f:
        json.dump(products_json_list, f, indent=2)

    # Save to catalog/fixtures/image_manifest.json
    with open(FIXTURES_DIR / "image_manifest.json", "w", encoding="utf-8") as f:
        json.dump(image_manifest, f, indent=2)

    print(f"Successfully generated {total_products} products across {len(CATEGORIES_DATA)} categories!")
    print(f"Generated products.json, image_manifest.json and {sku_counter - 1} SVG product images in media/products/")

if __name__ == "__main__":
    build_dataset()
