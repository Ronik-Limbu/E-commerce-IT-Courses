from django.shortcuts import render,redirect
from .models import Course,Student,Order,Certificate
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Profile,Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from .form import ProfileUpdateForm,ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404




def home(request):
    data=Course.objects.all()
    return render(request,'main/home.html',{'data':data})


def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        age=request.POST['age']
        email=request.POST['email']
        message=request.POST['message']
        
        Student.objects.create(name=name,age=age,email=email,message=message)
        messages.success(request,f'Hi {name} Your form is sccessfully submitted!!!')
        
        return redirect("contact")
        
        
    
    return render(request,'main/contact.html')


def About_us(request):
    return render(request,'main/About_us.html')
    
def verify_certificate(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        finds = Certificate.objects.filter(Q(certificate_number__icontains=searched)|Q(issued_to__icontains=searched))
        return render(request, 'main/certificate_detail.html', {'finds': finds})
    return render(request, 'main/verify_certificate.html')


def all_courses(request):
    data=Course.objects.all()
    return render(request,'main/all_courses.html',{'data':data})

def search_form(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        finds = Course.objects.filter(Q(name__icontains=searched)|Q(price__icontains=searched))

        return render(request, 'main/search.html', {'finds': finds})

def course_reviews(request, id):
    course = Course.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
           
    else:
        form = ReviewForm()
    return render(request, 'main/product_detail.html', {'form': form, 'course': course})


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            else:
                # Create a new user
                User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=confirm_password)
                return redirect('log_in')
        else:
            messages.error(request, "Password and confirm password do not match!")
            return redirect("register")
    return render(request, 'auth/register.html')

def log_in(request):
    if request.method=='POST':
       username=request.POST['username']
       password=request.POST['password']

       user=authenticate(username=username,password=password)
       if not User.objects.filter(username=username).exists():
           messages.info(request,"username is not found")
       if user is not None:
          login(request,user)
          return redirect('home')
          
    return render(request, 'auth/log_in.html')


def log_out(request):
    logout(request)
    return redirect('home')


@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in') 

        subject = "thanks for training"
        message = "Thank you for visiting again"
        from_email = 'limburonik4#gmail.com'
        recipient_list = [email, 'sujanthadara71@gmail.com']
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
   
    return render(request,'auth/change_password.html',{'form':form})




@login_required(login_url='log_in')
def customer_profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    profile_form=ProfileUpdateForm(instance=profile)
    
    if request.method=='POST':
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        
    context={
        'form':profile_form,
        'user':request.user,
        'profile':request.user.profile
    }
    return render(request,'main/customer_profile.html',context)


def product_detail(request, id):
    course = get_object_or_404(Course, id=id)

    cmt_all = request.GET.get('cmt_all')
    if cmt_all:
        reviews = course.reviews.all()
    else:
        reviews = course.reviews.all()[:3]

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.course = course
            review.save()
            return redirect('product_detail', id=id)

    context = {
        'course': course,
        'form': form,
        'reviews': reviews,
        'cmt_all': cmt_all
    }

    return render(request, 'main/product_detail.html', context)












from .models import Cart, CartItem

@login_required(login_url="log_in")
def cart_detail(request):
    try:
        cart = Cart.objects.get(cart_id=request.user)
    except Cart.DoesNotExist:
        cart = Cart(cart_id=request.user)
        cart.save()
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'main/cart_detail.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url="log_in")
def cart_add(request, id):
    course = Course.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id=request.user)
    except Cart.DoesNotExist:
        cart = Cart(cart_id=request.user)
        cart.save()
    try:
        cart_item = CartItem.objects.get(cart=cart, course=course)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem(cart=cart, course=course)
        cart_item.save()
    return redirect("cart_detail")

@login_required(login_url="log_in")
def item_clear(request, id):
    try:
        cart_item = CartItem.objects.get(id=id)
    except CartItem.DoesNotExist:
        return redirect("cart_detail")
    
    if cart_item.cart.cart_id == request.user:
        cart_item.delete()
    return redirect("cart_detail")

@login_required(login_url="log_in")
def item_increment(request, id):
    course = Course.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id=request.user)
    except Cart.DoesNotExist:
        cart = Cart(cart_id=request.user)
        cart.save()
    cart_item = CartItem.objects.get(cart=cart, course=course)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart_detail")

@login_required(login_url="log_in")
def item_decrement(request, id):
    course = Course.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id=request.user)
    except Cart.DoesNotExist:
        cart = Cart(cart_id=request.user)
        cart.save()
    cart_item = CartItem.objects.get(cart=cart, course=course)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart_detail")

@login_required(login_url="log_in")
def cart_clear(request):
    try:
        cart = Cart.objects.get(cart_id=request.user)
    except Cart.DoesNotExist:
        cart = Cart(cart_id=request.user)
        cart.save()
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items.delete()
    return redirect("cart_detail")





