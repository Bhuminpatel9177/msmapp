"""msm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from msmapp import views
from django.conf.urls.static import static
from django.conf import settings


from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("main_pdf/", views.CustomerListView.as_view(), name="main_pdf"),
    path("pdf1/", views.customer_render, name="customer_render_view"),
    path("", views.index, name="index"),
    path("checkout/", views.checkout1, name="checkout"),
    path("contact/", views.Contact, name="contact"),
    path("about/", views.about, name="about"),
    path("shop/", views.shop, name="shop"),
    path("test/", views.test, name="test"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("add_wishlist/<str:id>", views.add_wishlist, name="add_wishlist"),
    path("sdetail/<str:id>", views.sdetail, name="sdetail"),
    path("account/", views.account, name="account"),
    path("service/", views.service, name="service"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("usernot/", views.usernot, name="usernot"),
    path("notlogin/", views.notlogin, name="notlogin"),
    path("ordernot/", views.ordernot, name="ordernot"),
    path("elec/<str:name>", views.elec, name="elec"),
    path("men/<str:name>", views.men, name="men"),
    path("women/<str:name>", views.women, name="women"),
    path("kitchen/<str:name>", views.kitchen, name="kitchen"),
    path("baby/<str:name>", views.baby, name="baby"),
    path("submen/<str:id>", views.submen, name="sub1"),
    path("history/", views.history11, name="history"),
    path("subwomen/<str:id>", views.subwomen, name="sub1"),
    path("subelec/<str:id>", views.subelec, name="sub1"),
    path("subkitchen/<str:id>", views.subkitchen, name="sub1"),
    path("subbaby/<str:id>", views.subbaby, name="sub1"),
    path("outer_add_cart/<str:id>", views.outer_add_cart, name="outer_add_cart"),
    path("add_cart/<str:id>", views.add_cart, name="add_cart"),
    path("cart/", views.cart, name="cart"),
    path("order/", views.orders, name="order"),
    path("cart/<str:id>", views.dele, name="dele"),
    path("history/<str:id>", views.dele_his, name="dele_his"),
    path("wishlist/<str:id>", views.dele_wish, name="dele_wish"),
    path("profile/", views.profile, name="profile"),
    path("resetpass/", views.resetpass, name="resetpass"),
    path("cpass/", views.ChangePassword.as_view(), name="cpass"),
    path("feedback/", views.feedback1, name="feedback"),
    path("buy/", views.buy, name="buy"),
    path("payment/", views.payment, name="payment"),
    path("p1/", views.p1, name="p1"),
    path("editprofile/<int:id>/", views.editProfile, name="editprofile"),
    path("main_pdf/", views.CustomerListView.as_view(), name="main_pdf"),
    path("pdf1/", views.customer_render, name="customer_render_view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
