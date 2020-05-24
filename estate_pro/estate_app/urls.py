from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'estate_app'

urlpatterns = [
    path('create/', views.PropertyCreateView.as_view(), name="property_create"),
    path('', views.PropertyListView.as_view(), name='property_list_view'),
    path('myoffers/', views.MyOfferList.as_view(), name='my_offers_list'),
    path('myoffers/<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='delete_property'),
    path('myoffers/<int:pk>/edit/', views.PropertyEditView.as_view(), name='edit_property' ),
    path('<str:username>/offers/', views.UserOffersList.as_view(), name='user_offers_view'),
    path('offers/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail_view'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
