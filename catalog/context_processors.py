from .models import Category

def catalog_context(request):
    try:
        categories = Category.objects.filter(is_active=True).order_by("name")
    except Exception:
        categories = []
    return {"nav_categories": categories}
