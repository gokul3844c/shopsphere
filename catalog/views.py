from decimal import Decimal
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Review
from .forms import ReviewForm

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    todays_deals = Product.objects.filter(is_active=True).order_by("-price")[:8]
    categories = Category.objects.filter(is_active=True).order_by("name")

    # Category shelf highlights
    electronics = Product.objects.filter(is_active=True, category__slug="electronics")[:4]
    fashion = Product.objects.filter(is_active=True, category__slug="fashion")[:4]
    books = Product.objects.filter(is_active=True, category__slug="books")[:4]
    sports = Product.objects.filter(is_active=True, category__slug="sports")[:4]

    return render(request, "catalog/home.html", {
        "featured_products": featured_products,
        "todays_deals": todays_deals,
        "categories": categories,
        "electronics": electronics,
        "fashion": fashion,
        "books": books,
        "sports": sports,
    })

def product_list(request):
    if not request.user.is_authenticated:
        return redirect("login")

    products = Product.objects.filter(is_active=True).select_related("category")
    categories = Category.objects.filter(is_active=True).order_by("name")

    q = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    min_rating = request.GET.get("rating", "").strip()
    in_stock_only = request.GET.get("in_stock", "").strip()
    sort = request.GET.get("sort", "featured").strip()

    # Text Search across name, brand, description, category
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(brand__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q)
        )

    # Category Filter
    selected_category = None
    if category_slug:
        if category_slug.isdigit():
            products = products.filter(category_id=int(category_slug))
            selected_category = categories.filter(id=int(category_slug)).first()
        else:
            products = products.filter(category__slug=category_slug)
            selected_category = categories.filter(slug=category_slug).first()

    # Price Filter
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except Exception:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except Exception:
            pass

    # Rating Filter
    if min_rating:
        try:
            products = products.filter(rating__gte=Decimal(min_rating))
        except Exception:
            pass

    # In Stock Filter
    if in_stock_only in ["1", "true", "on"]:
        products = products.filter(stock__gt=0)

    # Sorting
    if sort == "price_low":
        products = products.order_by("price")
    elif sort == "price_high":
        products = products.order_by("-price")
    elif sort == "rating":
        products = products.order_by("-rating", "-review_count")
    elif sort == "newest":
        products = products.order_by("-created_at")
    else:
        # Default featured
        products = products.order_by("-is_featured", "-rating", "-created_at")

    total_results = products.count()

    # Pagination: 16 products per page
    paginator = Paginator(products, 16)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "catalog/product_list.html", {
        "products": page_obj,
        "page_obj": page_obj,
        "total_results": total_results,
        "categories": categories,
        "selected_category": selected_category,
        "q": q,
        "category_slug": category_slug,
        "min_price": min_price,
        "max_price": max_price,
        "min_rating": min_rating,
        "in_stock_only": in_stock_only,
        "sort": sort,
    })

def product_detail(request, slug):
    if not request.user.is_authenticated:
        return redirect("login")

    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    reviews = product.reviews.select_related("user").order_by("-created_at")
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    review_form = ReviewForm()

    if request.method == "POST" and "submit_review" in request.POST:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review, created = Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    "rating": review_form.cleaned_data["rating"],
                    "title": review_form.cleaned_data["title"],
                    "comment": review_form.cleaned_data["comment"],
                }
            )
            product.update_rating()
            messages.success(request, "Your review has been submitted. Thank you!")
            return redirect(product.get_absolute_url())

    return render(request, "catalog/product_detail.html", {
        "product": product,
        "images": images,
        "reviews": reviews,
        "user_review": user_review,
        "review_form": review_form,
        "related": related,
    })

def search_suggestions(request):
    q = request.GET.get("q", "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})

    matches = Product.objects.filter(
        is_active=True
    ).filter(
        Q(name__icontains=q) | Q(brand__icontains=q)
    )[:6]

    results = []
    for p in matches:
        results.append({
            "name": p.name,
            "brand": p.brand,
            "price": f"₹{p.price:,.2f}",
            "url": p.get_absolute_url(),
            "category": p.category.name,
            "image": p.display_image
        })

    return JsonResponse({"results": results})
