import json
from decimal import Decimal
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from catalog.models import Category, Product, ProductImage, Review

User = get_user_model()

CATEGORY_META = {
    "Electronics": {"image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800"},
    "Computers": {"image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800"},
    "Mobile Phones": {"image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800"},
    "Fashion": {"image_url": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=800"},
    "Home and Kitchen": {"image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800"},
    "Books": {"image_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=800"},
    "Sports": {"image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800"},
    "Beauty": {"image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800"},
}

SAMPLE_REVIEWS = [
    ("Exceptional build quality!", 5, "I have been using this for over a month now. Build quality is top-notch and delivery was super fast. Highly recommended!"),
    ("Great value for money", 4, "Definitely punches above its price bracket. Packaging was intact and works exactly as advertised."),
    ("Worth every rupee", 5, "Exceeded my expectations. Clean finish, solid feel, and works reliably every single day."),
    ("Good product, quick delivery", 4, "Delivered within 24 hours. The packaging was neat and the item performs well."),
]

class Command(BaseCommand):
    help = "Idempotently import categories, products, and sample reviews from products.json fixture."

    def handle(self, *args, **options):
        fixture_path = Path(__file__).resolve().parent.parent.parent / "fixtures" / "products.json"
        if not fixture_path.exists():
            self.stderr.write(self.style.ERROR(f"Fixture file not found at {fixture_path}"))
            return

        with open(fixture_path, "r", encoding="utf-8") as f:
            products_data = json.load(f)

        # 1. Create or update Categories
        category_cache = {}
        for cat_name, meta in CATEGORY_META.items():
            slug = slugify(cat_name)
            cat_obj, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": cat_name,
                    "image_url": meta.get("image_url", ""),
                    "is_active": True,
                }
            )
            category_cache[cat_name] = cat_obj

        # 2. Ensure a reviewer user exists for sample reviews
        reviewer, _ = User.objects.get_or_create(
            username="verified_buyer",
            defaults={"email": "buyer@shopsphere.in", "first_name": "Arjun"}
        )
        if _:
            reviewer.set_password("buyerpass123")
            reviewer.save()

        # 3. Create or update Products
        seeded_count = 0
        for item in products_data:
            cat_name = item["category"]
            cat_obj = category_cache.get(cat_name)
            if not cat_obj:
                cat_slug = slugify(cat_name)
                cat_obj, _ = Category.objects.update_or_create(slug=cat_slug, defaults={"name": cat_name})
                category_cache[cat_name] = cat_obj

            sku = item["sku"]
            local_img = item.get("local_image", "")

            product, created = Product.objects.update_or_create(
                sku=sku,
                defaults={
                    "category": cat_obj,
                    "name": item["name"],
                    "slug": item.get("slug") or f"{slugify(item['name'])}-{sku.lower()}",
                    "brand": item.get("brand", "ShopSphere Select"),
                    "description": item.get("description", ""),
                    "specifications": item.get("specifications", {}),
                    "price": Decimal(str(item["price"])),
                    "original_price": Decimal(str(item["original_price"])),
                    "stock": int(item.get("stock", 20)),
                    "image": local_img if local_img else None,
                    "image_url": item.get("image_url", ""),
                    "rating": Decimal(str(item.get("rating", "4.5"))),
                    "review_count": int(item.get("review_count", 50)),
                    "is_featured": bool(item.get("is_featured", False)),
                    "is_active": bool(item.get("is_active", True)),
                }
            )

            # Ensure primary ProductImage entry exists
            ProductImage.objects.get_or_create(
                product=product,
                display_order=1,
                defaults={
                    "image": local_img if local_img else None,
                    "image_url": item.get("image_url", ""),
                    "alt_text": product.name,
                }
            )

            # Seed a sample review for featured products if not present
            if product.is_featured and not product.reviews.exists():
                r_title, r_rating, r_comment = SAMPLE_REVIEWS[seeded_count % len(SAMPLE_REVIEWS)]
                Review.objects.get_or_create(
                    product=product,
                    user=reviewer,
                    defaults={
                        "title": r_title,
                        "rating": r_rating,
                        "comment": r_comment,
                    }
                )

            seeded_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {seeded_count} products across {len(category_cache)} categories without duplicates."
            )
        )
