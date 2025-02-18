from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MemberRegisterForm, InstructorForm, ClassForm, GroupForm, CalendarForm, InstructorForm1
from .models import Member, Instructor, Tclass, Grupo
from django.http import JsonResponse

@login_required
def register_member(request):
    if hasattr(request.user, 'member'):
        return redirect('update_member')
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            return redirect('home')
    else:
        form = MemberRegisterForm()
    return render(request, 'members/register_member.html', {'form': form})

@login_required
def update_member(request):
    member = get_object_or_404(Member, user=request.user)
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MemberRegisterForm(instance=member)
    return render(request, 'members/update_member.html', {'form': form, 'member': member})

@login_required
def update_member_admin(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('list_members')
    else:
        form = MemberRegisterForm(instance=member)
    return render(request, 'members/update_member_admin.html', {'form': form, 'member': member})

@login_required
def list_members(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    members = Member.objects.all()
    return render(request, 'members/list_members.html', {'members': members})



@login_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        member.delete()
        return redirect('list_members')
    return render(request, 'members/confirm_delete.html', {'member': member})

@login_required
def list_instructors(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    instructors = Instructor.objects.all()
    return render(request, 'members/list_instructor.html', {'instructors': instructors})


@login_required
def create_instructor(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_instructors')  # Redirige a la lista de instructores
    else:
        form = InstructorForm()

    return render(request, 'members/create_instructor.html', {'form': form})

@login_required
def update_instructor(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    if request.method == 'POST':
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('list_instructors')
    else:
        form = InstructorForm(instance=instructor)
    return render(request, 'members/update_instructor.html', {'form': form, 'instructor': instructor})


@login_required
def list_classes(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    classes = Tclass.objects.all()
    return render(request, 'members/list_class.html', {'classes': classes})


@login_required
def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            nueva_clase = form.save(commit=False)  # commit=False es clave
            nueva_clase.creo = request.user
            nueva_clase.save()
            return redirect('list_classes')  # Redirige a la lista de clases
    else:
        form = ClassForm()

    return render(request, 'members/create_class.html', {'form': form})

@login_required
def update_class(request, id):
    classe = get_object_or_404(Tclass, id=id)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            return redirect('list_classes')
    else:
        form = ClassForm(instance=classe)
    return render(request, 'members/update_class.html', {'form': form, 'classe': classe})


@login_required
def list_group(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    groups = Grupo.objects.all()
    return render(request, 'members/list_group.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            nuevo_grupo = form.save(commit=False)  # commit=False es clave
            nuevo_grupo.creo = request.user
            nuevo_grupo.save()
            return redirect('list_groups')  # Redirige a la lista de clases
    else:
        form = GroupForm()

    return render(request, 'members/create_group.html', {'form': form})

@login_required
def update_group(request, id):
    group = get_object_or_404(Grupo, id=id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('list_groups')
    else:
        form = GroupForm(instance=group)
    return render(request, 'members/update_group.html', {'form': form, 'group': group})

@login_required
def get_tclass_info(request):
    clase_id = request.GET.get('clase_id')
    
    if not clase_id:
        return JsonResponse({'error': 'No se proporcionó clase_id'}, status=400)
    try:
        clase = get_object_or_404(Tclass, id=clase_id)
        return JsonResponse({
            'minimo': clase.minimo,
            'maximo': clase.maximo,
            'duracion': clase.duracion
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def calendar_view(request):
    form = CalendarForm()
    groups = []

    if request.method == 'POST':
        form = CalendarForm(request.POST)
        if form.is_valid():
            instructor = form.cleaned_data['instructor']
            groups = Grupo.objects.filter(instructor=instructor)

    return render(request, 'members/calendar_inst.html', {'form': form, 'groups': groups})

@login_required
def instructor_schedule_view(request):
    form = InstructorForm1()
    schedule = {hour: {day: "" for day in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']} for hour in range(0, 24)}

    if request.method == 'POST':
        form = InstructorForm1(request.POST)
        if form.is_valid():
            instructor = form.cleaned_data['instructor']
            groups = Grupo.objects.filter(instructor=instructor,estatus=True)

            # Rellenar el horario con "X" en las intersecciones
            for group in groups:
                days = group.dias_semana
                print(f'dias_semana: {days}')  # Imprimir el contenido de dias_semana
                start_hour = group.horaInicio.hour
                start_minute = group.horaInicio.minute
                end_hour = group.horaTermino.hour
                end_minute = group.horaTermino.minute

                for day in days:
                    print(f'day: {day}')  # Imprimir el contenido de cada day
                    day_name = day  # Usar directamente el valor de day
                    # Mapeo de abreviaturas a nombres completos de días
                    day_map = {
                        'LU': 'Lunes',
                        'MA': 'Martes',
                        'MI': 'Miércoles',
                        'JU': 'Jueves',
                        'VI': 'Viernes',
                        'SA': 'Sábado',
                        'DO': 'Domingo'
                    }
                    if day_name in day_map:
                        day_name = day_map[day_name]  # Convertir abreviatura a nombre completo

                    for hour in range(start_hour, end_hour + 1):
                        if hour == start_hour:
                            schedule[hour][day_name] = "ocupado"  # Marcar la primera hora completa
                        elif hour == end_hour:
                            if end_minute > 0:
                                schedule[hour][day_name] = "ocupado"  # Marcar la última hora si está parcialmente ocupada
                        else:
                            schedule[hour][day_name] = "ocupado"  # Marcar las horas completas entre la primera y la última

    return render(request, 'members/instructor_schedule.html', {'form': form, 'schedule': schedule})

