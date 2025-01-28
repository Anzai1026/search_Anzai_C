from itertools import product
from django.shortcuts import render, get_object_or_404, redirect
from search_app.models import Product, Category
from search_app.forms import ProductForm, SearchForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from search_app.utils import search_amazon_products
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # ユーザー作成
            return redirect('login')  # 作成後、ログインページにリダイレクト
    else:
        form = UserCreationForm()  # 空のフォームを表示

    return render(request, 'signup.html', {'form': form})

# Amazon商品検索
def amazon_product_search_view(request): 
    query = request.GET.get('q', '') 
    if query: 
        # Amazon APIを使って商品を検索 
        response_data = search_amazon_products(query) 
        return JsonResponse({'data': response_data}, safe=False) 
    else: 
        return JsonResponse({'error':  ' 検索クエリが指定されていません。'}, status=400)
    
# 商品作成・更新ビュー
def product_create_or_update_view(request, product_id=None):
    product = get_object_or_404(Product, id=product_id) if product_id else None

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {'form': form, 'product': product})


# 商品作成ビュー
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'product': product})

# 商品詳細ビュー
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# 商品編集ビュー
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'product': product})

# 商品削除ビュー
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

# 商品一覧ビュー
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# 検索ビュー
def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all()  # クエリセットの初期化

    # 検索クエリの処理
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query)

        # カテゴリフィルタリング
        category_name = request.GET.get('category')
        print(f"Category name from URL: {category_name}")  # デバッグ用
        if category_name:
            category_name = category_name.strip().lower()  # 空白削除と小文字化
            try:
                category = Category.objects.get(name=category_name)
                results = results.filter(category_id=category.id)
            except Category.DoesNotExist:
                results = results.none()

        # 価格のフィルタリング（最低価格・最高価格）
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            results = results.filter(price__gte=min_price)
        if max_price:
            results = results.filter(price__lte=max_price)

        # 並び替え処理
        sort_by = request.GET.get('sort', 'name')
        if sort_by == 'price_asc':
            results = results.order_by('price')
        elif sort_by == 'price_desc':
            results = results.order_by('-price')

    # ページネーション処理
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {'form': form, 'page_obj': page_obj, 'results': results})
