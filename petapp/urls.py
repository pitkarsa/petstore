"""
URL configuration for petapp application.

"""

from django.urls import path
from petapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.homeFunction),
    path('login',views.userlogin),
    path('register',views.register),
    path('details/<pid>',views.petdetails),
    path('logout',views.userlogout),
    path('addtocart/<petid>',views.addtocart),
    path('mycart',views.showMyCart),
    path('removecart/<cartid>',views.removeCart),
    path('confirmorder',views.confirmorder),
    path('searchby/<val>',views.searchPetByType),
    path('sort/<dir>',views.sortPetsByPrice),
    path('pricerange',views.rangeofprice),
    path('makepayment',views.makepayment),
    path('placeorder',views.placeorder),
]

urlpatterns += static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT )
