from django.shortcuts import render

from django.shortcuts import render
from .models import *
from .forms import ProductSearchForm



def product_list(request):
    form = ProductSearchForm(request.GET)

    if not Product.objects.exists() and not Category.objects.exists() and not Brand.objects.exists():

        electronics_category = Category.objects.create(name='Electronics', description='Electronic devices')
        clothing_category = Category.objects.create(name='Clothing', description='Apparel and accessories')
        apple_brand = Brand.objects.create(name='Apple', country='USA')
        samsung_brand = Brand.objects.create(name='Samsung', country='South Korea')

        Product.objects.create(
            name='iPhone 13',
            price=799.99,
            brand=apple_brand,
            category=electronics_category,
            discount=0,
            status='NEW',
            quantity=100,
            in_stock=True
        )
        Product.objects.create(
            name='Galaxy S21',
            price=999.99,
            brand=samsung_brand,
            category=electronics_category,
            discount=10,
            status='POPULAR',
            quantity=50,
            in_stock=True
        )
        Product.objects.create(
            name='T-Shirt',
            price=19.99,
            brand=None,
            category=clothing_category,
            discount=5,
            status='DISCOUNT',
            quantity=200,
            in_stock=True
        )

    products = Product.objects.all()

    if form.is_valid():
        if form.cleaned_data['category']:
            products = products.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['brand']:
            products = products.filter(brand=form.cleaned_data['brand'])
        if form.cleaned_data['min_price']:
            products = products.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
            products = products.filter(price__lte=form.cleaned_data['max_price'])
        if form.cleaned_data['in_stock']:
            products = products.filter(in_stock=True)

    return render(request, 'product_list.html', {'products': products, 'form': form})
