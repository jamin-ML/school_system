from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #---------home page url
    path('',views.home ,name='home'),
    #---------Materials page url
    path('materials/',views.materials,name='materials'),
    path('materials/<int:subject_id>/', views.materials_by_subject, name='materials_by_subject'),
    path('materials/<int:material_id>/', views.material_detail, name='material_detail'),
    path('mark-complete/<int:material_id>/', views.mark_material_complete, name='mark_complete'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('resource/<int:resource_id>/',views.view_resource, name='view_resource'),
    path('upload/', login_required(views.upload_resource), name='upload_resource'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)