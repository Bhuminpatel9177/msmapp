from django.shortcuts import render, redirect
from .models import *
import razorpay


from django.contrib import messages
from django.core import serializers
from django.views import View
from django.views.generic import View

from django.core.mail import EmailMultiAlternatives
from msm.settings import EMAIL_HOST_USER
from django.core.mail import message
from .forms import EditProfile

from django.shortcuts import redirect, get_object_or_404, render
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


import random


# Create your views:
def index(request):
    con = {}
    if "is_logged" in request.session:
        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        con["user"] = user
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        con["count"] = count
        img = r1.image
        con["img"] = img
    else:

        return render(request, "index.html", con)
    return render(request, "index.html", con)

    # return render(request, "index.html")


def register(request):
    if request.method == "POST":
        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        img = r1.image

        fname = request.POST["fname"]
        lname = request.POST["lname"]
        eadd = request.POST["eadd"]
        cnumber = request.POST["cnumber"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        city = request.POST["city"]
        password = request.POST["password"]

        valid = Register(
            fname=fname,
            lname=lname,
            eadd=eadd,
            cnumber=cnumber,
            dob=dob,
            gender=gender,
            address=address,
            pincode=pincode,
            city=city,
            password=password,
        )

        if "image" in request.FILES:
            img = request.FILES["image"]
            valid.image = img
            valid.save()
        valid.save()
        return redirect("/login")
    return render(request, "registration.html")


def login(request):
    if request.method == "POST":
        # name = request.POST["name"]
        eadd = request.POST["eadd"]
        password = request.POST["password"]

        if Register.objects.filter(eadd=eadd, password=password):
            valid = Register.objects.get(eadd=eadd, password=password)
            # print("*************************************************************")
            user_name = valid.fname
            request.session["is_logged"] = eadd
            v1 = "welcome"
            v = messages.error(request, " ")
            return render(request, "index.html", {"v1": v1, "user": user_name})
        else:
            v1 = "not exist"
            v = messages.error(request, " ")
            return render(request, "login.html", {"v1": v1})
    return render(request, "login.html")


def logout(request):
    if "is_logged" in request.session:
        del request.session["is_logged"]
        return redirect("index")
    else:
        return redirect("/usernot")


def about(request):
    con = {}
    if "is_logged" in request.session:
        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        con["user"] = user
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        con["count"] = count
        img = r1.image
        con["img"] = img
    else:
        pass
    return render(request, "about.html", con)


def elec(request, name):
    if "is_logged" in request.session:
        fcat = categories.objects.filter(name=name)
        sub = subcategories.objects.filter(cname_id=fcat[0].id)
        prod = products.objects.filter(category_id=fcat[0].id)

        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        c1 = sub.count()
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        img = r1.image

        if request.method == "POST":
            if "kind" in request.POST:
                se1 = request.POST["se1"]
                se1 = str(se1)
                print(se1)
                se_pro = products.objects.filter(category_id=fcat[0].id, p_type=se1)
                print(se_pro)
                return render(
                    request,
                    "electronic.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "se_pro": se_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )

            elif "price1" in request.POST:
                min1 = request.POST["min"]
                max1 = request.POST["max"]
                print(min1)
                print(max1)
                price_pro = products.objects.filter(
                    category_id=fcat[0].id, price__range=(int(min1), int(max1))
                )
                print(price_pro)
                return render(
                    request,
                    "electronic.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "price_pro": price_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )
            elif "ser1" in request.POST:
                qs = products.objects.all()
                title1 = request.POST.get("search")
                if title1 != "" and title1 is not None:
                    qs = qs.filter(product_name__icontains=title1)
                    cou1 = qs.count()
                    print(cou1)
                    return render(
                        request,
                        "electronic.html",
                        {
                            "qs": qs,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                            "cou1": cou1,
                        },
                    )
                else:
                    search_err = "Not Found " + '"' + se1 + '"'
                    print(search_err)
                    return render(
                        request,
                        "electronic.html",
                        {
                            "search_err": search_err,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                        },
                    )
            else:
                pass

        return render(
            request,
            "electronic.html",
            {
                "prod": prod,
                "sub": sub,
                "count": count,
                "user": user,
                "c1": c1,
                "img": img,
            },
        )
    else:
        return redirect("notlogin")


def subelec(request, id):
    sub = subcategories.objects.filter()
    sm = subcategories.objects.filter(name=id)
    prod = products.objects.filter(subcategory_id=sm[0].id)
    if request.method == "POST":
        if "kind" in request.POST:
            se1 = request.POST["se1"]
            se1 = str(se1)
            print(se1)
            se_pro = products.objects.filter(subcategory_id=sm[0].id, p_type=se1)
            print(se_pro)
            return render(
                request,
                "electronic.html",
                {
                    "prod": prod,
                    "se_pro": se_pro,
                },
            )

        elif "price1" in request.POST:
            min1 = request.POST["min"]
            max1 = request.POST["max"]
            print(min1)
            print(max1)
            price_pro = products.objects.filter(
                subcategory_id=sm[0].id, price__range=(int(min1), int(max1))
            )
            print(price_pro)
            return render(
                request,
                "electronic.html",
                {
                    "prod": prod,
                    "price_pro": price_pro,
                },
            )
        else:
            pass
    return render(request, "electronic.html", {"prod": prod})


def men(request, name):
    if "is_logged" in request.session:

        fcat = categories.objects.filter(name=name)
        sub = subcategories.objects.filter(cname_id=fcat[0].id)
        prod = products.objects.filter(category_id=fcat[0].id)

        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        c1 = sub.count()
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        img = r1.image

        if request.method == "POST":
            if "kind" in request.POST:
                se1 = request.POST["se1"]
                se1 = str(se1)
                print(se1)
                se_pro = products.objects.filter(category_id=fcat[0].id, p_type=se1)
                print(se_pro)
                return render(
                    request,
                    "men.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "se_pro": se_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )

            elif "price1" in request.POST:
                min1 = request.POST["min"]
                max1 = request.POST["max"]
                print(min1)
                print(max1)
                price_pro = products.objects.filter(
                    category_id=fcat[0].id, price__range=(int(min1), int(max1))
                )
                print(price_pro)
                return render(
                    request,
                    "men.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "price_pro": price_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )
            elif "ser1" in request.POST:
                qs = products.objects.all()
                title1 = request.POST.get("search")
                if title1 != "" and title1 is not None:
                    qs = qs.filter(product_name__icontains=title1)
                    cou1 = qs.count()
                    print(cou1)
                    return render(
                        request,
                        "men.html",
                        {
                            "qs": qs,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                            "cou1": cou1,
                        },
                    )
                else:
                    search_err = "Not Found " + '"' + se1 + '"'
                    print(search_err)
                    return render(
                        request,
                        "men.html",
                        {
                            "search_err": search_err,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                        },
                    )
            else:
                pass

        return render(
            request,
            "men.html",
            {
                "prod": prod,
                "sub": sub,
                "count": count,
                "user": user,
                "c1": c1,
                "img": img,
            },
        )
    else:
        return redirect("notlogin")


def submen(request, id):
    sub = subcategories.objects.filter()
    sm = subcategories.objects.filter(name=id)
    prod = products.objects.filter(subcategory_id=sm[0].id)
    if request.method == "POST":
        if "kind" in request.POST:
            se1 = request.POST["se1"]
            se1 = str(se1)
            print(se1)
            se_pro = products.objects.filter(subcategory_id=sm[0].id, p_type=se1)
            print(se_pro)
            return render(
                request,
                "men.html",
                {
                    "prod": prod,
                    "se_pro": se_pro,
                },
            )

        elif "price1" in request.POST:
            min1 = request.POST["min"]
            max1 = request.POST["max"]
            print(min1)
            print(max1)
            price_pro = products.objects.filter(
                subcategory_id=sm[0].id, price__range=(int(min1), int(max1))
            )
            print(price_pro)
            return render(
                request,
                "men.html",
                {
                    "prod": prod,
                    "price_pro": price_pro,
                },
            )
        else:
            pass
    return render(request, "men.html", {"prod": prod})


def women(request, name):
    if "is_logged" in request.session:
        fcat = categories.objects.filter(name=name)
        sub = subcategories.objects.filter(cname_id=fcat[0].id)
        prod = products.objects.filter(category_id=fcat[0].id)

        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        c1 = sub.count()
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        img = r1.image

        if request.method == "POST":
            if "kind" in request.POST:
                se1 = request.POST["se1"]
                se1 = str(se1)
                print(se1)
                se_pro = products.objects.filter(category_id=fcat[0].id, p_type=se1)
                print(se_pro)
                return render(
                    request,
                    "women.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "se_pro": se_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )

            elif "price1" in request.POST:
                min1 = request.POST["min"]
                max1 = request.POST["max"]
                print(min1)
                print(max1)
                price_pro = products.objects.filter(
                    category_id=fcat[0].id, price__range=(int(min1), int(max1))
                )
                print(price_pro)
                return render(
                    request,
                    "women.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "price_pro": price_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )
            elif "ser1" in request.POST:
                qs = products.objects.all()
                title1 = request.POST.get("search")
                if title1 != "" and title1 is not None:
                    qs = qs.filter(product_name__icontains=title1)
                    cou1 = qs.count()
                    print(cou1)
                    return render(
                        request,
                        "women.html",
                        {
                            "qs": qs,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                            "cou1": cou1,
                        },
                    )
                else:
                    search_err = "Not Found " + '"' + se1 + '"'
                    print(search_err)
                    return render(
                        request,
                        "women.html",
                        {
                            "search_err": search_err,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                        },
                    )
            else:
                pass

        return render(
            request,
            "women.html",
            {
                "prod": prod,
                "sub": sub,
                "count": count,
                "user": user,
                "c1": c1,
                "img": img,
            },
        )
    else:
        return redirect("notlogin")


def subwomen(request, id):
    sub = subcategories.objects.filter()
    sm = subcategories.objects.filter(name=id)
    prod = products.objects.filter(subcategory_id=sm[0].id)
    if request.method == "POST":
        if "kind" in request.POST:
            se1 = request.POST["se1"]
            se1 = str(se1)
            print(se1)
            se_pro = products.objects.filter(subcategory_id=sm[0].id, p_type=se1)
            print(se_pro)
            return render(
                request,
                "women.html",
                {
                    "prod": prod,
                    "se_pro": se_pro,
                },
            )

        elif "price1" in request.POST:
            min1 = request.POST["min"]
            max1 = request.POST["max"]
            print(min1)
            print(max1)
            price_pro = products.objects.filter(
                subcategory_id=sm[0].id, price__range=(int(min1), int(max1))
            )
            print(price_pro)
            return render(
                request,
                "women.html",
                {
                    "prod": prod,
                    "price_pro": price_pro,
                },
            )
        else:
            pass
    return render(request, "women.html", {"prod": prod})


def kitchen(request, name):
    if "is_logged" in request.session:
        fcat = categories.objects.filter(name=name)
        sub = subcategories.objects.filter(cname_id=fcat[0].id)
        prod = products.objects.filter(category_id=fcat[0].id)

        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        c1 = sub.count()
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        img = r1.image

        if request.method == "POST":
            if "kind" in request.POST:
                se1 = request.POST["se1"]
                se1 = str(se1)
                print(se1)
                se_pro = products.objects.filter(category_id=fcat[0].id, p_type=se1)
                print(se_pro)
                return render(
                    request,
                    "kitchen.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "se_pro": se_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )

            elif "price1" in request.POST:
                min1 = request.POST["min"]
                max1 = request.POST["max"]
                print(min1)
                print(max1)
                price_pro = products.objects.filter(
                    category_id=fcat[0].id, price__range=(int(min1), int(max1))
                )
                print(price_pro)
                return render(
                    request,
                    "kitchen.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "price_pro": price_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )
            elif "ser1" in request.POST:
                qs = products.objects.all()
                title1 = request.POST.get("search")
                if title1 != "" and title1 is not None:
                    qs = qs.filter(product_name__icontains=title1)
                    cou1 = qs.count()
                    print(cou1)
                    return render(
                        request,
                        "kitchen.html",
                        {
                            "qs": qs,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                            "cou1": cou1,
                        },
                    )
                else:
                    search_err = "Not Found " + '"' + se1 + '"'
                    print(search_err)
                    return render(
                        request,
                        "kitchen.html",
                        {
                            "search_err": search_err,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                        },
                    )
            else:
                pass

        return render(
            request,
            "kitchen.html",
            {
                "prod": prod,
                "sub": sub,
                "count": count,
                "user": user,
                "c1": c1,
                "img": img,
            },
        )
    else:
        return redirect("notlogin")


def subkitchen(request, id):
    sub = subcategories.objects.filter()
    sm = subcategories.objects.filter(name=id)
    prod = products.objects.filter(subcategory_id=sm[0].id)
    if request.method == "POST":
        if "kind" in request.POST:
            se1 = request.POST["se1"]
            se1 = str(se1)
            print(se1)
            se_pro = products.objects.filter(subcategory_id=sm[0].id, p_type=se1)
            print(se_pro)
            return render(
                request,
                "kitchen.html",
                {
                    "prod": prod,
                    "se_pro": se_pro,
                },
            )

        elif "price1" in request.POST:
            min1 = request.POST["min"]
            max1 = request.POST["max"]
            print(min1)
            print(max1)
            price_pro = products.objects.filter(
                subcategory_id=sm[0].id, price__range=(int(min1), int(max1))
            )
            print(price_pro)
            return render(
                request,
                "kitchen.html",
                {
                    "prod": prod,
                    "price_pro": price_pro,
                },
            )
        else:
            pass
    return render(request, "kitchen.html", {"prod": prod})


def baby(request, name):
    if "is_logged" in request.session:
        fcat = categories.objects.filter(name=name)
        sub = subcategories.objects.filter(cname_id=fcat[0].id)
        prod = products.objects.filter(category_id=fcat[0].id)

        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        c1 = sub.count()
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        img = r1.image

        if request.method == "POST":
            if "kind" in request.POST:
                se1 = request.POST["se1"]
                se1 = str(se1)
                print(se1)
                se_pro = products.objects.filter(category_id=fcat[0].id, p_type=se1)
                print(se_pro)
                return render(
                    request,
                    "baby.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "se_pro": se_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )

            elif "price1" in request.POST:
                min1 = request.POST["min"]
                max1 = request.POST["max"]
                print(min1)
                print(max1)
                price_pro = products.objects.filter(
                    category_id=fcat[0].id, price__range=(int(min1), int(max1))
                )
                print(price_pro)
                return render(
                    request,
                    "baby.html",
                    {
                        "prod": prod,
                        "sub": sub,
                        "price_pro": price_pro,
                        "count": count,
                        "user": user,
                        "c1": c1,
                    },
                )
            elif "ser1" in request.POST:
                qs = products.objects.all()
                title1 = request.POST.get("search")
                if title1 != "" and title1 is not None:
                    qs = qs.filter(product_name__icontains=title1)
                    cou1 = qs.count()
                    print(cou1)
                    return render(
                        request,
                        "baby.html",
                        {
                            "qs": qs,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                            "cou1": cou1,
                        },
                    )
                else:
                    search_err = "Not Found " + '"' + se1 + '"'
                    print(search_err)
                    return render(
                        request,
                        "baby.html",
                        {
                            "search_err": search_err,
                            "sub": sub,
                            "count": count,
                            "user": user,
                            "c1": c1,
                        },
                    )
            else:
                pass

        return render(
            request,
            "baby.html",
            {
                "prod": prod,
                "sub": sub,
                "count": count,
                "user": user,
                "c1": c1,
                "img": img,
            },
        )
    else:
        return redirect("notlogin")


def subbaby(request, id):
    sub = subcategories.objects.filter()
    sm = subcategories.objects.filter(name=id)
    prod = products.objects.filter(subcategory_id=sm[0].id)
    if request.method == "POST":
        if "kind" in request.POST:
            se1 = request.POST["se1"]
            se1 = str(se1)
            print(se1)
            se_pro = products.objects.filter(subcategory_id=sm[0].id, p_type=se1)
            print(se_pro)
            return render(
                request,
                "baby.html",
                {
                    "prod": prod,
                    "se_pro": se_pro,
                },
            )

        elif "price1" in request.POST:
            min1 = request.POST["min"]
            max1 = request.POST["max"]
            print(min1)
            print(max1)
            price_pro = products.objects.filter(
                subcategory_id=sm[0].id, price__range=(int(min1), int(max1))
            )
            print(price_pro)
            return render(
                request,
                "baby.html",
                {
                    "prod": prod,
                    "price_pro": price_pro,
                },
            )
        else:
            pass
    return render(request, "baby.html", {"prod": prod})


def sdetail(request, id):
    if "is_logged" in request.session:

        product = products.objects.get(id=id)
        name = product.product_name
        price = product.price
        cat = product.category
        desc = product.desc

        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        type1 = product.p_type
        img1 = product.image
        product = products.objects.get(id=id)
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        user = Register.objects.get(eadd=request.session["is_logged"])
        # visit page
        his = history.objects.filter(user_id=user.id, product_id_id=product.id)
        his = history(
            user_id=user.id,
            product_id_id=product.id,
            product_name=product.product_name,
            price=product.price,
            desc=product.desc,
        )
        his.save()
        print("done")
        total_all = price

        total_all_r = total_all * 100

        if request.method == "POST":
            q1 = request.POST["quantity"]
            q1 = int(q1)
            print(q1)
            if "is_logged" in request.session:
                print(request.session["is_logged"])
                product = products.objects.get(id=id)
                user = Register.objects.get(eadd=request.session["is_logged"])
                print(user.id)

                cart = carts.objects.filter(user_id=user.id, product_id_id=product.id)
                count = carts.objects.filter(
                    user_id=user.id, product_id_id=product.id
                ).count()

                if count > 0:
                    cart = carts.objects.filter(
                        user_id=user.id, product_id_id=product.id
                    )
                    qty = q1
                    t_price = qty * round(product.price, 2)
                    carts.objects.filter(
                        user_id=user.id, product_id_id=product.id
                    ).update(quantity=qty, price=t_price)
                    return redirect("cart")

                else:
                    print("@@@@@@", user.id)
                    cart = carts(
                        user_id=user.id,
                        product_id_id=product.id,
                        quantity=q1,
                        price=product.price * q1,
                    )

                    cart.save()
                    return redirect("cart")
            else:
                return redirect("login")

        return render(
            request,
            "shop-detail.html",
            {
                "name": name,
                "total_all_r": total_all_r,
                "price": price,
                "count": count,
                "img1": img1,
                "cat": cat,
                "desc": desc,
                "type1": type1,
            },
        )
    else:
        product = products.objects.get(id=id)
        name = product.product_name
        price = product.price
        cat = product.category
        desc = product.desc

        type1 = product.p_type
        type1 = product.p_type
        img1 = product.image
        product = products.objects.get(id=id)

        return render(
            request,
            "shop-detail.html",
            {
                "name": name,
                "price": price,
                "img1": img1,
                "cat": cat,
                "desc": desc,
                "type1": type1,
            },
        )
    # return render(request, "shop-detail.html")


def add_cart(request, id):
    context = {}
    if "is_logged" in request.session:
        print(request.session["is_logged"])
        product = products.objects.get(id=id)
        user = Register.objects.get(eadd=request.session["is_logged"])
        print(user.id)

        cart = carts.objects.filter(user_id=user.id, product_id_id=product.id)
        count = carts.objects.filter(user_id=user.id, product_id_id=product.id).count()

        if count > 0:
            cart = carts.objects.filter(user_id=user.id, product_id_id=product.id)
            qty = cart[0].quantity + 1
            t_price = qty * product.price
            carts.objects.filter(user_id=user.id, product_id_id=product.id).update(
                quantity=qty, price=t_price
            )
            return redirect("cart")

        else:
            print("@@@@@@", user.id)
            cart = carts(
                user_id=user.id,
                product_id_id=product.id,
                quantity=1,
                price=product.price,
            )
            cart.save()
            return redirect("cart")
    else:
        return redirect("notlogin")


def cart(request):
    if "is_logged" in request.session:
        user = Register.objects.get(eadd=request.session["is_logged"])
        print(user)

        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        img = r1.image
        cart = carts.objects.filter(user__id=user.id)
        count = carts.objects.filter(user__id=user.id).count()
        data = serializers.serialize("json", cart)

        all_prod = []
        totalprice = []
        q1 = 0

        for i in cart:

            totalprice.append(i.price)
            q1 = int(i.quantity)
            product = products.objects.filter(id=i.product_id_id)

            all_prod.extend(product)

        total = sum(totalprice)
        dis = total - ((total * 10) / 100)
        gst = (total * 2) / 100
        total_all = round(dis + gst, 2)
        print(total)

        cart1 = zip(all_prod, cart)
        return render(
            request,
            "cart.html",
            {
                "q1": q1,
                "cart": cart1,
                "count": count,
                "total": total,
                "total_all": total_all,
                "data": data,
                "img": img,
            },
        )
    else:
        return redirect("notlogin")


def dele(request, id):
    if "is_logged" in request.session:
        product = products.objects.get(id=id)
        user = Register.objects.get(eadd=request.session["is_logged"])
        cart = carts.objects.filter(user_id=user.id, product_id=product.id)

        del cart
        carts.objects.filter(user_id=user.id, product_id=product.id).delete()
        return redirect("cart")
    return render(request, "cart.html")


def add_wishlist(request, id):
    if "is_logged" in request.session:

        print(request.session["is_logged"])
        product = products.objects.get(id=id)
        user = Register.objects.get(eadd=request.session["is_logged"])
        print(user.id)

        wishlist = wishlists.objects.filter(user_id=user.id, product_id_id=product.id)
        count = wishlists.objects.filter(
            user_id=user.id, product_id_id=product.id
        ).count()

        if count > 0:
            wishlist = wishlists.objects.filter(
                user_id=user.id, product_id_id=product.id
            )
            qty = wishlist[0].quantity + 1
            t_price = qty * product.price
            wishlists.objects.filter(user_id=user.id, product_id_id=product.id).update(
                quantity=qty, price=t_price
            )
            return redirect(request.META["HTTP_REFERER"])

        else:
            print("@@@@@@", user.id)
            wishlist = wishlists(
                user_id=user.id,
                product_id_id=product.id,
                quantity=1,
                price=product.price,
            )
            wishlist.save()
            return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("notlogin")


def wishlist(request):
    if "is_logged" in request.session:
        user = Register.objects.get(eadd=request.session["is_logged"])
        print(user)

        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        img = r1.image
        wishlist = wishlists.objects.filter(user__id=user.id)
        count = wishlists.objects.filter(user__id=user.id).count()
        data = serializers.serialize("json", wishlist)

        all_prod = []
        q1 = 0

        for i in wishlist:

            q1 = int(i.quantity)
            product = products.objects.filter(id=i.product_id_id)

            all_prod.extend(product)

        wishlist1 = zip(all_prod, wishlist)
        return render(
            request,
            "wishlist.html",
            {
                "q1": q1,
                "wishlist": wishlist1,
                "count": count,
                "data": data,
                "img": img,
            },
        )
    else:
        return redirect("notlogin")


def dele_wish(request, id):
    if "is_logged" in request.session:
        product = products.objects.get(id=id)
        user = Register.objects.get(eadd=request.session["is_logged"])
        wishlist = wishlists.objects.filter(user_id=user.id, product_id=product.id)

        del wishlist
        wishlists.objects.filter(user_id=user.id, product_id=product.id).delete()
        return redirect("wishlist")
    return render(request, "wishlist.html")


def history11(request):
    if "is_logged" in request.session:
        user = Register.objects.get(eadd=request.session["is_logged"])
        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        img = r1.image
        data = history.objects.filter(user_id=user.id)
        count = history.objects.filter(user__id=user.id).count()

        return render(
            request,
            "history.html",
            {"data": data, "count": count, "img": img},
        )
    else:
        return redirect("notlogin")


def dele_his(request, id):
    if "is_logged" in request.session:
        his = history.objects.filter(id=id)

        del his
        history.objects.filter(id=id).delete()
        return redirect("history")
    return render(request, "history.html")


def Contact(request):
    con = {}
    if "is_logged" in request.session:
        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        con["user"] = user
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        con["count"] = count
        img = r1.image
        con["img"] = img

        if request.method == "POST":
            name = request.POST["name"]
            email = request.POST["email"]
            subject = request.POST["subject"]
            message = request.POST["message"]

            valid = contact(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            valid.save()
        return render(request, "contact-us.html", con)
    return render(request, "contact-us.html", con)


def shop(request):
    return render(request, "shop.html")


def account(request):
    return render(request, "my-account.html")


def service(request):
    con = {}
    if "is_logged" in request.session:
        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        user = r1.fname
        con["user"] = user
        cart = carts.objects.filter(user__id=r1.id)
        count = cart.count()
        con["count"] = count
        img = r1.image
        con["img"] = img
    else:
        pass
    return render(request, "service.html", con)


otp_v = []


def test(request):
    return render(request, "test.html")


a = []


def resetpass(request):
    if "is_logged" in request.session:
        if request.method == "POST":
            if "email1" in request.POST:
                otp_user = random.randint(1000, 9999)
                a.append(otp_user)
                print(otp_user)
                e1 = request.POST.get("email")
                if Register.objects.filter(eadd=e1):
                    msg = EmailMultiAlternatives(
                        f"otp from msm app", f"{otp_user}", EMAIL_HOST_USER, [f"{e1}"]
                    )
                    msg.send()
                    return render(request, "reset_pass.html", {"otp": otp_user})
                else:
                    not_user = "not user match"
                    return render(request, "reset_pass.html", {"not_user": not_user})

        if "otp1" in request.POST:
            print(a)
            print(a[-1])
            o1 = request.POST["otp"]
            if int(a[-1]) == int(o1):
                print("done")
                msg = "done"
                return render(request, "reset_pass.html", {"msg": msg})
            else:
                print("error")
                msg = "Error Please Enter Valid OTP !!(Agian Enter Email)"
                return render(request, "reset_pass.html", {"msg": msg})

        if "change" in request.POST:
            e11 = request.POST["e1"]
            c11 = request.POST["c1"]
            if Register.objects.filter(eadd=e11):
                valid = Register.objects.get(eadd=e11)
                Register.objects.filter(eadd=e11).update(password=c11)
                done = "PASSWORD CHANGES SUCCESFULLY !!!!"
                return render(request, "reset_pass.html", {"done": done})
            else:
                done = "Not Change A Password!! Please Valid Email.."
                return render(request, "reset_pass.html", {"done": done})

        return render(request, "reset_pass.html")
    return redirect("notlogin")


class ChangePassword(View):
    def get(self, request):
        return render(request, "change_password.html")

    def post(self, request):
        context = {}
        old_pass = request.POST["old_pass"]
        new_pass = request.POST["new_pass"]
        print(request.session["is_logged"])
        user = Register.objects.get(eadd=request.session["is_logged"])
        if user:
            user.password = new_pass
            user.save()
            context["msg"] = "Password Changes succesFully !!!!"
        else:
            context["error"] = "Incurrect Old Password !!!!"
        return render(request, "change_password.html", context)


# auth code close
def usernot(request):
    return render(request, "ar.html")


def notlogin(request):
    return render(request, "un.html")


def ordernot(request):
    return render(request, "ordernot.html")


def orders(request):
    if "is_logged" in request.session:
        user = Register.objects.get(eadd=request.session["is_logged"])
        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        img = r1.image
        cart = carts.objects.filter(user__id=user.id)
        aa = []
        bb = []
        cc = []
        all_prod = []
        for i in cart:
            product = products.objects.filter(id=i.product_id_id)
            all_prod.extend(product)
        if payment1.objects.filter(user__id=user.id):
            cc = payment1.objects.filter(user__id=user.id).count()
            cc = cc - 1
            qq = payment1.objects.filter(user__id=user.id)[cc]
            aa = qq.product_names
            aa = aa.split(",")
            print(type(aa))
            bb = qq.product_price
            bb = bb.split(",")
            print(type(bb))
            cc = qq.product_qun
            cc = cc.split(",")
            print(type(cc))
            dd = str(qq.status)
            ee = qq.total

            cart1 = zip(aa, bb, cc, all_prod)

            return render(
                request, "order.html", {"data": cart1, "s": dd, "total": ee, "img": img}
            )
        else:
            return render(request, "ordernot.html")

    else:
        return redirect("notlogin")
    return render(request, "order.html")


# def outer(request):
#     cart = carts.objects.get(id=48)
#     print(cart.product_id)
#     print(cart.quantity)

#     print(cart.price)

#     return render(request, "base.html")


def outer_add_cart(request, id):
    if "is_logged" in request.session:
        if request.method == "POST":
            q1 = request.POST.get("quantity")
            q1 = int(q1)
            print(f"{q1}`````")
            print(id)

            product = products.objects.get(id=id)
            user = Register.objects.get(eadd=request.session["is_logged"])
            print("==============================================")
            print(user.id)

            cart = carts.objects.filter(user_id=user.id, product_id_id=product.id)
            qty = q1
            t_price = qty * product.price
            carts.objects.filter(user_id=user.id, product_id_id=product.id).update(
                quantity=qty, price=t_price
            )
            return redirect("cart")


def checkout1(request):

    customer_name = request.session.get("is_logged")
    print()
    if request.method == "POST":
        fname1 = request.POST["fname"]
        lname1 = request.POST["lname"]
        eadd1 = request.POST["eadd"]
        cnumber1 = request.POST["cnumber"]
        address1 = request.POST["address"]
        country1 = request.POST["country"]
        city1 = request.POST["city"]

        valid = checkout(
            fname=fname1,
            lname=lname1,
            eadd=eadd1,
            cnumber=cnumber1,
            address=address1,
            country=country1,
            city=city1,
        )
        valid.save()

    r1 = Register.objects.get(eadd=customer_name)
    fname = r1.fname
    lname = r1.lname
    add = r1.address

    img = r1.image
    user = Register.objects.get(eadd=request.session["is_logged"])
    print(user.id)

    cart = carts.objects.filter(user__id=user.id)
    count = carts.objects.filter(user__id=user.id).count()
    data = serializers.serialize("json", cart)

    all_prod = []
    totalprice = []
    q1 = 0
    for i in cart:

        totalprice.append(i.price)
        q1 = int(i.quantity)
        product = products.objects.filter(id=i.product_id_id)

        all_prod.extend(product)

    total = sum(totalprice)
    dis = total - ((total * 10) / 100)
    gst = (total * 2) / 100
    total_all = int(round(dis + gst, 2))

    total_all_r = total_all * 100

    ed = checkout.objects.all()

    # move data on order
    c1 = carts.objects.filter(user__id=user.id)
    form = checkout(request.POST)

    return render(
        request,
        "checkout.html",
        {
            "fname": fname,
            "lname": lname,
            "count": count,
            "total": total,
            "total_all": total_all,
            "data": data,
            "img": img,
            "from": form,
        },
    )


def payment(request):
    if "is_logged" in request.session:
        customer_name = request.session.get("is_logged")
        print()
        if request.method == "POST":
            fname1 = request.POST["fname"]
            lname1 = request.POST["lname"]
            eadd1 = request.POST["eadd"]
            cnumber1 = request.POST["cnumber"]
            address1 = request.POST["address"]
            country1 = request.POST["country"]
            city1 = request.POST["city"]

            valid = checkout(
                fname=fname1,
                lname=lname1,
                eadd=eadd1,
                cnumber=cnumber1,
                address=address1,
                country=country1,
                city=city1,
            )
            valid.save()
        customer_name = request.session.get("is_logged")
        r1 = Register.objects.get(eadd=customer_name)
        fname = r1.fname
        lname = r1.lname
        add = r1.address

        img = r1.image
        user = Register.objects.get(eadd=request.session["is_logged"])
        print(user.id)

        cart = carts.objects.filter(user__id=user.id)
        count = carts.objects.filter(user__id=user.id).count()
        data = serializers.serialize("json", cart)

        all_prod = []
        totalprice = []
        q1 = 0
        for i in cart:
            totalprice.append(i.price)
            q1 = int(i.quantity)
            product = products.objects.filter(id=i.product_id_id)
            all_prod.extend(product)

        total = sum(totalprice)
        dis = total - ((total * 10) / 100)
        gst = (total * 2) / 100
        total_all = int(round(dis + gst, 2))

        total_all_r = total_all * 100

        print(payment)
        cart1 = zip(all_prod, cart)
        ed = checkout.objects.all()

    return render(
        request,
        "payment.html",
        {
            "rz": total_all_r,
            "q1": q1,
            "cart": cart1,
            "add": add,
            "fname": fname,
            "lname": lname,
            "count": count,
            "total": total,
            "total_all": total_all,
            "data": data,
            "img": img,
        },
    )


def p1(request):
    customer_name = request.session.get("is_logged")
    r1 = Register.objects.get(eadd=customer_name)
    fname = r1.fname
    lname = r1.lname
    add = r1.address

    img = r1.image
    user = Register.objects.get(eadd=request.session["is_logged"])
    print(user.id)

    cart = carts.objects.filter(user__id=user.id)
    count = carts.objects.filter(user__id=user.id).count()

    all_prod = []
    totalprice = []
    q1 = 0
    for i in cart:
        totalprice.append(i.price)
        q1 = int(i.quantity)
        product = products.objects.filter(id=i.product_id_id)
        all_prod.extend(product)

    total = sum(totalprice)
    dis = total - ((total * 10) / 100)
    gst = (total * 2) / 100
    total_all = int(round(dis + gst, 2))

    total_all_r = total_all * 100

    x = "order_"
    order_receipt = x + str(user.id) + str(total_all)
    client = razorpay.Client(
        auth=("rzp_test_FLbN0nWF4Pn79H", "hlRS6JkcnNPh6zEAotqWH2s7")
    )
    payment = client.order.create(
        {
            "amount": total_all,
            "currency": "INR",
            "receipt": order_receipt,
            "payment_capture": "0",
        }
    )

    # add order

    product_names = []
    product_price_i = []
    product_price_s = []
    product_qun = []
    total = []
    for i in cart:
        product_price_s.append(str(i.price))

    for i in cart:
        product_price_i.append(i.price)
        product_qun.append(str(i.quantity))
        product = products.objects.filter(id=i.product_id_id)
        product_names.extend(product)

    total = sum(product_price_i)
    x1 = "order_"
    recipt = x1 + str(total) + str(user.id)

    # convert string
    pn_str = ""
    pp = ",".join(product_price_s)
    pq = ",".join(product_qun)

    for i in cart:
        product = products.objects.filter(id=i.product_id_id)
        for i in product:
            p = str(i) + ","
            pn_str += p
    print(pn_str)
    print(pp)
    print(pq)
    print("---------done")
    if not payment1.objects.filter(user__id=user.id, recipt=recipt):
        z1 = payment1(
            user_id=user.id,
            product_names=pn_str,
            product_price=pp,
            product_qun=pq,
            total=total_all,
            recipt=recipt,
        )
        z1.save()
    return render(request, "test.html")


def profile(request):
    if "is_logged" in request.session:
        print(request.session["is_logged"])
        data = Register.objects.get(eadd=request.session["is_logged"])
        print(data)

    else:
        return redirect("/notlogin")
    return render(request, "profile.html", {"data": data})


def editProfile(request, id):
    data = Register.objects.get(pk=id)
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        eadd = request.POST["eadd"]
        cnumber = request.POST["cnumber"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        city = request.POST["city"]
        password = request.POST["password"]

        Register.objects.filter(pk=id).update(
            fname=fname,
            lname=lname,
            eadd=eadd,
            cnumber=cnumber,
            dob=dob,
            gender=gender,
            address=address,
            pincode=pincode,
            city=city,
            password=password,
        )
        return redirect("/profile")

    return render(request, "editprofile.html", {"data": data})


def feedback1(request):
    if request.method == "POST":
        fname1 = request.POST["name"]
        lname1 = request.POST["email"]
        eadd1 = request.POST["subject"]
        cnumber1 = request.POST["msg"]

        c = feedback(
            name=fname1,
            email=lname1,
            subject=eadd1,
            message=cnumber1,
        )
        c.save()
    return render(request, "feedback.html")


def buy(request):
    if "is_logged" in request.session:
        print(request.session["is_logged"])

        user = Register.objects.get(eadd=request.session["is_logged"])
        print(user.id)
        p = 900

        total_all = p * 100

        client = razorpay.Client(
            auth=("rzp_test_FLbN0nWF4Pn79H", "hlRS6JkcnNPh6zEAotqWH2s7")
        )
        payment = client.order.create(
            {
                "amount": p,
                "currency": "INR",
                "payment_capture": "0",
            }
        )
        return redirect("stdetail")


# urls and msmapp urls(optional)
# pdf1.html
# customer.html
# mathfilter install, add settings ,and import html file
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
from io import BytesIO
import datetime


class CustomerListView(ListView):
    model = payment1
    template_name = "test.html"


def customer_render(request, *args, **kwargs):
    template_path = "invoice.html"
    # data-created
    all_prod = []
    user = Register.objects.get(eadd=request.session["is_logged"])

    cart = carts.objects.filter(user__id=user.id)
    for i in cart:
        product = products.objects.filter(id=i.product_id_id)
        all_prod.extend(product)
    if payment1.objects.filter(user__id=user.id):

        user1 = Register.objects.get(eadd=request.session["is_logged"])
        name1 = user1.fname
        add1 = user1.address

        cc = payment1.objects.filter(user__id=user.id).count()
        cc = cc - 1
        qq = payment1.objects.filter(user__id=user.id)[cc]
        aa = qq.product_names
        aa = aa.split(",")
        print(type(aa))
        bb = qq.product_price
        bb = bb.split(",")
        print(type(bb))
        cc = qq.product_qun
        cc = cc.split(",")
        print(type(cc))
        dd = str(qq.status)
        print(dd)
        # ee = str(qq.product_img)
        # ee = ee.split(",")
        # print(ee)
        total = qq.total
        r = qq.recipt
        now = datetime.datetime.now()
        date1 = now.strftime("%Y-%m-%d %H:%M:%S")
        cart1 = zip(aa, bb, cc, all_prod)
    context = {
        "data": cart1,
        "total": total,
        "r": r,
        "date": date1,
        "name": name1,
        "add": add1,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Mihira_reciept_101.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


# def payment_m(request):
#     amount = {{total_all}}
#     mobile = "tinu1316@gmail.com"
#     client = razorpay.Client(
#         auth=("rzp_test_FLbN0nWF4Pn79H", "hlRS6JkcnNPh6zEAotqWH2s7")
#     )
#     payment = client.order.create(
#         {"amount": amount, "currency": "INR", "payment_capture": "total_all"}
#     )
#     return render(request, "success.html", {"total": amount, "mobile": mobile})
