from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('spk-prioritas/', views.spk_prioritas, name='spk_prioritas'),
    path('spk-gereja/', views.spk_gereja, name='spk_gereja'),

    path('kecamatan/', views.kecamatan_list, name='kecamatan_list'),
    path('kecamatan/tambah/', views.kecamatan_tambah, name='kecamatan_tambah'),
    path('kecamatan/<int:pk>/edit/', views.kecamatan_edit, name='kecamatan_edit'),
    path('kecamatan/<int:pk>/hapus/', views.kecamatan_hapus, name='kecamatan_hapus'),

    path('gereja/', views.gereja_list, name='gereja_list'),
    path('gereja/tambah/', views.gereja_tambah, name='gereja_tambah'),
    path('gereja/<int:pk>/edit/', views.gereja_edit, name='gereja_edit'),
    path('gereja/<int:pk>/hapus/', views.gereja_hapus, name='gereja_hapus'),

    path('masjid/', views.masjid_list, name='masjid_list'),
    path('masjid/tambah/', views.masjid_tambah, name='masjid_tambah'),
    path('masjid/<int:pk>/edit/', views.masjid_edit, name='masjid_edit'),
    path('masjid/<int:pk>/hapus/', views.masjid_hapus, name='masjid_hapus'),
]
