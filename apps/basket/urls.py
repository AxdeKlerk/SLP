# apps/basket/urls.py
from django.urls import path
from . import views
from apps.basket.views import basket_view, add_event_to_basket, add_merch_to_basket

app_name = "basket"

urlpatterns = [
    path('', views.basket_view, name='basket_view'),
    path('add/<int:event_id>/', views.add_event_to_basket, name='add_event_to_basket'),
    path('add-merch/<int:merch_id>/', views.add_merch_to_basket, name='add_merch_to_basket'),
    path("update/<int:item_id>/", views.update_item, name="update_item"),
    path("delete/<int:item_id>/", views.delete_item, name="delete_item"),
]