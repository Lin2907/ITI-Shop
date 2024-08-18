from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Review
from wishlist.models import Wishlist
from .forms import ProductForm ,ReviewForm


# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)
    similar_products = Product.objects.filter(tags__in=product.tags.all()).exclude(id=product.id).distinct()[:3] 
    # Default to None for unauthenticated users
    user_wishlist = None
    
    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user, products=product).exists()

    context = {
        'product': product,
        'reviews': reviews,
        'user_wishlist': user_wishlist,
        'similar_products': similar_products,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners are allowed to add products.')
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners are allowed to edit products.')
        return redirect(reverse('index'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

#Delete a product

@login_required
def delete_product(request, product_id):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners are allowed to delete products.')
        return redirect(reverse('index'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

#Review views

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            try:
                review = review_form.save(commit=False)
                review.product = product
                review.author_name = request.user.username
                review.author_email = request.user.email
                review.save()
                messages.success(request, "Your review has been successfully added!")
                return redirect(reverse("product_detail", args=[product.id]))
            except IntegrityError:
                messages.error(request, "You have already reviewed this product.")
                return redirect(reverse("product_detail", args=[product.id]))
    
    # If the request method is not POST, or the form is not valid, redirect to the product detail page
    return render(request, 'products/add_review.html', {'product': product, 'form': ReviewForm()})

# Editing and deleting reviews

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # The user must be the author of the review to be able to edit it
    if review.author_email != request.user.email:
        messages.error(request, 'You are not authorized to edit this review.')
        return redirect('product_detail', product_id=review.product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect(reverse('product_detail', args=[review.product.id]))
        else:
            messages.error(request, 'Failed to update the review. Please ensure the form is valid.')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'products/edit_review.html', {'form': form, 'product': review.product})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # The user must be the author of the review to be able to delete it
    if review.author_email != request.user.email:
        messages.error(request, 'You are not authorized to delete this review.')
        return redirect('product_detail', product_id=review.product.id)

    review.delete()
    messages.success(request, 'Review deleted successfully.')
    return redirect(reverse('product_detail', args=[review.product.id]))

    # A view for toggeling the wishlist

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        # Product is already in wishlist; no need to add it again.
        return redirect('product_detail', product_id=product.id)
    else:
        wishlist.products.add(product)

    return redirect('product_detail', product_id=product.id)