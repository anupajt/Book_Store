from django.urls import path
from . import views

urlpatterns = [
    path("",views.Admin_dashboard,name='dashboard'),
    path("add-new-books/",views.Create_Book,name='add_book'),
    path("list-of-books/",views.list_Book,name="book_list"),
    path('add-category/',views.Create_category,name='create_category'),
    path('categories/',views.Categories,name='categories'),
    path('category/<int:category_id>/', views.books_by_category, name='books_by_category'),
    path('new_arrivals/', views.new_arrivals, name='new_arrivals'),
    path("update/<int:book_id>/",views.Update_Book,name="update"),
    path("delete/<int:book_id>/",views.Remove_Book,name="delete"),
    path("details/<int:book_id>/",views.View_Page,name="details"),
    path('search/',views.Search_Book,name='search'),
    path('login/', views.Admin_Login, name='login'),
    path('logout/',views.logout,name="logout"),
    path('update_categoey/<int:category_id>/',views.update_category,name='update_category'),
    path('delete_categoey/<int:category_id>/',views.Remove_category,name='delete_category'),
    path('notifications/',views.admin_notifications,name='notifications'),
    path('customer_orders/', views.customer_order_view, name='customer_orders'),
    path('user-log/',views.user_loginLog,name='user_log')




]