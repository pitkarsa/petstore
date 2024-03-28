from django.shortcuts import render, redirect
from petapp.models import Pet, Cart, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
import razorpay
import random
from django.core.mail import send_mail

# Create your views here.
def homeFunction(request):
    context = {}
    data = Pet.objects.all()
    context['pets'] = data
    return render(request,'index.html',context)

def searchPetByType(request,val):
    context={}    
    data = Pet.objects.filter(type = val )
    '''
    Writing multiple conditions using Q, and filtering data based on that
    c1 = Q(type = 'cat')
    c2 = Q(breed = 'persian')
    data = Pet.objects.filter(c1 & c2)
    '''
    context['pets'] = data
    return render(request,'index.html',context)

def sortPetsByPrice(request,dir):
    col=''
    context = {}
    if dir == 'asc':
        col='price'
    else:
        col='-price'
    data = Pet.objects.all().order_by(col)
    context['pets'] = data
    return render(request,'index.html',context)

def rangeofprice(request):
    context = {}
    min = request.GET['min']
    max =request.GET['max']
    c1 = Q(price__gte = min)
    c2 = Q(price__lte = max)
    data = Pet.objects.filter(c1 & c2)
    context['pets'] = data
    return render(request,'index.html',context)

def petdetails(request,pid):
    context = {}
    data = Pet.objects.filter(id = pid)
    context['pet'] = data[0]
    return render(request,'petdetails.html',context)

def userlogin(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        context = {}
        n = request.POST['username']
        p = request.POST['password']
        if n=='' or p=='':
            context['error'] = 'Please enter all the fields'
            return render(request,'login.html',context)
        else:
            user = authenticate(username = n, password= p)
            if user is not None:
                login(request,user)
                # context['success'] = 'Logged in successfully'
                messages.success(request,'Logged in successfully !!')
                return redirect('/')
            else:
                context['error'] = 'Please provide correct details'
                return render(request,'login.html',context)
            
def userlogout(request):
    context={}
    context['success']='Logged out successfully !! '
    logout(request)
    return redirect('/')

def register(request):
    if request.method == "GET":
        return render(request,'register.html')
    else:
        context = {}
        n = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirmpass']
        if n=='' or e=='' or p=='' or cp=='':
            context['error'] = 'Please enter all the fields'
            return render(request,'register.html',context)
        elif p != cp:
            context['error'] = 'Password and confirm password must be same !!'
            return render(request,'register.html',context)
        else:
            context['success'] = 'Registred Successfully!! Please Login'
            user = User.objects.create(username = n, email=e)
            user.set_password(p)# to set encrypted password
            user.save()
            return render(request,'login.html',context)
        
def addtocart(request,petid):
    userid = request.user.id
    context= {}
    if userid is None:        
        context['error'] = 'Plaese login so as to add the Pet in your cart'
        return render(request,'login.html',context)
    else:
        # cart will added if pet and user object is known
        userid = request.user.id
        users = User.objects.filter(id = userid)
        pets = Pet.objects.filter(id = petid)
        cart = Cart.objects.create(pid = pets[0] , uid = users[0] )
        cart.save()
        # context['success'] = 'Pet added to cart !!'
        messages.success(request,'Pet added to cart !!')
        return redirect('/')
    
def showMyCart(request):
    context = {}
    userid = request.user.id
    data = Cart.objects.filter(uid = userid )
    context['mycart'] = data
    count = len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count'] = count
    context['total'] = total
    return render(request,'mycart.html',context)

def removeCart(request,cartid):
    data = Cart.objects.filter(id = cartid)
    data.delete()
    messages.success(request,'Pet removed from your cart')
    return redirect('/mycart')

def confirmorder(request):
    context = {}
    userid = request.user.id
    data = Cart.objects.filter(uid = userid )
    context['mycart'] = data
    count = len(data)
    total=0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count'] = count
    context['total'] = total
    return render(request,'conforder.html',context)

def makepayment(request):
    '''
    get current userid
    calculating bill amnt:
        1. cart fetch 
        2. using loop, find the bill
    using razorpay make payment
    '''
    context = {}
    userid = request.user.id
    data = Cart.objects.filter(uid = userid )
    total = 0
    for cart in data:
        total += cart.pid.price * cart.quantity
    client = razorpay.Client(auth=("razorpay key", "razorpay secret key"))
    data = { "amount": total*100 , "currency": "INR", "receipt": "" }
    payment = client.order.create(data=data)
    print(payment)
    context['data'] = payment
    return render(request,'pay.html',context)


def placeorder(request):
    userid = request.user.id
    user = User.objects.filter(id = userid) # fetching user object as we need to set up the object reference
    mycart= Cart.objects.filter(uid = userid)
    ordid = random.randrange(10000,99999)
    # 43677
    for cart in mycart:
        pet = Pet.objects.filter(id = cart.pid.id) # fetching pet objects as we need to set object reference
        ord = Order.objects.create(uid = user[0], pid = pet[0], quantity = cart.quantity, orderid = ordid)
        ord.save()
    mycart.delete()

    msg_body = 'Order id is:'+str(ordid)
    custEmail = request.user.email
    send_mail(
    "Order placed successfully!!", #subject
    msg_body, 
    "sapitkar@gmail.com", #from
    [custEmail],
    fail_silently=False,
    )    

    messages.success(request,'Order placed successfully!!')
    return redirect('/')
