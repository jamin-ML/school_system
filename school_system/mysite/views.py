from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .forms import MaterialUploadForm,ResourceUploadForm
from .models import Materials, ClassLevel, Subjects, StudentProgress,TeacherResource


def home(request):
    return render(request,'home.html')

def materials(request):
    all_materials = Materials.objects.all()
    most_viewed = Materials.objects.order_by('-views')[:6]  # top 6 most viewed

    return render(request, 'materials.html', {
        'materials': all_materials,
        'most_viewed': most_viewed,
    })

def materials_by_subject(request, subject_id):
    materials = Materials.objects.filter(subject_id=subject_id)
    subject = get_object_or_404(Subjects, id=subject_id)
    
    return render(request, 'materials_by_subject.html', {
        'materials': materials,
        'subject': subject
    })

#views details 
def material_detail(request, material_id):
    material = get_object_or_404(Materials, id=material_id)
    #increment the views counts
    material.views += 1
    material.save()
    return render(request, 'material_detail.html', {'material': material})


@login_required
def upload_material(request):
    form = MaterialUploadForm()
    if request.method == 'POST':
        form = MaterialUploadForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.teacher = request.user
            material.save()
            return redirect('materials_dashboard')
    return render(request, 'upload_material.html', {'form': form})

def browse_materials(request):
    class_id = request.GET.get('class')
    subject_id = request.GET.get('subject')
    
    classes = ClassLevel.objects.all()
    subjects = Subjects.objects.all()

    materials = Materials.objects.all()
    if class_id:
        materials = materials.filter(class_level_id=class_id)
        subjects = Subjects.objects.filter(class_level_id=class_id)
    if subject_id:
        materials = materials.filter(subject_id=subject_id)

    context = {
        'materials': materials,
        'classes': classes,
        'subjects': subjects,
        'selected_class': class_id,
        'selected_subject': subject_id
    }
    return render(request, 'materials_list.html', context)


@login_required
def study_dashboard(request):
    class_id = request.GET.get('class')
    subject_id = request.GET.get('subject')
    
    classes = ClassLevel.objects.all()
    subjects = Subjects.objects.all()
    materials = Materials.objects.all()

    if class_id:
        materials = materials.filter(class_level_id=class_id)
        subjects = subjects.filter(class_level_id=class_id)

    if subject_id:
        materials = materials.filter(subject_id=subject_id)

    #Get user's progress
    progress = StudentProgress.objects.filter(student=request.user)
    completed_ids = [p.material_id for p in progress if p.completed]

    context = {
        'classes': classes,
        'subjects': subjects,
        'materials': materials,
        'completed_ids': completed_ids,
        'selected_class': class_id,
        'selected_subject': subject_id,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def mark_material_complete(request, material_id):
    material = get_object_or_404(Materials, id=material_id)

    progress, created = StudentProgress.objects.get_or_create(
        student=request.user, material=material
    )
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()

    return JsonResponse({'status': 'ok', 'material_id': material_id})

#--------------------------
# Resource upload views
#--------------------------
def view_resource(request,resource_id):
    resource = get_object_or_404(TeacherResource,id=resource_id)
    return render(request,'resource_detail.html',{'resource':resource})


@login_required
def upload_resource(request):
    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.teacher = request.user
            resource.save()
            return redirect('content_page')
    else:
        form = ResourceUploadForm()
    
    return render(request, 'upload_form.html', {'form': form})