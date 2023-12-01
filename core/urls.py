from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from shop import views


urlpatterns = [
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('signup/',views.signup, name='signup'),
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:pk>/', login_required(views.add_to_cart), name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('place-order/', views.place_order, name='place_order'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('browse-orders/', views.browse_orders, name='browse_orders'),
    path('payment/', views.payment_page, name='payment_page'),
    path('process-payment/', views.process_payment, name='process_payment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
