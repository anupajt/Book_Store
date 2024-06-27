from datetime import datetime

from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Case,When, IntegerField
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from admin_panel.models import Book, Category, Notification
from .forms import UserRegisterForm, BillingAddressForm
from .decorators import login_required
from .models import Cart, CartItem, Wishlist, User_Credentials, Address, Order, Order_confirm, OrderItem
import requests
from bs4 import BeautifulSoup
from django.conf import settings

import stripe


def home(request):
    return render(request, 'user_template/index.html')

def contact(request):
    return render(request,'user_template/contact.html')
@login_required
def user_list_Book(request):
    category=Category.objects.all()
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 8)  # Show 10 books per page (you can adjust this number)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'user_template/userbooklist.html', {'page': page,'category':category})


def user_Search_Book(request):
    query = request.GET.get('q')
    books = []

    if query:
        books = Book.objects.filter(Q(name__icontains=query) | Q(author__icontains=query)| Q(categories__c_name__icontains=query))

    return render(request, 'user_template/usersearch.html', {'books': books})

@login_required
def user_View_Page(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'user_template/userviewpage.html', {'book': book})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.quantity > 0:  # Check if the book is in stock
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not item_created:
            # If the item already exists in the cart, increase the quantity
            cart_item.quantity += 1
            cart_item.save()
    return redirect('user_book:cart')






@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    cart_item = CartItem.objects.all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    total_items = cart_items.count()

    context = {'cart_items': cart_items, 'total_price': total_price, 'total_items': total_items, 'cart_item': cart_item}
    return render(request, 'user_template/cart.html', context)


@login_required
def increase_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity < cart_item.book.quantity:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('user_book:cart')  # Redirect back to the cart

@login_required
def decrease_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('user_book:cart')  # Redirect back to the cart

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('user_book:cart')

@login_required
def add_to_wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.books.add(book)
    return redirect('user_book:wishlist')

@login_required
def remove_from_wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.books.remove(book)
    return redirect('user_book:wishlist')

@login_required
def view_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_books = wishlist.books.all()
    return render(request, 'user_template/wishlist.html', {'wishlist_books': wishlist_books})


def new_arrivals(request):
    new_books = Book.objects.order_by('-created_date')[:20]  # Get the 10 newest books, adjust as needed
    return render(request, 'user_template/new_arrivals.html', {'new_books': new_books})


def registerPage(request):
    form=UserRegisterForm()
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'Registration Successful for '+user )
            return redirect('user_book:user_login')
        else:
            messages.error(request, 'Registration Failed')

    context={'form':form}
    return render(request,'user_template/register.html',context)

def user_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None and user is not user.is_superuser:
            login(request,user)
            print("login successful")
            return redirect("user_book:home")
        else:
            print("Authentication failed")

    return render(request, 'user_template/userlogin.html')
#
def logout(request):
    auth.logout(request)
    return redirect('user_book:home')



def Category_all(request):
    categories=Category.objects.all()
    return render(request,'user_template/all_category.html',{'categories':categories})

@login_required
def category_page(request, category_id):
    categories = get_object_or_404(Category, id=category_id)
    books_in_category = Book.objects.filter(categories=categories)
    print(categories)
    return render(request, 'user_template/user_books_by_category.html', {'categories': categories, 'books': books_in_category})



from gtts import gTTS
import os
import tempfile
#
# from translate import Translator
#
# # ...
#
# def scrape_book(request):
#     title = ""
#     description = ""
#     translated_description = ""
#
#     if request.method == 'POST':
#         book_name = request.POST.get('book_name')
#         if not book_name:
#             return render(request, 'user_template/scraping.html', {'error': 'Please provide a book name'})
#
#         try:
#             sanitized_book_name = book_name.replace(' ', '_')
#             website_url = f"https://en.wikipedia.org/wiki/{sanitized_book_name}"
#
#             response = requests.get(website_url)
#             response.raise_for_status()
#
#             soup = BeautifulSoup(response.text, 'html.parser')
#
#             book_info = soup.find('h1', {"class": "firstHeading mw-first-heading"})
#             if book_info:
#                 title = book_info.text.strip()
#
#             book_description = soup.find('div', {'class': 'mw-parser-output'})
#
#             if book_description:
#                 paragraphs = book_description.find_all('p')
#                 description = " ".join([p.text.strip() for p in paragraphs])
#
#                 try:
#                     translator = Translator(to_lang='ml')  # Replace 'ml' with your target language code
#                     translated_description = translator.translate(description)
#                 except Exception as e:
#                     # Handle the translation error
#                     translated_description = f"Translation error: {str(e)}"
#
#         except requests.exceptions.RequestException as e:
#             return render(request, 'user_template/scraping.html', {'error': f"An error occurred: {str(e)}"})
#
#     return render(request, 'user_template/scraping.html', {'title': title, 'description': description, 'translated_description': translated_description})
#


