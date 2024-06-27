from datetime import datetime, date
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum, Case, When, IntegerField
from django.shortcuts import render, redirect

from user_panel.models import OrderItem
from .forms import BookForm,Categoryform
from .models import Book, Category, Notification
from user_panel.models import User_Credentials
from . import forms
# Create your views here.


def Admin_dashboard(request):
        current_date = date.today()
        # Using a Case expression to sum the quantity of available books (where out_of_stock is False)
        available_books_count = Book.objects.aggregate(
            total_count=Sum(
                Case(
                    When(out_of_stock=False, then='quantity'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )['total_count']

        # Render the result to a template or return it as needed
        context = {'available_books_count': available_books_count,'current_date': current_date}


        return render(request,'admin_template/index.html',context)


def Create_Book(request):
    if request.method == "POST":
        form = BookForm(request.POST, files=request.FILES)
        if form.is_valid():
            # Debugging: Print form data
            print(form.cleaned_data)
            form.save()
            return redirect('book_list')
        else:
            # Debugging: Print form errors
            print(form.errors)
    else:
        form = BookForm()  # Initialize a new form for GET requests

    return render(request, 'admin_template/addbook.html', {'form': form})
def new_arrivals(request):
    new_books = Book.objects.order_by('-created_date')[:20]  # Get the 10 newest books, adjust as needed
    return render(request, 'admin_template/new_arrivals.html', {'new_books': new_books})

def list_Book(request):
    books=Book.objects.all()
    in_stock_books = []
    out_of_stock_books = []

    for book in books:
        if book.quantity >= 1:
            in_stock_books.append(book)
        else:
            out_of_stock_books.append(book)
    paginator = Paginator(books, 10)  # Create a Paginator object with the query set and 5 items per page
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)  # Get the requested page
    except PageNotAnInteger:
        page = paginator.page(1)  # If page is not an integer, deliver the first page
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context={"book":books,'page':page}
    return render(request,'admin_template/listbook.html',context)



def Create_category(request):
    if request.method == "POST":
        form = Categoryform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Add a success message
            messages.success(request, "Category successfully added")
            return redirect('categories')
        else:
            # Add an error message for form validation errors
            messages.error(request, "Check entry")
    else:
        form = Categoryform()

    return render(request, 'admin_template/Categoryform.html', {'form': form})
def Categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_template/categories.html', {'categories': categories})

def books_by_category(request, category_id):
    categories = Category.objects.get(id=category_id)
    books = Book.objects.filter(categories=categories)
    return render(request, 'admin_template/books_by_category.html', {'categories': categories, 'books': books})

def update_category(request,category_id):
    category=Category.objects.get(id=category_id)
    if request.method=='POST':
        form=Categoryform(request.POST,files=request.FILES,instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form=Categoryform(instance=category)
    return render(request,'admin_template/updatecategory.html',{'form':form})

def Remove_category(request,category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    messages.success(request, 'Item Deleted successfully.')
    return redirect('categories')

def Update_Book(request, book_id):
    book = Book.objects.get(id=book_id)
    current_time = datetime.now().isoformat()

    try:
        latest_item = Book.objects.latest('updated')
        latest_updated_date = latest_item.updated
    except ObjectDoesNotExist:
        latest_updated_date = None

    if request.method == 'POST':
        print("POST Data:", request.POST)
        form = BookForm(request.POST, files=request.FILES, instance=book)

        if form.is_valid():
            book_instance = form.save(commit=False)
            book_instance.updated = current_time
            book_instance.save()

            messages.success(request, 'Item updated successfully.')

            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'admin_template/updatebook.html', {'form': form,'latest_updated_date': latest_updated_date})



def Remove_Book(request,book_id):
    book=Book.objects.get(id=book_id)
    book.delete()
    messages.success(request, 'Item Deleted successfully.')
    return redirect('book_list')



def View_Page(request,book_id):
    book = Book.objects.get(id=book_id)
    return render(request,'admin_template/viewpage.html',{'book':book})

def Search_Book(request):
    query=None
    books=None
    if 'q'in request.GET:
        query = request.GET.get('q')
        books = Book.objects.filter(Q(name__icontains=query) | Q(author__icontains=query))
    else:
        books = []  # Empty list when no query is provided

    return render(request, 'admin_template/search.html', {'books': books,'query':query})


def Admin_Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password = request.POST['password']
        admin=authenticate(username=username,password=password)
        try:
            if admin.is_superuser:
                login(request,admin)
                messages.info(request, 'login successfully')
                return redirect('dashboard')

            else:
                messages.error(request,"error in login")
        except:
            messages.info(request,"Invalid credentials . Connect with Admin")

    return render(request, 'admin_template/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


def admin_notifications(request):
    messages_list = messages.get_messages(request)


    context = {'messages_list': messages_list}
    return render(request, 'admin_template/notification.html',context)

def customer_order_view(request):
    ordered_items = OrderItem.objects.all()

    context = {'ordered_items': ordered_items}
    return render(request, 'admin_template/customer_order.html', context)


def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        # Update the order status in the database
        order = OrderItem.objects.get(pk=order_id)
        order.status = new_status
        order.save()

        # Redirect back to the order summary page

        return redirect('user_book:order_summary')


def user_loginLog(request):
    # Count the distinct users who have logged in
    registered_users = User_Credentials.objects.all()

    context = {
        'registered_users': registered_users,
    }

    return render(request, 'admin_template/userlog.html', context)