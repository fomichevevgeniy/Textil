from django.shortcuts import render
from materials.models import Material
from .models import MaterialTaked, ClothProductModel, Product, Clients


# Create your views here.

def index(request):
    materials = Material.objects.all()
    materials = materials.order_by('mass')
    materialtakeds = MaterialTaked.objects.all()
    materialtakeds = materialtakeds.order_by('-created_at')
    clothproductmodels = ClothProductModel.objects.all()
    clothproductmodels = clothproductmodels.order_by('-created_at')
    products = Product.objects.all()
    products = products.order_by('-created_at')

    context = {
        'materials': materials[:5],
        'materialtakeds': materialtakeds[:5],
        'clothproductmodels': clothproductmodels[:5],
        'products': products[:5]
    }

    return render(request, 'fabrika/index.html', context)


def sklad(request):
    materials = Material.objects.all()
    materials = materials.order_by('mass')
    context = {
        'materials': materials,
    }

    return render(request, 'fabrika/sklad.html', context)


def vyazka(request):
    materialtakeds = MaterialTaked.objects.all()
    materialtakeds = materialtakeds.order_by('-created_at')
    context = {
        'materialtakeds': materialtakeds,
    }

    return render(request, 'fabrika/vyazka.html', context)


def shitye(request):
    clothproductmodels = ClothProductModel.objects.all()
    clothproductmodels = clothproductmodels.order_by('-created_at')
    context = {
        'clothproductmodels': clothproductmodels,
    }

    return render(request, 'fabrika/shitye.html', context)


def gotovie(request):
    products = Product.objects.all()
    products = products.order_by('-created_at')
    context = {
        'products': products
    }

    return render(request, 'fabrika/gotovie.html', context)


def clienti(request):
    clients = Clients.objects.all()
    clients = clients.order_by('-client_name')
    context = {
        'clients': clients
    }

    return render(request, 'fabrika/clienti.html', context)