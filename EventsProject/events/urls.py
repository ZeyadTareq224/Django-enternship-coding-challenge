from django.urls import path

from . import views

urlpatterns = [
    path('', views.eventListView, name="events-list"),
    path('event/<int:pk>/', views.eventDetailView, name="event-details"),
    path('event/create/', views.eventCreateView, name="event-create"),
    path('event/update/<int:pk>/', views.eventUpdateView, name="event-update"),
    path('event/delete/<int:pk>/', views.eventDeleteView, name="event-delete"),
    path('event/subscribe/<int:event_id>/', views.subscribeToEventView, name="event-subscribe"),
    path('event/withdraw/<int:event_id>/', views.withdrawalFromEventView, name="event-withdrawal"),
    path('event/dashboard/', views.userDashboardView, name="dashboard"),
]
