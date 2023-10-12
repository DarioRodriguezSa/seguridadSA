from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Project
from django.contrib.auth.models import User
from Apps.users.models import Userdate

@login_required(login_url="/accounts/login/")
def ProjectsListView(request):
    projects = Project.objects.prefetch_related('users__user')
    context = {
        "active_icon": "projects",
        "projects": projects
    }
    return render(request, "projects/projects.html", context=context)


@login_required(login_url="/accounts/login/")
def ProjectsAddView(request):
    users= User.objects.filter(userdate__project__isnull=True).exclude(id=1)

    context = {
        "active_icon": "projects",
        "users": users,
    }

    if request.method == 'POST':
        data = request.POST
        selected_users = request.POST.getlist('selected_users')
        costo_proyecto = float(data.get('cost', 0))
        cantidad= len(selected_users)

        attributes = {
            "nombre": data['name_P'],
            "ubicacion": data['ubicacion_direccion'] + ", " + data['ubicacion_ciudad'] + ", " +  data['ubicacion_estado'],
            "fecha_inicio": data['start_date'],
            "fecha_finalizacion_estimada": data['end_date'],
            "costo": costo_proyecto,
            "user_total":  cantidad,
        }

        if Project.objects.filter(**attributes).exists():
            messages.error(request, '¡El proyecto ya existe!', extra_tags="warning")
            return redirect('Apps.projects:projects_add')

        try:
            new_project = Project.objects.create(**attributes)
            
            for user_id in selected_users:
                user = User.objects.get(id=user_id)
                
                # Obtén el objeto Userdate relacionado con el usuario
                userdate, created = Userdate.objects.get_or_create(user=user)
                
                # Realiza las modificaciones en Userdate
                userdate.debts += costo_proyecto
                userdate.project = new_project
                userdate.save()
                
                # Actualiza el objeto User
                user.save()
                        
            messages.success(request, '¡Proyecto Creado con éxito!', extra_tags="success")
            return redirect('Apps.projects:projects_list')
        except Exception as e:
            messages.error(request, '¡Hubo un error durante la creación! ' + str(e), extra_tags="danger")
            return redirect('Apps.projects:projects_add')

    return render(request, "projects/projects_add.html", context=context)

def ProjectsDeleteView(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        
        for userdate in project.users.all():
            # Quita la referencia al proyecto en la columna 'project' de Userdate
            userdate.project = None
            userdate.debts = 0
            userdate.save()

        # Ahora puedes eliminar el proyecto
        project.delete()

        messages.success(request, '¡Proyecto: ' + project.nombre + ' Eliminado!', extra_tags="success")
        return redirect('Apps.projects:projects_list')
    except Exception as e:
        messages.success(request, '¡Hubo un error durante la eliminación!' + str(e), extra_tags="danger")
        return redirect('Apps.projects:projects_list')

@login_required(login_url="/accounts/login/")
def ProjectsUpdateView(request, project_id):
    try:
        users = User.objects.filter(userdate__project__isnull=True).exclude(id=1)
        project = Project.objects.get(id=project_id)
        assigned_users = Userdate.objects.filter(project=project)
    except Exception as e:
        messages.success(request, '¡Hubo un error al intentar conseguir el proyecto!', extra_tags="danger")
        return redirect('Apps.projects:projects_list')

    context = {
        "active_icon": "projects",
        "project": project,
        "assigned_users": assigned_users,
        "users": users,
    }

    if request.method == 'POST':
        try:
            data = request.POST
            cantidad_user = 0.0  # Initialize cantidad_user as a float

            # Procesar la eliminación de usuarios
            users_to_remove = request.POST.getlist('users_to_remove')
            cantidad_user = len(users_to_remove)
            cantidad_user =  float(data.get('cantidad', 0))-  cantidad_user# Subtract
            for user_id in users_to_remove:
                userdate = Userdate.objects.get(id=user_id)
                userdate.project = None
                userdate.debts = 0
                userdate.save()
            # Procesar la adición de usuarios
            users_to_add = request.POST.getlist('users_to_add')
            cantidad = len(users_to_add)
            cantidad_user  +=cantidad # Add
            print(cantidad_user)

            for user_id in users_to_add:
                user = User.objects.get(id=user_id)
                userdate, _ = Userdate.objects.get_or_create(user=user)
                userdate.project = project  # Assign the Project instance
                userdate.debts = float(data.get('cost', 0))
                userdate.save()

            attributes = {
                "nombre": data['name_P'],
                "ubicacion": data['ubicacion_ciudad'],
                "fecha_inicio": data['start_date'],
                "fecha_finalizacion_estimada": data['end_date'],
                "costo": data['cost'],
                "user_total": cantidad_user,  # Include the updated cantidad_user
            }

            # Actualizar el proyecto
            Project.objects.filter(id=project_id).update(**attributes)
            project = Project.objects.get(id=project_id)

            messages.success(request, '¡Proyecto: ' + project.nombre + ' actualizado exitosamente!', extra_tags="success")
            return redirect('Apps.projects:projects_list')
        except Exception as e:
            messages.success(request, '¡Hubo un error durante la actualización! ' + str(e), extra_tags="danger")
            return redirect('Apps.projects:projects_list')

    return render(request, "projects/projects_update.html", context=context)