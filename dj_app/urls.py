from django.urls import path
from dj_app import views

urlpatterns = [
    path('actions/split/<company_slug>/', views.SplitShareAPIView.as_view()),
    path('actions/sell/<company_slug>/', views.SellSharesAPIView.as_view()),
    path('holdings/<company_slug>/', views.HoldingDetailsAPIView.as_view()),
]
