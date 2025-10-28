from django.urls import path
from . import views

app_name = 'notes'  # this is key

urlpatterns = [
    path('', views.note_list_view, name='note_list'),
    path('create/', views.note_create, name='note_create'),
    path('edit/<int:pk>/', views.note_edit, name='note_edit'),
    path('delete/<int:pk>/', views.note_delete, name='note_delete'),
    path('restore/<int:pk>/', views.note_restore, name='note_restore'),
    path('recycle/', views.recycle_bin, name='recycle_bin'),
    path('pin/<int:pk>/', views.pin_toggle, name='pin_toggle'),
    path('autosave/<int:pk>/', views.autosave, name='autosave'),
    path('note/<int:pk>/', views.note_view, name='note_view'),
    path('upload-image/', views.upload_image, name='upload_image'),
]
