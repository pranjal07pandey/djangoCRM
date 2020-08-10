from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group    


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()

                group = Group.objects.get(name = 'customer')
                user.groups.add(group)

                Customer.objects.create(
                    user = user,
                )

                redirect('login')

        return render(request, 'accounts/register.html', {
            'form':form
        })


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('index')

    else:
        if request.method =='POST':
            username=  request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username= username, password= password)

            if user is not None:
                login(request, user)
                return redirect('index')

        return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')

# Create your views here.
@login_required(login_url='login')
@admin_only
def index(request):
    customers = Customer.objects.all()
    orders = Order.objects.order_by('-id')

    delivered = Order.objects.filter(status='Delivered')
    pending = Order.objects.filter(status='Pending')

    return render(request,'accounts/dashboard.html', {
        'customers':customers,
        'orders': orders,
        'delivered':delivered,
        'pending': pending
    })

    
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def pending(request):
    pending = Order.objects.filter(status='Pending')
    return render(request, 'accounts/pending.html',{
        'pending':pending
    })


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})
    

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id = pk)
    # orders = Order.objects.filter(customer = customer)
    orders = customer.order_set.all()

    myfilter = OrderFilter(request.GET, queryset= orders)
    orders = myfilter.qs
    # products = Order.objects.filter()

    return render(request, 'accounts/customers.html', {
        'customer':customer,
        'orders':orders,
        'myfilter':myfilter
    })

# def newCustomer(request):


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def newOrder(request, pk):
    customer = Customer.objects.get(id = pk)
    form = OrderFrom(initial={'customer':customer})
    if request.method == 'POST':
        form = OrderFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'accounts/newOrder.html',{
        'form':form
    })


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderFrom(instance=order)

    if request.method == 'POST':
        form = OrderFrom(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'accounts/updateOrder.html',{
        'form':form
    })
    

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id = pk)
    order.delete()

    return redirect('index')


def user(request):

    # orders = Customer.objects.filter(user = request.user)
    orders = request.user.customer.order_set.all()
    delivered = orders.filter(status='Delivered')
    pending = orders.filter(status='Pending')


     
    return render(request, 'accounts/user.html',{
        'orders':orders,
        'delivered':delivered,
        'pending':pending
    })