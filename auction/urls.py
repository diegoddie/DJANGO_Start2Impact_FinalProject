from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('auctions/', views.AuctionListView.as_view(), name='auctions'),
    path('auctions/<int:pk>/', views.AuctionDetailView.as_view(), name='auction-detail'),
    path('profile/', views.user_profile, name='user-profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)