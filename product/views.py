from django.shortcuts import render, redirect
from .models import Product
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    pg = request.GET.get("page", 1)
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")

    if kw:
        if cate == "sub":
            b = Product.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Product.objects.filter(writer=u)
            except:
                b = Product.objects.none()
        elif cate == "con":
            b = Product.objects.filter(content__contains=kw)
        else:
            b = Product.objects.none()
    else:
        b = Product.objects.all()

    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context = {
        "bset": obj,
        "cate": cate,
        "kw": kw,
        "b": b
    }
    return render(request, "product/index.html", context)




def update(request, bpk):
    b = Product.objects.get(id=bpk)

    if b.writer != request.user:
        return redirect("product:index")

    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("product:detail", bpk)
    context = {
        "b":b
    }
    return render(request, "product/update.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        pi = request.FILES.get("pic")
        Product(subject=s, content=c, picture=pi,
        writer=request.user, pubdate=timezone.now()).save()
        print(Product.objects.all())
        return redirect("product:index")
    return render(request, "product/create.html")

def delete(request, bpk):
    b = Product.objects.get(id=bpk)
    if request.user == b.writer:        
        b.picture.delete()
        b.delete()
    else:
        pass 
    return redirect("product:index")

def detail(request, bpk):
    b = Product.objects.get(id=bpk)
    # r = b.reply_set.all()
    context = {
        "b": b,
        # "rset" : r
    }
    return render(request, "product/detail.html", context )


# def dreply(request, bpk, rpk):
#     r = Reply.objects.get(id=rpk)
#     if r.replyer == request.user:
#         r.delete()
#     else:
#         pass 
#     return redirect("product:detail", bpk)


# def creply(request, bpk):
#     b = Product.objects.get(id=bpk)
#     c = request.POST.get("com")
#     Reply(board=b, replyer=request.user, comment=c).save()
#     return redirect("product:detail", bpk)

