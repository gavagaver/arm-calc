from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'calc'

urlpatterns_objects = [
    path(
        'site/<int:pk>/',
        views.SiteDetailView.as_view(),
        name='site_detail',
    ),
    path(
        'site/create/',
        views.SiteCreateView.as_view(),
        name='site_create',
    ),
    path(
        'site/<int:pk>/update/',
        views.SiteUpdateView.as_view(),
        name='site_update',
    ),
    path(
        'site/<int:pk>/duplicate/',
        views.site_duplicate,
        name='site_duplicate',
    ),
    path(
        'site/<int:pk>/delete/',
        views.site_delete,
        name='site_delete',
    ),

    path(
        'construction/<int:pk>/',
        views.ConstructionDetailView.as_view(),
        name='construction_detail',
    ),
    path(
        'site/<int:site_pk>/construction-create/',
        views.ConstructionCreateView.as_view(),
        name='construction_create',
    ),
    path(
        'construction/<int:pk>/update/',
        views.ConstructionUpdateView.as_view(),
        name='construction_update',
    ),
    path(
        'construction/<int:pk>/duplicate/',
        views.construction_duplicate,
        name='construction_duplicate',
    ),
    path(
        'construction/<int:pk>/delete/',
        views.construction_delete,
        name='construction_delete',
    ),

    path(
        'version/<int:pk>/',
        views.VersionDetailView.as_view(),
        name='version_detail',
    ),
    path(
        'construction/<int:construction_pk>/version-create/',
        views.VersionCreateView.as_view(),
        name='version_create',
    ),
    path(
        'version/<int:pk>/update/',
        views.VersionUpdateView.as_view(),
        name='version_update',
    ),
    path(
        'version/<int:pk>/duplicate/',
        views.version_duplicate,
        name='version_duplicate',
    ),
    path(
        'version/<int:pk>/delete/',
        views.version_delete,
        name='version_delete',
    ),

    path(
        'folder/<int:pk>/',
        views.FolderDetailView.as_view(),
        name='folder_detail',
    ),
    path(
        'version/<int:version_pk>/folder-create/',
        views.FolderCreateView.as_view(),
        name='folder_create',
    ),
    path(
        'folder/<int:pk>/update/',
        views.FolderUpdateView.as_view(),
        name='folder_update',
    ),
    path(
        'folder/<int:pk>/duplicate/',
        views.folder_duplicate,
        name='folder_duplicate',
    ),
    path(
        'folder/<int:pk>/delete/',
        views.folder_delete,
        name='folder_delete',
    ),

    path(
        'element/<int:pk>/',
        views.ElementDetailView.as_view(),
        name='element_detail',
    ),
    path(
        'folder/<int:folder_pk>/element-create/',
        views.ElementCreateView.as_view(),
        name='element_create',
    ),
    path(
        'element/<int:pk>/update/',
        views.ElementUpdateView.as_view(),
        name='element_update',
    ),
    path(
        'element/<int:pk>/duplicate/',
        views.element_duplicate,
        name='element_duplicate',
    ),
    path(
        'element/<int:pk>/delete/',
        views.element_delete,
        name='element_delete',
    ),
]

urlpatterns_rods_calc = [
    path(
        'element/<int:element_pk>/rods-calc-create/',
        views.RodsCalcCreateView.as_view(),
        name='rods_calc_create',
    ),
    path(
        'rods_calc/<int:pk>/update/',
        views.RodsCalcUpdateView.as_view(),
        name='rods_calc_update',
    ),
    path(
        'rods_calc/<int:pk>/duplicate/',
        views.rods_calc_duplicate,
        name='rods_calc_duplicate',
    ),
    path(
        'rods_calc/<int:pk>/delete/',
        views.rods_calc_delete,
        name='rods_calc_delete',
    ),
    path(
        'rods_calc/<int:pk>/result/',
        views.RodsCalcResultView.as_view(),
        name='rods_calc_result',
    ),

    path(
        'rod/<int:pk>/duplicate/',
        views.rod_duplicate,
        name='rod_duplicate',
    ),
    path(
        'rod/<int:pk>/delete/',
        views.rod_delete,
        name='rod_delete',
    ),
]

urlpatterns = (
        [
            path(
                '',
                views.LandingView.as_view(),
                name='landing',
            ),
            path(
                'profile/<str:username>/',
                views.ProfileView.as_view(),
                name='profile',
            ),
        ]
        + urlpatterns_objects
        + urlpatterns_rods_calc
)
