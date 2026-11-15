"""
Management command: fix_product_images
Clears the local SVG image field and assigns curated, realistic Unsplash
image URLs to every product and ProductImage entry so the storefront shows
real product photography.
"""
from django.core.management.base import BaseCommand
from catalog.models import Product, ProductImage

# ---------------------------------------------------------------------------
# Curated Unsplash image map keyed by product SKU prefix / name keywords.
# Every URL uses ?w=800&q=85&auto=format for consistent sizing and quality.
# ---------------------------------------------------------------------------

SKU_IMAGE_MAP = {
    # ── Electronics ────────────────────────────────────────────────────────
    "SP-ELE-0001": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=85&auto=format",  # headphones
    "SP-ELE-0002": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&q=85&auto=format",  # soundbar
    "SP-ELE-0003": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=800&q=85&auto=format",  # streaming box
    "SP-ELE-0004": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=85&auto=format",  # earbuds
    "SP-ELE-0005": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=800&q=85&auto=format",  # security camera
    "SP-ELE-0006": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=85&auto=format",  # bluetooth speaker
    "SP-ELE-0007": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&q=85&auto=format",  # action camera
    "SP-ELE-0008": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=85&auto=format",  # desk lamp
    "SP-ELE-0009": "https://images.unsplash.com/photo-1609592426868-45e054527787?w=800&q=85&auto=format",  # power bank
    "SP-ELE-0010": "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=800&q=85&auto=format",  # drone
    "SP-ELE-0011": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800&q=85&auto=format",  # smart plug
    "SP-ELE-0012": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&q=85&auto=format",  # microphone
    "SP-ELE-0013": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&q=85&auto=format",  # alarm clock

    # ── Computers ───────────────────────────────────────────────────────────
    "SP-COM-0014": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=85&auto=format",  # laptop
    "SP-COM-0015": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=85&auto=format",  # monitor
    "SP-COM-0016": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800&q=85&auto=format",  # SSD
    "SP-COM-0017": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=800&q=85&auto=format",  # mouse
    "SP-COM-0018": "https://images.unsplash.com/photo-1544652478-6653e09f18a2?w=800&q=85&auto=format",  # USB hub
    "SP-COM-0019": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=85&auto=format",  # webcam
    "SP-COM-0020": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=85&auto=format",  # keyboard
    "SP-COM-0021": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=800&q=85&auto=format",  # router
    "SP-COM-0022": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&q=85&auto=format",  # laptop stand
    "SP-COM-0023": "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=800&q=85&auto=format",  # drawing tablet
    "SP-COM-0024": "https://images.unsplash.com/photo-1595053826286-2e59ef79ff18?w=800&q=85&auto=format",  # cable mgmt
    "SP-COM-0025": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=85&auto=format",  # gaming monitor
    "SP-COM-0026": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800&q=85&auto=format",  # laptop sleeve

    # ── Mobile Phones ───────────────────────────────────────────────────────
    "SP-MOB-0027": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=85&auto=format",
    "SP-MOB-0028": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=800&q=85&auto=format",
    "SP-MOB-0029": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800&q=85&auto=format",
    "SP-MOB-0030": "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=800&q=85&auto=format",
    "SP-MOB-0031": "https://images.unsplash.com/photo-1586495777744-4e6232bf2b45?w=800&q=85&auto=format",
    "SP-MOB-0032": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&q=85&auto=format",
    "SP-MOB-0033": "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=800&q=85&auto=format",
    "SP-MOB-0034": "https://images.unsplash.com/photo-1512054502232-10a0a035d672?w=800&q=85&auto=format",
    "SP-MOB-0035": "https://images.unsplash.com/photo-1558756520-22cfe5d382ca?w=800&q=85&auto=format",
    "SP-MOB-0036": "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=800&q=85&auto=format",
    "SP-MOB-0037": "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=800&q=85&auto=format",
    "SP-MOB-0038": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=800&q=85&auto=format",
    "SP-MOB-0039": "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=800&q=85&auto=format",

    # ── Fashion ─────────────────────────────────────────────────────────────
    "SP-FAS-0040": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&q=85&auto=format",
    "SP-FAS-0041": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=85&auto=format",  # sneakers
    "SP-FAS-0042": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=85&auto=format",  # backpack
    "SP-FAS-0043": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=800&q=85&auto=format",  # jacket
    "SP-FAS-0044": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=85&auto=format",  # watch
    "SP-FAS-0045": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=800&q=85&auto=format",  # bag
    "SP-FAS-0046": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=800&q=85&auto=format",  # hoodie
    "SP-FAS-0047": "https://images.unsplash.com/photo-1559563458-527698bf5295?w=800&q=85&auto=format",  # sunglasses
    "SP-FAS-0048": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=800&q=85&auto=format",  # running shoes
    "SP-FAS-0049": "https://images.unsplash.com/photo-1521335629791-ce4aec67dd15?w=800&q=85&auto=format",  # belt
    "SP-FAS-0050": "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=800&q=85&auto=format",  # perfume
    "SP-FAS-0051": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&q=85&auto=format",  # sunglasses 2
    "SP-FAS-0052": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=800&q=85&auto=format",  # shoes

    # ── Home and Kitchen ────────────────────────────────────────────────────
    "SP-HOM-0053": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=85&auto=format",  # kitchen appliance
    "SP-HOM-0054": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&q=85&auto=format",  # coffee maker
    "SP-HOM-0055": "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800&q=85&auto=format",  # mixer
    "SP-HOM-0056": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=85&auto=format",  # cookware
    "SP-HOM-0057": "https://images.unsplash.com/photo-1556909172-54557c7e4fb7?w=800&q=85&auto=format",  # air fryer
    "SP-HOM-0058": "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=800&q=85&auto=format",  # vacuum
    "SP-HOM-0059": "https://images.unsplash.com/photo-1594735811673-dd9db7b44b30?w=800&q=85&auto=format",  # bedding
    "SP-HOM-0060": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800&q=85&auto=format",  # organizer
    "SP-HOM-0061": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&q=85&auto=format",  # kettle
    "SP-HOM-0062": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=85&auto=format",  # pots
    "SP-HOM-0063": "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800&q=85&auto=format",  # blender
    "SP-HOM-0064": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=85&auto=format",  # toaster
    "SP-HOM-0065": "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=800&q=85&auto=format",  # iron

    # ── Books ───────────────────────────────────────────────────────────────
    "SP-BOO-0066": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800&q=85&auto=format",
    "SP-BOO-0067": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800&q=85&auto=format",
    "SP-BOO-0068": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&q=85&auto=format",
    "SP-BOO-0069": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=800&q=85&auto=format",
    "SP-BOO-0070": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800&q=85&auto=format",
    "SP-BOO-0071": "https://images.unsplash.com/photo-1476275466078-4cad320172cf?w=800&q=85&auto=format",
    "SP-BOO-0072": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&q=85&auto=format",
    "SP-BOO-0073": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800&q=85&auto=format",
    "SP-BOO-0074": "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=800&q=85&auto=format",
    "SP-BOO-0075": "https://images.unsplash.com/photo-1472289065668-ce650ac443d2?w=800&q=85&auto=format",
    "SP-BOO-0076": "https://images.unsplash.com/photo-1455885661740-29cbf08a42fa?w=800&q=85&auto=format",
    "SP-BOO-0077": "https://images.unsplash.com/photo-1491841573634-28140fc7ced7?w=800&q=85&auto=format",
    "SP-BOO-0078": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800&q=85&auto=format",

    # ── Sports ──────────────────────────────────────────────────────────────
    "SP-SPO-0079": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&q=85&auto=format",
    "SP-SPO-0080": "https://images.unsplash.com/photo-1584735175315-9d5df23be4b1?w=800&q=85&auto=format",  # yoga mat
    "SP-SPO-0081": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&q=85&auto=format",  # dumbbell
    "SP-SPO-0082": "https://images.unsplash.com/photo-1607962837359-5e7e89f86776?w=800&q=85&auto=format",  # resistance bands
    "SP-SPO-0083": "https://images.unsplash.com/photo-1591291621164-2c6367723315?w=800&q=85&auto=format",  # football
    "SP-SPO-0084": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&q=85&auto=format",  # fitness tracker
    "SP-SPO-0085": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&q=85&auto=format",  # bicycle helmet
    "SP-SPO-0086": "https://images.unsplash.com/photo-1535914254981-b5012eebbd15?w=800&q=85&auto=format",  # water bottle
    "SP-SPO-0087": "https://images.unsplash.com/photo-1562771379-eafdca7a02f8?w=800&q=85&auto=format",  # jump rope
    "SP-SPO-0088": "https://images.unsplash.com/photo-1576678927484-cc907957088c?w=800&q=85&auto=format",  # boxing gloves
    "SP-SPO-0089": "https://images.unsplash.com/photo-1593079831268-3381b0db4a77?w=800&q=85&auto=format",  # badminton
    "SP-SPO-0090": "https://images.unsplash.com/photo-1533560904424-a0c61dc306fc?w=800&q=85&auto=format",  # cricket bat
    "SP-SPO-0091": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=800&q=85&auto=format",  # gym bag

    # ── Beauty ──────────────────────────────────────────────────────────────
    "SP-BEA-0092": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800&q=85&auto=format",
    "SP-BEA-0093": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&q=85&auto=format",  # skincare
    "SP-BEA-0094": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800&q=85&auto=format",  # face cream
    "SP-BEA-0095": "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=800&q=85&auto=format",  # serum
    "SP-BEA-0096": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&q=85&auto=format",  # lipstick
    "SP-BEA-0097": "https://images.unsplash.com/photo-1631730486572-226d1f595058?w=800&q=85&auto=format",  # hair dryer
    "SP-BEA-0098": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&q=85&auto=format",  # makeup brush
    "SP-BEA-0099": "https://images.unsplash.com/photo-1567721913486-6585f069b3f4?w=800&q=85&auto=format",  # nail polish
    "SP-BEA-0100": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&q=85&auto=format",  # moisturizer
    "SP-BEA-0101": "https://images.unsplash.com/photo-1515688594390-b649af70d282?w=800&q=85&auto=format",  # perfume
    "SP-BEA-0102": "https://images.unsplash.com/photo-1573461169842-e37e1b88b3c3?w=800&q=85&auto=format",  # shampoo
    "SP-BEA-0103": "https://images.unsplash.com/photo-1621607512214-68297480165e?w=800&q=85&auto=format",  # sunscreen
    "SP-BEA-0104": "https://images.unsplash.com/photo-1612817288484-6f916006741a?w=800&q=85&auto=format",  # face wash
}

