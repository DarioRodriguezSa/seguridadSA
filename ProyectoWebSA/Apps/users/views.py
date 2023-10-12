from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Userdate, Pago
from django.contrib.auth.hashers import make_password
import datetime


@login_required(login_url="/accounts/login/")
def UsersListView(request):
    users = User.objects.exclude(id=1)
    userdata_list = Userdate.objects.filter(user__in=users)

    context = {
        "active_icon": "users",
        "users_with_data": zip(users, userdata_list),
    }
    return render(request, "users/users.html", context=context)

@login_required(login_url="/accounts/login/")
def UsersAddView(request):
    context = {
        "active_icon": "users",
    }
    if request.method == 'POST':
        data = request.POST
        attributes = {
            "username": data['first_name'],
            "email": data['email'],
            "password": make_password(data['password']),
        }
        if User.objects.filter(**attributes).exists():
            messages.error(request, '¡El usuario ya existe!',
                extra_tags="warning")
            return redirect('Apps.users:users_add')
        try:
            new_users = User.objects.create(**attributes)
            new_users.save()

            Userdate.objects.create(user=new_users, address=data['address'], phone =  data['phone'],debts=0)
            messages.success(request, '¡usario: ' + attributes["username"] + " " + ' Creado con éxito!', extra_tags="success")
            return redirect('Apps.users:users_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la creación!'+ str(e), extra_tags="danger")
            return redirect('Apps.users:users_add')
    return render(request, "users/users_add.html", context=context)

@login_required(login_url="/accounts/login/")
def UsersDeleteView(request, user_id):
    try:
        userdata = Userdate.objects.filter(user=user_id).first()
        if userdata:
            project = userdata.project
            if project is None: 
                userdata.delete()
                user = User.objects.filter(id=user_id)
                user.delete()
                messages.success(request, '¡Usuario Eliminado!', extra_tags="success")
            else:
                messages.error(
                    request, '¡Hubo un error durante la eliminación ya que está asignado a un proyecto!', extra_tags="danger")
        else:
            messages.error(request, 'No se encontraron datos de Userdate para este usuario.', extra_tags="danger")
        return redirect('Apps.users:users_list')
    except Exception as e:
        messages.error(request, 'Hubo un error durante la eliminación:', extra_tags="danger")
        return redirect('Apps.users:users_list')


@login_required(login_url="/accounts/login/")
def UsersUpdateView(request, user_id,userdate_id):
    try:
        userdata = Userdate.objects.filter(id=userdate_id).first()
        user = User.objects.filter(id=user_id).first()
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al intentar conseguir al usuario!', extra_tags="danger")
        return redirect('Apps.users:users_list')
    context = {
        "active_icon": "users",
        "user": user,
        "userdata": userdata,
    }
    if request.method == 'POST':
        try:
            data = request.POST
            attributes = {
                "address": data['address'],
                "phone": data['phone'],
            }
            atrributer ={
                "username": data['first_name'],
                "email": data['email'],
            }
            Userdate.objects.filter(id=userdate_id).update(**attributes)
            user=User.objects.filter(id=user_id).update(**atrributer)
            user2 = User.objects.filter(id=user_id).first()
            messages.success(request, '¡Usuario: ' + user2.username +
                ' actualizado exitosamente!', extra_tags="success")
            return redirect('Apps.users:users_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la actualización! ' + str(e), extra_tags="danger")
            
            return redirect('Apps.users:users_list')
    return render(request, "users/users_update.html", context=context)



@login_required(login_url="/accounts/login/")
def UsersPayView(request, user_id,userdate_id):
    try:
        userdata = Userdate.objects.filter(id=userdate_id).first()
        user = User.objects.filter(id=user_id).first()
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al intentar conseguir al usuario!', extra_tags="danger")
        return redirect('Apps.users:users_list')
    context = {
        "active_icon": "users",
        "user": user,
        "userdata": userdata,
    }
    if request.method == 'POST':
        try:
            data = request.POST
            fecha_actual = datetime.date.today()
            attributes ={
                "fecha": fecha_actual,
                "monto":data['bet'],
                "usuario": data['first_name'], 
                "proyecto": data['project'],
            }

            new_register = Pago.objects.create(**attributes)
            new_register.save()
            Userdate.objects.filter(id=userdate_id).update(debts=0)

            messages.success(request, '¡Pago aceptado exitosamente!', extra_tags="success")
            return redirect('Apps.users:users_list')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante el pago! ' + str(e), extra_tags="danger")
            return redirect('Apps.users:users_list')
    return render(request, "users/users_pay.html", context=context)

@login_required(login_url="/accounts/login/")
def PayListView(request):
    pago = Pago.objects.all()
    context = {
        "active_icon": "pays",
        "pagos": pago,
    }
    return render(request, "users/Pagos.html", context=context)