from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from .models import Cliente,Movimiento
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.db.models import Sum,Q
from .forms import ClienteForm,MovimientoForm

@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            messages.success(request, 'Cliente agregado correctamente.')
            return redirect('panel')
    else:
        form = ClienteForm()
    return render(request, 'clientes/agregar_cliente.html', {'form': form})

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id, usuario=request.user)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.telefono = request.POST['telefono']
        cliente.email = request.POST['email']
        cliente.direccion = request.POST['direccion']
        cliente.save()
        return redirect('panel')
    return redirect('panel')

@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id, usuario=request.user)
    if request.method == 'POST':
        cliente.delete()
    return redirect('panel')

@login_required
def movimientos_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id, usuario=request.user)
    movimientos = cliente.movimientos.all()
    return render(request, 'clientes/movimientos_cliente.html', {'cliente': cliente, 'movimientos': movimientos})

@login_required
def agregar_movimiento(request, id):
    cliente = get_object_or_404(Cliente, id=id, usuario=request.user)
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.cliente = cliente
            movimiento.save()
            return redirect('movimientos_cliente', id=cliente.id)
    else:
        form = MovimientoForm()
    return render(request, 'clientes/agregar_movimiento.html', {'form': form, 'cliente': cliente})

@login_required
def editar_movimiento(request, id):
    movimiento = get_object_or_404(Movimiento, id=id, cliente__usuario=request.user)
    if request.method == 'POST':
        form = MovimientoForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            return redirect('movimientos_cliente', id=movimiento.cliente.id)
    else:
        form = MovimientoForm(instance=movimiento)
    return render(request, 'clientes/editar_movimiento.html', {'form': form, 'movimiento': movimiento})

@login_required
def eliminar_movimiento(request, id):
    movimiento = get_object_or_404(Movimiento, id=id, cliente__usuario=request.user)
    if request.method == 'POST':
        movimiento.delete()
    return redirect('movimientos_cliente', id=movimiento.cliente.id)

@login_required
def panel(request):
    query = request.GET.get('q')  # Obtener el término de búsqueda
    clientes = Cliente.objects.filter(usuario=request.user)

    if query:
        clientes = clientes.filter(Q(nombre__icontains=query))  # Filtrar por nombre

    total_deudas = Movimiento.objects.filter(cliente__usuario=request.user, estado=False).aggregate(Sum('monto'))['monto__sum'] or 0
    total_pagado = Movimiento.objects.filter(cliente__usuario=request.user, estado=True).aggregate(Sum('monto'))['monto__sum'] or 0

    return render(request, 'clientes/panel.html', {
        'clientes': clientes,
        'total_deudas': total_deudas,
        'total_pagado': total_pagado,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('panel')  # Redirige al panel
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'clientes/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')