from .models import Order, CartItem


@login_required(login_url="log_in")
def orders_list(request):
    orders = Order.objects.all()
    cart_items = CartItem.objects.all()
    total_price = sum(item.total_price for item in cart_items)
    context = {"orders": orders,"cart_items":cart_items,"total_price":total_price}
    return render(request, 'main/orders_list.html', context)


@login_required(login_url="log_in")
def order_remove(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('orders_list')
    return render(request, 'main/order_remove.html', {'order': order})
    
@login_required(login_url="log_in")
def order_checkout(request, id):
    order = Order.objects.get(id=id)
    cart_items = CartItem.objects.all()
    total_price = sum(item.total_price for item in cart_items)
    context = {"order": order,"cart_items":cart_items,"total_price":total_price}
    return render(request, 'main/order_checkout.html', context)



def create_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        Address = request.POST['Address']
        # total_price = request.POST['total_price']
        is_paid = request.POST.get('is_paid', False)  # default to False if 'is_paid' does not exist
        paid_amount = request.POST.get('paid_amount', 0)  # default to 0 if 'paid_amount' does not exist

        order = Order(name=name, phone_number=phone_number, Address=Address, is_paid=is_paid, paid_amount=paid_amount)
        order.save()

        return redirect('orders_list')
    return render(request, 'main/create_order.html')



@login_required(login_url="log_in")
def esewa_callback(request):
    oid = request.GET.get('oid')
    amt = request.GET.get('amt')
    refId = request.GET.get('refId')

    if oid is None or oid == 'None':
        messages.error(request, 'Invalid order ID')
        return redirect('main/home')

    try:
        oid = int(oid)  # Convert oid to integer
        order = Order.objects.get(id=oid)
    except ValueError:
        messages.error(request, 'Invalid order ID')
        return redirect('home')
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('home')

    order.is_paid = True
    order.paid_amount = amt
    order.save()
    messages.success(request, 'Order paid successfully!')
    return redirect('home')


@login_required(login_url="log_in")
def payment_failed(request):
    messages.error(request, 'Payment failed!')
    return redirect('cart_details')

from decimal import Decimal
import hmac
import hashlib
import base64
import uuid

@login_required(login_url="log_in")
def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=request.user)
    except Cart.DoesNotExist:
        cart = Cart(cart_id=request.user)
        cart.save()

    # Get the cart items for the current user
    cart_items = CartItem.objects.all()


    shipping = Decimal('0.0')  
    subtotal_amount = sum((item.course.price * Decimal(item.quantity)) for item in cart_items)
    subtotal_amount_formatted = format(subtotal_amount, ".2f")  # Format subtotal amount
    tax_rate = Decimal('0.003')  # Convert tax rate to Decimal (0.3% = 0.003)
    tax_amount = subtotal_amount * tax_rate
    tax_amount_formatted = format(tax_amount, ".2f")  # Format tax amount
    total_amount = subtotal_amount + tax_amount
    total_amount_formatted = format(total_amount, ".2f")
     
#     # Generate a unique transaction UUID
#     uuid_value = uuid.uuid4()

#     # Your eSewa SecretKey
#     secret_key = '8gBm/:&EnhH.1/q'

#     # Concatenate input parameters for signature
#     concatenated_string = f"{total_amount}{uuid_value}EPAYTEST"
#     hmac_sha256 = hmac.new(secret_key.encode(), concatenated_string.encode(), hashlib.sha256)
#     generated_signature = base64.b64encode(hmac_sha256.digest()).decode()
    
#     # Create the payload for eSewa
#     payload = {
#         'amt': total_amount_formatted,
#         'txAmt': tax_amount_formatted,
#         'tAmt': total_amount_formatted,
#         'scd': 'EPAYTEST',
#         'pid': ','.join(str(item.id) for item in cart_items),   # Use the order id
#         'uname': request.user.username,
#         'pno': request.user.phone_number if hasattr(request.user, 'phone_number') else '',  # Replace with your actual phone number field
#         'eml': request.user.email,
#         'mobno': request.user.mobile_number if hasattr(request.user, 'mobile_number') else '',  # Replace with your actual mobile number field
#         }

#     context = {
#         'cart_items': cart_items,
#         'subtotal_amount': subtotal_amount_formatted,  # Use formatted subtotal amount
#         'total_amount': total_amount,
#         'tax_amount': tax_amount_formatted,  # Use formatted tax amount
#         'shipping': shipping,
#         'uuid': str(uuid_value),
#         'esewa_signature': generated_signature,
#         'payload': payload,
        
#     }

#     return render(request, 'main/checkout.html', context)