#


import gtts
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
import pygame

def scrape_book(request):
    title = ""
    description = ""
    audio_file_path = ""  # Initialize the variable

    if request.method == 'POST':
        book_name = request.POST.get('book_name')

        if not book_name:
            return render(request, 'user_template/scraping.html', {'error': 'Please provide a book name'})

        sanitized_book_name = book_name.replace(' ', '_')
        website_url = f"https://en.wikipedia.org/wiki/{sanitized_book_name}"

        try:
            response = requests.get(website_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            book_info = soup.find('h1', {"class": "firstHeading mw-first-heading"})
            if book_info:
                title = book_info.text.strip()

            book_description = soup.find('div', {'class': 'mw-parser-output'})

            if book_description:
                paragraphs = book_description.find_all('p')
                description = " ".join([p.text.strip() for p in paragraphs])

                # Perform audio synthesis using the gtts library with English language
                tts = gtts.gTTS(description, lang="en")
                audio_file_path = "hello.mp3"
                tts.save(audio_file_path)

                # Initialize pygame mixer
                pygame.mixer.init()

                # Load and play the audio file
                pygame.mixer.music.load(audio_file_path)
                pygame.mixer.music.play()

                # Wait for the audio to finish playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

        except requests.exceptions.RequestException as e:
            return render(request, 'user_template/scraping.html', {'error': f"An error occurred: {str(e)}"})

    return render(request, 'user_template/scraping.html', {'title': title, 'description': description, 'audio_file_path': audio_file_path})



# import gtts
# from playsound import playsound
# import requests
# from django.shortcuts import render
# from bs4 import BeautifulSoup
#
# def scrape_book(request):
#     title = ""
#     description = ""
#     audio_file_path = ""  # Initialize the variable
#
#     if request.method == 'POST':
#         book_name = request.POST.get('book_name')
#
#         if not book_name:
#             return render(request, 'user_template/scraping.html', {'error': 'Please provide a book name'})
#
#         sanitized_book_name = book_name.replace(' ', '_')
#         website_url = f"https://en.wikipedia.org/wiki/{sanitized_book_name}"
#
#         try:
#             response = requests.get(website_url)
#             response.raise_for_status()
#
#             soup = BeautifulSoup(response.text, 'html.parser')
#
#             book_info = soup.find('h1', {"class": "firstHeading mw-first-heading"})
#             if book_info:
#                 title = book_info.text.strip()
#
#             book_description = soup.find('div', {'class': 'mw-parser-output'})
#
#             if book_description:
#                 paragraphs = book_description.find_all('p')
#                 description = " ".join([p.text.strip() for p in paragraphs])
#
#                 # Perform audio synthesis using the gtts library with English language
#                 tts = gtts.gTTS(description, lang="en")
#                 audio_file_path = "hello.mp3"
#                 tts.save(audio_file_path)
#
#                 # Play the audio file
#                 playsound(audio_file_path)
#
#         except requests.exceptions.RequestException as e:
#             return render(request, 'user_template/scraping.html', {'error': f"An error occurred: {str(e)}"})
#
#     return render(request, 'user_template/scraping.html', {'title': title, 'description': description, 'audio_file_path': audio_file_path})




from django.db import transaction


class CheckOut(View):
    @transaction.atomic
    def get(self, request):
        # Add your GET request logic here (e.g., rendering the form)
        form = BillingAddressForm()
        context = {'form': form}
        return render(request, 'user_template/checkout.html', context)
    @transaction.atomic
    def post(self, request):
        form = BillingAddressForm(request.POST)



        if form.is_valid():
            # Create a billing address from the form data
            billing_address = Address(
                name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone_number'],
                street_address=form.cleaned_data['street_address'],
                apartment_suite=form.cleaned_data['apartment_suite'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code'],
                country=form.cleaned_data['country']
            )
            billing_address.save()
            cart = Cart.objects.get(user=request.user)


            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                order = Order(

                    product=cart_item.book,
                    price=cart_item.book.price,
                    billing_address=billing_address,
                    quantity=cart_item.quantity
                )
                order.save()

            # Clear the cart session
            request.session['cart'] = {}

            messages.success(request, 'Address added')
            return redirect('user_book:review')
        else:
            # Handle form validation errors here
            messages.error(request, 'Address not taken')
            context = {'form': form}
            return render(request, 'user_template/checkout.html', context)


def review_page(request):
    user = request.user  # Retrieve the user
    orders = []
    total=[]# Create an empty list to store the order objects

    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        order = Order(
            product=cart_item.book,
            price=cart_item.book.price,
            image=cart_item.book.image,  # Assuming 'image' is a field in your Order model
            quantity=cart_item.quantity
        )
        order.save()
        orders.append(order)  # Add the order object to the list
        total = sum(order.price for order in orders)


    try:
        billing_address = Address.objects.all() # Adjust this based on your model structure
    except Address.DoesNotExist:
        billing_address = None
    for order in orders:
        print(order.product.name, order.quantity, order.price, order.image.url)
    print(billing_address)


    context = {
        'orders': orders,  # Pass the list of orders
        'billing_address': billing_address,
        'total':total# Pass the billing address
    }

    return render(request, 'user_template/order_snippet.html', context)






your_domain=' http://127.0.0.1:8000/'
def create_checkout_session(request):
    # try:
        # Replace this with your logic to obtain the product to be sold
    cart_items = CartItem.objects.all()
    print(cart_items)# Fetch the first cart item for demonstration

    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if request.method == 'POST':
            line_items = []

            # Iterate through the cart items and add them to the line_items list
            for cart_item in cart_items:
                if cart_item.book:
                    line_item = {
                        'price_data': {
                            'currency': 'INR',
                            'unit_amount': int(cart_item.book.price * 100),  # Amount should be in cents
                            'product_data': {
                                'name': cart_item.book.name,
                            },
                        },
                        'quantity': 1,
                    }
                    line_items.append(line_item)

            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('user_book:success')),
                    cancel_url=request.build_absolute_uri(reverse('user_book:cancel')),
                )

                return redirect(checkout_session.url, code=303)







