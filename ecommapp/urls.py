from django.urls import path
from ecommapp import views
from django.conf import settings
from django.conf.urls.static import static
'''
urlpatterns = [
    path('about',views.about),
    # path('contact',views.contact),
    path('edit/<rid>',views.edit),
    path('delete/<did>',views.delete),
]'''

urlpatterns=[
    path('products',views.products),
    path('about',views.about),
    path('contact',views.contact),
    path('cart',views.cart),
    path('product_detail/<pid>',views.product_detail),
    path('placeorder',views.placeorder),
    path('login',views.user_login),
    path('register',views.register),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sortprice),
    path('pricefilter',views.pricefilter),
    path('addcart/<pid>',views.cart),
    path('viewcart',views.viewcart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('removecart/<cid>',views.removecart),
    path('fetchorder',views.fetchorderdetails),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),
    path('removeorder/<cid>',views.removeorder),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)