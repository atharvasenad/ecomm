from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecommapp.models import Products,Cart,Order
import random
import razorpay
from django.core.mail import send_mail,EmailMessage
from django.db.models import Q
# Create your views here.
'''
def about(request):
    return HttpResponse("Hello from about function")

def contact(request):
    return HttpResponse("contact-7448267098")

def edit(request,rid):
    print("Id to be edited",rid)
    return HttpResponse("id to be edited:"+rid)

def delete(request,did):
    print("Id to be deleted",did)
    return HttpResponse("id to be deleted:"+did)

def hello(request):
    context={}
    context['data']="hello we passing to html file"
    context['x']=100
    context['y']=500
    context['l']=[10,20,30,40,50,60,70]
    context['products']=[
        {'id':1,'image':'p1image','name':'samsung','price':'18000','cat':'mobile'},
        {'id':2,'image':'p2image','name':'jeans','price':'1000','cat':'cloth'},
        {'id':3,'image':'p3image','name':'adidas','price':'5000','cat':'shoes'},
    ]
    return render(request,'hello.html',context)
'''


def products(request):
    p=Products.objects.filter(is_active=True)
    # print(p)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def cart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Products.objects.filter(id=pid)
        # check product exist or not
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['data']=p
        if n==1:
            context['msg']="product already exist in cart"
        else:
            c=Cart.objects.create(userid=u[0],pid=p[0])
            c.save()
            context['success']="Product added succesfully to cart"
        return render(request,'product_detail.html',context)
    else:
        return redirect('/login')

def placeorder(request):
    c=Cart.objects.filter(userid=request.user.id)
    orderid=random.randrange(1000,9999)
    # print(orderid)
    for x in c:
        amount=x.qty*x.pid.price
        o=Order.objects.create(orderid=orderid,qty=x.qty,pid=x.pid,userid=x.userid,amt=amount)
        o.save()
        x.delete()
    return redirect('/fetchorder')

def fetchorderdetails(request):
    orders=Order.objects.filter(userid=request.user.id)
    # print(orders)
    sum=0
    for x in orders:
        sum=sum+x.amt
    context={}
    context['orders']=orders
    context['tamount']=sum
    context['n']=len(orders)
    return render(request,'placeorder.html',context)

def product_detail(request,pid):
    p=Products.objects.filter(id=pid)
    context={}
    context['data']=p
    return render(request,'product_detail.html',context)

def register(request):
    context={}
    if request.method=="GET":
        return render(request,'register.html')
    else:
        n=request.POST['uname']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        if n=='' or p=='' or cp=='':
            context['errmsg']="Fields cannot be Empty!!"
        # return HttpResponse("data fetched")
            return render(request,'register.html',context)
        elif p!=cp:
            context['errmsg']="Password and Confirm Password Didn't Matched"
            return render(request,'register.html',context)
        elif len(p)<8:
            context['errmsg']="Password must be 8 characters"
            return render(request,'register.html',context)
        else:
          try:
            u=User.objects.create(username=n,email=n)
            u.set_password(p)
            u.save()
            context['success']="user created succesfully"
            return render(request,'register.html',context)
          except Exception:
              context['errmsg']="User with Same Username Already Exist Please login"
              return render(request,'register.html',context)

def user_login(request):
    if request.method =="GET":
        return render(request,'login.html')
    else:
        name=request.POST['uname']
        upass=request.POST['upass']
        # print(name)
        # print(upass)
        u=authenticate(username=name,password=upass)
        # print(u)
        if u is not None:
            login(request,u)
            return redirect('/products')
        else:
            context={}
            context['errmsg']="Invalid username or Password"
            return render(request,'login.html',context)

def user_logout(request):
    logout(request)
    return redirect('/products')

# category filter
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Products.objects.filter(q1 & q2)
    print(p)
    context={}
    context['data']=p
    # print(cv)
    return render(request,'index.html',context)

# sort price
def sortprice(request,sv):
    if sv=='1':
        t='-price'
    else:
        t='price'
    p=Products.objects.order_by(t).filter(is_active=True)
    context={}
    context['data']=p
    return render(request,'index.html',context)

# pricefilter
def pricefilter(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    p=Products.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request,'index.html',context)

def viewcart(request):
    c=Cart.objects.filter(userid=request.user.id)
    sum=0
    for x in c:
        sum=sum+x.pid.price*x.qty
    context={}
    context['data']=c
    context['total']=sum
    context['n']=len(c)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x =='1':
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect('/viewcart')
    # print(type(qty))
    # print(type(x))
    # return HttpResponse("qty fetched")

def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_8OBnL8eaOvYZXm", "eQ3ouTkVQbxDmYbbjrycwbbV"))
    orders=Order.objects.filter(userid=request.user.id)
    # print(orders)
    sum=0
    for x in orders:
        sum=sum+x.amt
        oid=x.orderid
    data = { "amount": sum*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['payment']=payment
    # context['amount']=sum
    return render(request,'pay.html',context)

# def paymentsuccess(request):
    # sub="Ekart-Order Status"
    # msg="Thanks for shopping, Order Details are:/n{{x.name}}/n{{x.price}}"
    # frm="atharvasenad4137@gmail.com"
    # u=User.objects.filter(id=request.user.id)
    # to=u[0].email
    # send_mail(
    # sub,
    # msg,
    # frm,
    # [to],
    # fail_silently=False
    # )
    # return render(request,'paymentsuccess.html')

def paymentsuccess(request):
    sub = "Ekart-Order Status"
    msg = "Thanks for Shopping. Order Details are:"
    frm = "atharvasenad4137@gmail.com"
    u = User.objects.filter(id=request.user.id)
    to = u[0].email
    email = EmailMessage(sub, msg, frm, [to])
    email.attach_file('templates/invoice.html')  
    email.send()
    return render(request,'paymentsuccess.html')

def removeorder(request,cid):
    o=Order.objects.filter(id=cid)
    o.delete()
    return redirect('/fetchorder')