def success(request):
    # Retrieve the cart items
    cart_items = CartItem.objects.all()

    # Calculate the total quantity and total amount
    total_quantity = sum(cart_item.quantity for cart_item in cart_items)
    total_amount = sum(cart_item.book.price * cart_item.quantity for cart_item in cart_items)

    # Create an order record
    order = Order_confirm.objects.create(user=request.user, total_amount=total_amount)

    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.book, quantity=cart_item.quantity, price=cart_item.book.price)

    # Update product quantities in the database
    for cart_item in cart_items:
        product = cart_item.book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()
        else:
            # Handle cases where there is not enough quantity in stock
            messages.error(request, f'Not enough quantity in stock for {book.name}.')
            return redirect('user_book:cart')  # Redirect to the cart or a relevant page

    # Clear the user's cart
    cart_items.delete()

    return render(request, 'user_template/success.html')


def order_confirmation(request):


    orders = Order_confirm.objects.all()
    order_items = OrderItem.objects.select_related('order', 'product').all()
    admin_username = request.user
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = "A new order has been placed"

    try:
        admin = User.objects.get(username=admin_username)

        # Create a notification for the admin
        notification = Notification.objects.create(user=admin, message=message)

        # Send a message to the admin
        messages.success(request, 'New order notification sent to admin.',notification)

    except User.DoesNotExist:
        # Handle the case where the admin user does not exist
        messages.error(request, 'Admin user not found.')


    context = {
        'orders': orders,
        'order_items': order_items,

    }

    return render(request, 'user_template/order_summary.html', context)
def get_latest_order_status(request, order_id):
    # Query the database to get the latest order status based on the order_id
    try:
        order = Order.objects.get(id=order_id)
        latest_status = order.status
        return JsonResponse({'status': latest_status})
    except Order.DoesNotExist:
        return JsonResponse({'status': 'Order not found'}, status=404)




def cancell(request):
    return render(request,'user_template/cancelled.html')