# Fallback images by category if SKU not found
CATEGORY_FALLBACKS = {
    "Electronics":      "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=85&auto=format",
    "Computers":        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=85&auto=format",
    "Mobile Phones":    "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=85&auto=format",
    "Fashion":          "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800&q=85&auto=format",
    "Home and Kitchen": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=85&auto=format",
    "Books":            "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800&q=85&auto=format",
    "Sports":           "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&q=85&auto=format",
    "Beauty":           "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800&q=85&auto=format",
}


class Command(BaseCommand):
    help = "Replace SVG placeholder images with real Unsplash product photos."

    def handle(self, *args, **options):
        products = Product.objects.select_related("category").all()
        updated = 0

        for product in products:
            # Pick the best URL: SKU map > existing image_url > category fallback
            best_url = (
                SKU_IMAGE_MAP.get(product.sku)
                or (product.image_url.strip() if product.image_url else None)
                or CATEGORY_FALLBACKS.get(product.category.name, "")
            )

            changed = False

            # Clear the local SVG image field (it overrides image_url)
            if product.image:
                product.image = None
                changed = True

            # Update image_url to the best URL
            if best_url and product.image_url != best_url:
                product.image_url = best_url
                changed = True

            if changed:
                product.save(update_fields=["image", "image_url"])
                updated += 1

            # Fix ProductImage entries too
            for pi in product.images.all():
                pi_changed = False
                if pi.image:
                    pi.image = None
                    pi_changed = True
                if best_url and pi.image_url != best_url:
                    pi.image_url = best_url
                    pi_changed = True
                if pi_changed:
                    pi.save(update_fields=["image", "image_url"])

        self.stdout.write(
            self.style.SUCCESS(
                f"SUCCESS: Fixed images for {updated} products ({products.count()} total)."
            )
        )
