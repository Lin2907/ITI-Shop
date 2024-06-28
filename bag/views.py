from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_bag(request):
    """A view that renders the bag contents page"""
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""
    
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = request.POST.get('product_size') if 'product_size' in request.POST else None
    color = request.POST.get('product_color') if 'product_color' in request.POST else None

    bag = request.session.get('bag', {})

    if item_id not in bag:
        bag[item_id] = {'items_by_size': {}}

    if size and color:
        if color not in bag[item_id]['items_by_size']:
            bag[item_id]['items_by_size'][color] = {}
        if size not in bag[item_id]['items_by_size'][color]:
            bag[item_id]['items_by_size'][color][size] = 0
        bag[item_id]['items_by_size'][color][size] += quantity
    elif size:
        if size not in bag[item_id]['items_by_size']:
            bag[item_id]['items_by_size'][size] = 0
        bag[item_id]['items_by_size'][size] += quantity
    else:
        if 'quantity' not in bag[item_id]:
            bag[item_id]['quantity'] = 0
        bag[item_id]['quantity'] += quantity

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size') if 'product_size' in request.POST else None
    color = request.POST.get('product_color') if 'product_color' in request.POST else None

    bag = request.session.get('bag', {})

    if size and color:
        if quantity > 0:
            bag[item_id]['items_by_size'][color][size] = quantity
        else:
            del bag[item_id]['items_by_size'][color][size]
            if not bag[item_id]['items_by_size'][color]:
                del bag[item_id]['items_by_size'][color]
            if not bag[item_id]['items_by_size']:
                del bag[item_id]
    elif size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                del bag[item_id]
    else:
        if quantity > 0:
            bag[item_id]['quantity'] = quantity
        else:
            del bag[item_id]

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = request.POST.get('product_size') if 'product_size' in request.POST else None
        color = request.POST.get('product_color') if 'product_color' in request.POST else None

        bag = request.session.get('bag', {})

        if size and color:
            del bag[item_id]['items_by_size'][color][size]
            if not bag[item_id]['items_by_size'][color]:
                del bag[item_id]['items_by_size'][color]
            if not bag[item_id]['items_by_size']:
                del bag[item_id]
        elif size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                del bag[item_id]
        else:
            del bag[item_id]

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
