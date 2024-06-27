from django.urls import path
from . import views
from .views import CheckOut


app_name='user_book'
urlpatterns = [
    path("",views.home,name='home'),
    path("contact/",views.contact,name='contact'),
    path("search-book/",views.user_Search_Book,name='search_book'),
    path("list/",views.user_list_Book,name='listbook'),
    path('new_arrivals/', views.new_arrivals, name='new_arrivals'),
    path('user-view-page/<int:book_id>/',views.user_View_Page,name='user_view'),
    path('user-add-to-cart/<int:book_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('increase-quantity/<int:item_id>/',views.increase_quantity,name='increase_quantity'),
    path('decrease-quantity/<int:item_id>/',views.decrease_quantity,name='decrease_quantity'),
    path('delete/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('increase_quantity/<int:item_id>/',views.increase_quantity,name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/',views.decrease_quantity,name='decrease_quantity'),
    path('user-register/', views.registerPage, name='register'),
    path('user-login/', views.user_login, name='user_login'),
    path("user-logout/", views.logout, name='user_logout'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('add_to_wishlist/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:book_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('category/<int:category_id>/', views.category_page, name='category_page'),
    path("book-scrap",views.scrape_book,name='search_scrap'),
    path("category/",views.Category_all,name='category'),
    path('checkout/',CheckOut.as_view(),name="checkout"),
    path('review/',views.review_page,name='review'),
    path('create-checkout-session/',views.create_checkout_session,name='create-checkout-session'),
    path('success/',views.success,name='success'),
    path('cancelled/', views.cancell, name='cancel'),
    path('order-summary/',views.order_confirmation,name='order_confirm'),
path('update_order_status/', views.get_latest_order_status, name='get_latest_order_status'),

    # path('create-payment-intent/<str:pk>/', StripeIntentView.as_view(), name='create-payment-intent'),


]