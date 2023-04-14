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

urlpatterns_volumes_calc = [
    path(
        'volumes_calc/<int:pk>/',
        views.VolumesCalcDetailView.as_view(),
        name='volumes_calc_detail',
    ),
    path(
        'volumes_calc/create/',
        views.VolumesCalcCreateView.as_view(),
        name='volumes_calc_create',
    ),
    path(
        'volumes_calc/<int:pk>/update/',
        views.VolumesCalcUpdateView.as_view(),
        name='volumes_calc_update',
    ),
    path(
        'volumes_calc/<int:pk>/duplicate/',
        views.VolumesCalcDuplicateView.as_view(),
        name='volumes_calc_duplicate',
    ),
    path(
        'volumes_calc/<int:pk>/delete/',
        views.VolumesCalcDeleteView.as_view(),
        name='volumes_calc_delete',
    ),

    path(
        'volume/<int:pk>/duplicate/',
        views.VolumeDuplicateView.as_view(),
        name='volume_duplicate',
    ),
    path(
        'volume/<int:pk>/delete/',
        views.VolumeDeleteView.as_view(),
        name='volume_delete',
    ),
]

urlpatterns_squares_calc = [
    path(
        'squares_calc/<int:pk>/',
        views.SquaresCalcDetailView.as_view(),
        name='squares_calc_detail',
    ),
    path(
        'squares_calc/create/',
        views.SquaresCalcCreateView.as_view(),
        name='squares_calc_create',
    ),
    path(
        'squares_calc/<int:pk>/update/',
        views.SquaresCalcUpdateView.as_view(),
        name='squares_calc_update',
    ),
    path(
        'squares_calc/<int:pk>/duplicate/',
        views.SquaresCalcDuplicateView.as_view(),
        name='squares_calc_duplicate',
    ),
    path(
        'squares_calc/<int:pk>/delete/',
        views.SquaresCalcDeleteView.as_view(),
        name='squares_calc_delete',
    ),

    path(
        'square/<int:pk>/duplicate/',
        views.SquareDuplicateView.as_view(),
        name='square_duplicate',
    ),
    path(
        'square/<int:pk>/delete/',
        views.SquareDeleteView.as_view(),
        name='square_delete',
    ),
]

urlpatterns_lengths_calc = [
    path(
        'lengths_calc/<int:pk>/',
        views.LengthsCalcDetailView.as_view(),
        name='lengths_calc_detail',
    ),
    path(
        'lengths_calc/create/',
        views.LengthsCalcCreateView.as_view(),
        name='lengths_calc_create',
    ),
    path(
        'lengths_calc/<int:pk>/update/',
        views.LengthsCalcUpdateView.as_view(),
        name='lengths_calc_update',
    ),
    path(
        'lengths_calc/<int:pk>/duplicate/',
        views.LengthsCalcDuplicateView.as_view(),
        name='lengths_calc_duplicate',
    ),
    path(
        'lengths_calc/<int:pk>/delete/',
        views.LengthsCalcDeleteView.as_view(),
        name='lengths_calc_delete',
    ),

    path(
        'length/<int:pk>/duplicate/',
        views.LengthDuplicateView.as_view(),
        name='length_duplicate',
    ),
    path(
        'length/<int:pk>/delete/',
        views.LengthDeleteView.as_view(),
        name='length_delete',
    ),
]

urlpatterns_units_calc = [
    path(
        'units_calc/<int:pk>/',
        views.UnitsCalcDetailView.as_view(),
        name='units_calc_detail',
    ),
    path(
        'units_calc/create/',
        views.UnitsCalcCreateView.as_view(),
        name='units_calc_create',
    ),
    path(
        'units_calc/<int:pk>/update/',
        views.UnitsCalcUpdateView.as_view(),
        name='units_calc_update',
    ),
    path(
        'units_calc/<int:pk>/duplicate/',
        views.UnitsCalcDuplicateView.as_view(),
        name='units_calc_duplicate',
    ),
    path(
        'units_calc/<int:pk>/delete/',
        views.UnitsCalcDeleteView.as_view(),
        name='units_calc_delete',
    ),

    path(
        'unit/<int:pk>/duplicate/',
        views.UnitDuplicateView.as_view(),
        name='unit_duplicate',
    ),
    path(
        'unit/<int:pk>/delete/',
        views.UnitDeleteView.as_view(),
        name='unit_delete',
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
        + urlpatterns_volumes_calc
        + urlpatterns_squares_calc
        + urlpatterns_lengths_calc
        + urlpatterns_units_calc
)
